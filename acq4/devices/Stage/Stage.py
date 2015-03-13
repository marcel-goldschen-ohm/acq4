# -*- coding: utf-8 -*-
from acq4.devices.Device import *
from acq4.devices.OptomechDevice import *
from acq4.util.Mutex import Mutex
import acq4.pyqtgraph as pg


class Stage(Device, OptomechDevice):
    """Base class for mechanical stages with motorized control and/or position feedback.
    """

    sigPositionChanged = QtCore.Signal(object)
    sigLimitsChanged = QtCore.Signal(object)

    def __init__(self, dm, config, name):
        Device.__init__(self, dm, config, name)
        OptomechDevice.__init__(self, dm, config, name)
        self.config = config
        self.lock = Mutex(QtCore.QMutex.Recursive)
        self.pos = [0]*3
        self._defaultSpeed = 'fast'
        
        self._limits = [(None, None), (None, None), (None, None)]

        self._progressDialog = None
        self._progressTimer = QtCore.QTimer()
        self._progressTimer.timeout.connect(self.updateProgressDialog)

        dm.declareInterface(name, ['stage'], self)

    def quit(self):
        self.stop()
    
    def capabilities(self):
        """Return a structure describing the capabilities of this device::
        
            {
                'getPos': (x, y, z),   # whether each axis can be read from the device
                'setPos': (x, y, z),   # whether each axis can be set on the device
                'limits': (x, y, z),   # whether limits can be set for each axis
            }
            
        Subclasses must reimplement this method.
        """
        # todo: add other capability flags like resolution, speed, closed-loop, etc?
        raise NotImplementedError

    def posChanged(self, pos):
        """Handle device position changes by updating the device transform and
        emitting sigPositionChanged.

        Subclasses must call this method when the device position has changed.
        """
        with self.lock:
            rel = [0] * len(self.pos)
            rel[:len(pos)] = [pos[i] - self.pos[i] for i in range(len(pos))]
            self.pos[:len(pos)] = pos
        
        tr = pg.SRTTransform3D()
        tr.translate(*self.pos)
        self.setDeviceTransform(tr) ## this informs rigidly-connected devices that they have moved

        self.sigPositionChanged.emit({'rel': rel, 'abs': self.pos[:]})

    def getPosition(self, refresh=False):
        """
        Return the position of the stage.
        If refresh==False, the last known position is returned. Otherwise, the
        current position is requested from the controller. If request is True,
        then the position request may block if the device is currently busy.
        """
        if not refresh:
            return self.pos[:]
        else:
            return self._getPosition()

    def _getPosition(self):
        """
        Must be reimplemented by subclass to re-read position from device.
        """
        raise NotImplementedError()

    def getState(self):
        with self.lock:
            return (self.pos[:],)

    def deviceInterface(self, win):
        return StageInterface(self, win)

    def setDefaultSpeed(self, speed):
        """Set the default speed of the device when moving.
        
        Generally speeds are specified approximately in m/s, although many 
        devices lack the capability to accurately set speed. This value may 
        also be 'fast' to indicate the device should move as quickly as 
        possible, or 'slow' to indicate the device should minimize vibrations
        while moving.        
        """
        if speed not in ('fast', 'slow'):
            speed = abs(float(speed))
        self._defaultSpeed = speed

    def isMoving(self):
        """Return True if the device is currently moving.
        """
        raise NotImplementedError()        

    def move(self, abs=None, rel=None, speed=None, progress=False):
        """Move the device to a new position.
        
        Must specify either *abs* for an absolute position, or *rel* for a
        relative position. Either argument must be a sequence (x, y, z) with
        values in meters. Optionally, values may be None to indicate no 
        movement along that axis.
        
        If the *speed* argument is given, it temporarily overrides the default
        speed that was defined by the last call to setSpeed().
        
        If *progress* is True, then display a progress bar until the move is complete.

        Return a MoveFuture instance that can be used to monitor the progress 
        of the move.
        """
        if speed is None:
            speed = self._defaultSpeed
        if speed is None:
            raise TypeError("Must specify speed or set default speed before moving.")
        if abs is None and rel is None:
            raise TypeError("Must specify one of abs or rel arguments.")

        mfut = self._move(abs, rel, speed)

        if progress:
            self._progressDialog = QtGui.QProgressDialog("%s moving..." % self.name(), None, 0, 100)
            self._progressDialog.mf = mfut
            self._progressTimer.start(100)

        return mfut
        
    def _move(self, abs, rel, speed):
        """Must be reimplemented by subclasses and return a MoveFuture instance.
        """
        raise NotImplementedError()

    def _toAbsolutePosition(self, abs, rel):
        """Helper function to convert absolute or relative position (possibly 
        containing Nones) to an absolute position.
        """
        if rel is None:
            if any([x is None for x in abs]):
                pos = self.getPosition()
                for i,x in enumerate(abs):
                    if x is not None:
                        pos[i] = x
            else:
                pos = abs
        else:
            pos = self.getPosition()
            for i,x in enumerate(rel):
                if x is not None:
                    pos[i] += x
        return pos
        
    def moveBy(self, pos, speed, progress=False):
        """Move by the specified relative distance. See move() for more 
        information.
        """
        return self.move(rel=pos, speed=speed, progress=progress)

    def moveTo(self, pos, speed, progress=False):
        """Move to the specified absolute position. See move() for more 
        information.
        """
        return self.move(abs=pos, speed=speed, progress=progress)
    
    def stop(self):
        """Stop moving the device immediately.
        """
        raise NotImplementedError()

    def updateProgressDialog(self):
        done = self._progressDialog.mf.percentDone()
        self._progressDialog.setValue(done)
        if done == 100:
            self._progressTimer.stop()

    def setLimits(self, x=None, y=None, z=None):
        """Set the (min, max) position limits to enforce for each axis.

        Note that some devices do not support limits.
        """
        changed = []
        for axis, limit in enumerate((x, y, z)):
            if self.capabilities()['limits'][axis] is not True:
                raise TypeError("Device does not support settings limits for axis %d." % axis)
            if tuple(self._limits[axis]) != tuple(limit):
                changed.append(axis)
                self._limits[axis] = tuple(limit)

        if len(changed) > 0:
            self.sigLimitsChanged.emit(changed)

    def getLimits(self):
        """Return a list the (min, max) position limits for each axis.
        """
        return self._limits[:]


class MoveFuture(object):
    """Used to track the progress of a requested move operation.
    """
    def __init__(self, dev, pos, speed):
        self.dev = dev
        self.speed = speed
        self.targetPos = pos
        self.startPos = dev.getPosition()
        
    def percentDone(self):
        """Return the percent of the move that has completed.
        
        The default implementation calls getPosition on the device to determine
        the percent complete. Devices that do not provide position updates while 
        moving should reimplement this method.
        """
        s = np.array(self.startPos)
        t = np.array(self.targetPos)
        p = np.array(self.dev.getPosition())
        return 100 * ((p - s) / (t - s)).mean()

    def wasInterrupted(self):
        """Return True if the move was interrupted before completing.
        """
        raise NotImplementedError()

    def isDone(self):
        """Return True if the move has completed or was interrupted.
        """
        return self.percentDone() == 100 or self.wasInterrupted()
        
    def wait(self, timeout=10):
        """Block until the move has completed, been interrupted, or the
        specified timeout has elapsed.
        """
        start = ptime.time()
        while ptime.time() < start+timeout:
            if self.isDone():
                break
            time.sleep(0.1)


class StageInterface(QtGui.QWidget):
    def __init__(self, dev, win):
        QtGui.QWidget.__init__(self)
        self.win = win
        self.dev = dev

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.axCtrls = {}
        self.posLabels = {}
        self.limitChecks = {}

        cap = dev.capabilities()
        self.nextRow = 0

        for axis in (0, 1, 2):
            if cap['getPos'][axis]:
                axLabel = QtGui.QLabel('XYZ'[axis])
                posLabel = QtGui.QLabel('0')
                self.posLabels[axis] = posLabel
                widgets = [axLabel, posLabel]
                if cap['limits'][axis]:
                    minCheck = QtGui.QCheckBox('Min:')
                    minBtn = QtGui.QPushButton('set')
                    minBtn.setMaximumWidth(30)
                    maxCheck = QtGui.QCheckBox('Max:')
                    maxBtn = QtGui.QPushButton('set')
                    maxBtn.setMaximumWidth(30)
                    self.limitChecks[axis] = (minCheck, maxCheck)
                    widgets.extend([minCheck, minBtn, maxCheck, maxBtn])
                for i,w in enumerate(widgets):
                    self.layout.addWidget(w, self.nextRow, i)
                self.axCtrls[axis] = widgets
                self.nextRow += 1

        self.updateLimits()
        self.dev.sigPositionChanged.connect(self.update)
        self.dev.sigLimitsChanged.connect(self.updateLimits)
        self.update()

    def update(self):
        pos = self.dev.getPosition()
        for i in range(3):
            if i not in self.posLabels:
                continue
            text = pg.siFormat(pos[i], suffix='m', precision=5)
            self.posLabels[i].setText(text)

    def updateLimits(self):
        limits = self.dev.getLimits()
        cap = self.dev.capabilities()
        for axis in range(0, 1, 2):
            if not cap['limits'][axis]:
                continue
            for i,limit in enumerate(limits[axis]):
                check = self.limitChecks[axis][i]
                cap = ('Max:', 'Min:')[i]
                if limit is None:
                    check.setCaption(cap)
                    check.setChecked(False)
                else:
                    check.setCaption(cap + ' %s' % pg.siFormat(limit, suffix='m'))
                    check.setChecked(True)









