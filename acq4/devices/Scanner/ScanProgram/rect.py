# -*- coding: utf8 -*-

from __future__ import division
import weakref
import numpy as np
from collections import OrderedDict

import acq4.pyqtgraph as pg
from acq4.pyqtgraph import QtGui, QtCore
import acq4.pyqtgraph.parametertree.parameterTypes as pTypes
from acq4.pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from .component import ScanProgramComponent
from acq4.util.StateSolver import StateSolver

class RectScanComponent(ScanProgramComponent):
    """
    Does a raster scan of a rectangular area.
    """
    name = 'rect'
    
    def __init__(self, cmd=None, scanProgram=None):
        ScanProgramComponent.__init__(self, cmd, scanProgram)
        self.ctrl = RectScanControl(self)
        
    def setSampleRate(self, rate, downsample):
        ScanProgramComponent.setSampleRate(rate, downsample)
        self.ctrl.update()

    def ctrlParameter(self):
        """
        The Parameter (see acq4.pyqtgraph.parametertree) set used to allow the 
        user to define this component.        
        """
        return self.ctrl.parameters()
    
    def graphicsItems(self):
        """
        A list of GraphicsItems to be displayed in a camera module or image
        analysis module. These show the location and shape of the scan 
        component, and optionally offer user interactivity to define the shape.
        """
        return self.ctrl.getGraphicsItems()

    def generateTask(self):
        return self.ctrl.generateTask()

    @classmethod
    def generateVoltageArray(cls, array, dt, dev, cmd, startInd, stopInd):
        pts = cmd['points']
        # print 'cmd: ', cmd
        SUF = ScannerUtility()
        SUF.setScannerDev(dev)
        SUF.setLaserDev(cmd['laser'])
        
        width  = (pts[1] -pts[0]).length() # width is x in M
        height = (pts[2]- pts[0]).length() # heigh in M
        rect = [pts[0][0], pts[0][1], width, height]
        overScanPct = cmd['overScan']
        SUF.setRectRoi(pts)
        SUF.setOverScan(overScanPct)
        SUF.setDownSample(1)
        SUF.setBidirectional(True)
        pixelSize = cmd['pixelSize']
        # recalulate pixelSize based on:
        # number of scans (reps) and total duration
        nscans = cmd['nScans']
        dur = cmd['duration']#  - cmd['startTime'] # time for nscans
        durPerScan = dur/nscans # time for one scan
        SUF.setPixelSize(cmd['pixelSize']) # pixelSize/np.sqrt(pixsf)) # adjust the pixel size
        SUF.setSampleRate(1./dt) # actually this is not used... 
        (x,y) = SUF.designRectScan() # makes one rectangle
        effScanTime = (SUF.getPixelsPerRow()/pixelSize)*(height/pixelSize)*dt # time it actually takes for one scan 
        pixsf = durPerScan/effScanTime # correction for pixel size based pm to,e

        cmd['imageSize'] = (SUF.getPixelsPerRow(), SUF.getnPointsY())

        printParameters = False
        if printParameters:
            print 'scans: ', nscans
            print 'width: ', width
            print 'points in width: ', width/pixelSize
            print 'dt: ', dt
            print 'points in a scan: ', (width/pixelSize)*(height/pixelSize)
            print 'effective scan time: ', effScanTime
            print 'pixsf: ', pixsf
            print 'original: ', pixelSize
            print 'new pix size: ', pixelSize*pixsf
        
        n = SUF.getnPointsY() # get number of rows
        m = SUF.getPixelsPerRow() # get number of points per row

        ## Build array with scanner voltages for rect repeated once per scan
        for i in range(cmd['nScans']):
            thisStart = startInd+i*n*m
            array[0, thisStart:thisStart + len(x)] = x
            array[1, thisStart:thisStart + len(y)] = y
        array[0, startInd+n*m*cmd['nScans']:stopInd] = array[0, startInd+n*m*cmd['nScans'] -1] # fill in any unused sample on this scan section
        array[1, startInd+n*m*cmd['nScans']:stopInd] = array[1, startInd+n*m*cmd['nScans'] -1]
        lastPos = (x[-1], y[-1])
            
            
        # A side-effect modification of the 'command' dict so that analysis can access
        # this information later
        cmd['scanParameters'] = SUF.packScannerParams()
        cmd['scanInfo'] = SUF.getScanInfo()

        return stopInd

class RectScanROI(pg.ROI):
    def __init__(self, size, pos):
        pg.ROI.__init__(self, size=size, pos=pos)
        self.addScaleHandle([1,1], [0.5, 0.5])
        self.addRotateHandle([0,0], [0.5, 0.5])
        self.overScan = 0

    def setOverScan(self, os):
        self.overScan = os
        self.prepareGeometryChange()
        self.update()

    def boundingRect(self):
        br = pg.ROI.boundingRect(self)
        os = br.width() * 0.5 * self.overScan/100.
        return br.adjusted(-os, 0, os, 0)

    def paint(self, p, *args):
        p.setPen(pg.mkPen(0.3))
        p.drawRect(self.boundingRect())
        pg.ROI.paint(self, p, *args)




class RectScanControl(QtCore.QObject):
    
    sigStateChanged = QtCore.Signal(object)
    
    def __init__(self, component):
        QtCore.QObject.__init__(self)
        ### These need to be initialized before the ROI is initialized because they are included in stateCopy(), which is called by ROI initialization.
        self.name = component.name
        self.blockUpdate = False
        self.component = weakref.ref(component)
        
        params = [
            dict(name='width', readonly=True, type='float', value=2e-5, suffix='m', siPrefix=True, bounds=[1e-6, None], step=1e-6),
            dict(name='height', readonly=True, type='float', value=1e-5, suffix='m', siPrefix=True, bounds=[1e-6, None], step=1e-6),
            dict(name='overScan', type='float', value=70., suffix='%', siPrefix=False, bounds=[0, 200.], step = 1),
            dict(name='pixelSize', type='float', value=4e-7, suffix='m', siPrefix=True, bounds=[2e-7, None], step=2e-7),
            dict(name='startTime', type='float', value=1e-2, suffix='s', siPrefix=True, bounds=[0., None], step=1e-2),
            dict(name='nScans', type='int', value=10, bounds=[1, None]),
            dict(name='duration', type='float', value=5e-1, suffix='s', siPrefix=True, bounds=[0., None], step=1e-2),
            dict(name='imageSize', type='str', readonly=True),
            dict(name='scanSpeed', type='float', readonly=True, suffix='m/ms', siPrefix=True), 
            dict(name='frameExp', title=u'frame exposure/μm²', type='float', readonly=True, suffix='s', siPrefix=True), 
            dict(name='totalExp', title=u'total exposure/μm²', type='float', readonly=True, suffix='s', siPrefix=True),
        ]
        self.params = pTypes.SimpleParameter(name=self.name, type='bool', value=True, removable=True, renamable=True, children=)
        self.params.component = self.component
        
        self.roi = RectScanROI(size=[self.params['width'], self.params['height']], pos=[0.0, 0.0])
        self.roi.setOverScan(self.params['overScan'])

        self.params.sigTreeStateChanged.connect(self.paramsChanged)
        self.roi.sigRegionChangeFinished.connect(self.roiChanged)
        
    def getGraphicsItems(self):
        return [self.roi]

    def isActive(self):
        return self.params.value()
 
    def setVisible(self, vis):
        if vis:
            self.roi.setOpacity(1.0)  ## have to hide this way since we still want the children to be visible
            for h in self.roi.handles:
                h['item'].setOpacity(1.0)
        else:
            self.roi.setOpacity(0.0)
            for h in self.roi.handles:
                h['item'].setOpacity(0.0)
                
    def parameters(self):
        return self.params

    def paramsChanged(self, param, changes):
        self.update(changed=[changes[0][0].name()])
        
    def update(self, changed=()):
        # Update all parameters to ensure consistency. 
        # *changed* may be a list of parameter names that have changed;
        # these will be kept constant during the update, if possible.
        
        if self.blockUpdate:
            return

        try:
            self.blockUpdate = True

            if 'overScan' in changed:
                self.roi.setOverScan(self.params['overScan'])

            self.setVisible(self.params.value())
            
            # TODO: this should be calculated by the same code that is used to generate the voltage array
            # (as currently written, it is unlikely to match the actual output exactly)

            w = self.params['width'] * (1.0 + self.params['overScan']/100.)
            h = self.params['height']
            sampleRate = float(self.component().sampleRate)
            downsample = self.component().downsample
            
            if 'duration' in changed:
                # Set pixelSize to match duration
                duration = self.params['duration']
                maxSamples = int(duration * sampleRate)
                maxPixels = maxSamples / downsample
                ar = w / h
                pxHeight = int((maxPixels / ar)**0.5)
                pxWidth = int(ar * pxHeight)
                imgSize = (pxWidth, pxHeight)
                pxSize = w / (pxWidth-1)
                self.params['pixelSize'] = pxSize
            else:
                # set duration to match pixelSize
                pxSize = self.params['pixelSize']
                imgSize = (int(w / pxSize) + 1, int(h / pxSize) + 1) 
                samples = imgSize[0] * imgSize[1] * downsample
                duration = samples / sampleRate
                self.params['duration'] = duration

            # Set read-only parameters:

            self.params['imageSize'] = str(imgSize)
            
            speed = w / (imgSize[0] * downsample / sampleRate)
            self.params['scanSpeed'] = speed * 1e-3

            samplesPerUm2 = 1e-12 * downsample / pxSize**2
            frameExp = samplesPerUm2 / sampleRate
            totalExp = frameExp * self.params['nScans']
            self.params['frameExp'] = frameExp
            self.params['totalExp'] = totalExp

        finally:
            self.blockUpdate = False

    
    def roiChanged(self):
        """ read the ROI rectangle width and height and repost
        in the parameter tree """
        state = self.roi.getState()
        w, h = state['size']
        self.params['width'] = w
        self.params['height'] = h
        
    def generateTask(self):
        state = self.roi.getState()
        w, h = state['size']
        p0 = pg.Point(0,0)
        p1 = pg.Point(w,0)
        p2 = pg.Point(0, h)
        points = [p0, p1, p2]
        points = [pg.Point(self.roi.mapToView(p)) for p in points] # convert to view points (as needed for scanner)
        return {'type': self.name, 'active': self.isActive(), 'points': points, 'startTime': self.params['startTime'], 
                'endTime': self.params['duration']+self.params['startTime'], 'duration': self.params['duration'],
                'nScans': self.params['nScans'],
                'pixelSize': self.params['pixelSize'], 'overScan': self.params['overScan'],
                }
        




arr = np.ndarray # just to clean up defaultState below..
class RectScan(StateSolver):
    """
    Manages the system of equations necessary to define a rectangular scanning area. 

    * Input parameters may be specified in any combination (as long as all DOF are fixed). 
    * Parameters may be individually locked 
    * Able to save and reload state information to disk

    Input parameters:

        * 3 corners of the scan area:

            p0______p1
            |
            |
            p2 

            * height / width
            * overscan (measured in us)

        * Horizontal / vertical sample density
        * Sample rate
        * Downsampling
        * Pixel size
        * Bidirectional
        * Total duration

    Output parameters:

        * scan offset, shape, strides  (includes overscan, ignores downsampling)
        * start position, delta vectors
        * bidirectionality
        * position array, voltage array, laser mask array

        * exposure time per um^2
        * image offset, shape, strides  (excludes overscan, includes downsampling)
        * image transform

    Theory:
    
        * There are 6 degrees of freedom that determine which array index 
          represents which point: scan shape (w, h), scan strides (x, y),
          bidirectionality, and overscan. With these variables one can 
          reconstruct an image from a PMT signal. 
        * There are 5 degrees of freedom that determine the placement of the 
          scan rectangle: p0(x,y), width, height, and angle. With these 
          variables, one can place the image into the global coordinate system.
          (For coding simplicity, it may be easier to consider a 6DOF 
          parallelogram instead, defined by p0,p1,p2)
        * There are 2 degrees of freedom affecting timing: sample rate and 
          downsampling. With these, the start/stop times, exposure times, etc.
          can be determined.
        * Various constraints may be applied:
            * fixed pixel shape (usually square)
            * maximum / fixed exposure
            * maximum / fixed duration
            * maximum / fixed pixel size
    """
    defaultState = OrderedDict([
            ('p0', [None, arr, None, 'f']),  # 3 corners of the rectangle
            ('p1', [None, arr, None, 'nf']),
            ('p2', [None, arr, None, 'nf']),
            ('width', [None, float, None, 'nf']),  # width of requested scan area, excluding overscan
            ('height', [None, float, None, 'nf']),
            ('angle', [None, float, None, 'nf']),
            ('overscan', [None, float, None, 'f']),  # overscan duration (sec)
            ('osP0', [None, arr, None, 'n']),
            ('osP1', [None, arr, None, 'n']),
            ('osVector', [None, arr, None, 'n']),  # vector from p1 -> osP1
            ('osLen', [None, int, None, 'n']),     # number of samples in overscan region (single row, one side)
            ('fullWidth', [None, float, None, 'n']), # full width of the scan area, including overscan
            ('pixelWidth', [None, float, None, 'nfr']),
            ('pixelHeight', [None, float, None, 'nfr']),
            ('pixelAspectRatio', [None, float, None, 'nf']),
            ('bidirectional', [None, bool, None, 'f']),
            ('sampleRate', [None, float, None, 'f']),
            ('downsample', [None, int, None, 'f']),
            ('duration', [None, float, None, 'nfr']),
            ('scanOffset', [None, int, None, 'n']),  # Offset, shape, and stride describe
            ('scanShape', [None, arr, None, 'n']),   # the full scan area including overscan
            ('scanStride', [None, arr, None, 'n']),  # and ignoring downsampling (index in samples)
            ('numRows', [None, int, None, 'n']),     # Same as scanShape[1] 
            #('sampleVectors', [None, arr, None, 'n']),
            ('exposurePerUm2', [None, float, None, 'nfr']),
            ('scanSpeed', [None, float, None, 'nfr']),
            ('activeOffset', [None, int, None, 'n']),  # Offset, shape, and stride describe
            ('activeShape', [None, arr, None, 'n']),   # the 'active' scan area excluding overscan
            ('activeStride', [None, arr, None, 'n']),  # and ignoring downsampling (index in samples)
            ('imageOffset', [None, int, None, 'n']),  # Offset, shape, and stride describe 
            ('imageShape', [None, arr, None, 'n']),   # the 'active' image area excluding overscan
            ('imageStride', [None, arr, None, 'n']),  # and accounting for downsampling (index in pixels)
            ])

    
    ### Functions defining the relationships between variables:
    
    def _width(self):
        return np.linalg.norm(self.p1 - self.p0)
            
    def _height(self):
        return np.linalg.norm(self.p2 - self.p0)

    def _angle(self):
        return angle(self.p1 - self.p0)

    def _p1(self):
        p0 = self.p0
        width = self.width
        angle = self.angle
        return p0 + width * np.array(np.cos(angle), np.sin(angle))

    def _p2(self):
        p0 = self.p0
        height = self.height
        angle = self.angle
        return p0 + height * np.array(np.sin(angle), -np.cos(angle))

    def _osVector(self):
        # This vector is p1 -> osP1
        # Compute from p0, overscan, and scanSpeed
        speed = self.scanSpeed
        os = self.overscan
        osDist = speed * os
        
        p0 = self.p0
        p1 = self.p1
        dx = p1 - p0
        dx *= osDist / np.linalg.norm(dx)
        
        return dx

    def _osLen(self):
        """Length of overscan in px (not samples)"""
        osv = self.osVector
        return np.ceil(np.linalg.norm(osv) / self.pixelWidth)

    def _osP0(self):
        osv = self.osVector
        p0 = self.p0
        return p0 - osv
    
    def _osP1(self):
        osv = self.osVector
        p1 = self.p1
        return p1 + osv
    
    def _fullWidth(self):
        p0 = self.osP0
        p1 = self.osP1
        return np.linalg.norm(p1 - p0)
    
    def _pixelWidth(self):
        try:
            return self.pixelHeight * self.pixelAspectRatio
        
        except RuntimeError:
            return self.scanSpeed / self.sampleRate
        
    def _pixelHeight(self):
        try:
            return self.pixelWidth / self.pixelAspectRatio
        
        except RuntimeError:
            return self.height / (self.numRows - 1)
    
    def _pixelAspectRatio(self):
        return self.pixelWidth / self.pixelHeight
    
    def _duration(self):
        # Note: duration calculation cannot depend on osp0, osp1, oswidth.
        # must be calculated from scan region excluding overscan.
        # (and then we can directly add 2*overscan*nlines)
        imageShape = self.imageShape
        os = self.overscan
        ds = self.downsample
        sr = self.sampleRate
        
        osTime = imageShape[1] * 2 * os
        imageSamples = imageShape[0] * imageShape[1] * ds
        imageTime = imageSamples / sr
        return imageTime + osTime
    
    def _scanSpeed(self):
        try:
            # calculate from pixel size first
            pw = self.pixelWidth
            sr = self.sampleRate
            ds = self.downsample
            return (pw / ds) * sr
            
        except RuntimeError:
            # then from duration
            d = self.duration
            nRows = self.numRows
            os = self.overscan
            osDuration = nRows * 2 * os
            d -= osDuration
            rowTime = d / nRows
            w = self.width
            return w / rowTime

    def _scanOffset(self):
        return 0
    
    def _scanShape(self):
        w, h = self.imageShape
        w = (w + 2 * self.osLen) * self.downsample
        return (w, h)
    
    def _scanStride(self):
        return (self.scanShape[0], 1)

    def _activeOffset(self):
        return self.imageOffset * self.downsample
    
    def _activeShape(self):
        ims = self.imageShape
        return ims * self.downsample
    
    def _activeStride(self):
        return self.scanStride

    def _imageShape(self):
        try:
            # image size and pixel size
            w = self.width
            h = self.height
            pxw = self.pixelWidth
            pxh = self.pixelHeight
            
            nx = int(w / pxw) + 1
            ny = int(h / pxh) + 1
            return (nx, ny)
        except RuntimeError:
            # duration, sample rate, size, and pixel aspect ratio
            w = self.width
            h = self.height
            sr = self.sampleRate
            dur = self.duration
            pxar = self.pixelAspectRatio
            ds = self.downsample
            
            maxPixels = int(dur * sr / ds)
            
            # given we may use maxPixels, what is the best way to fill 
            # the scan area with pixels of the desired pixel aspect ratio?
            shapeRatio = (w / h) / pxar  # this is nx / ny
            
            # solve:   nx * ny == maxPixels
            #          nx / ny == shapeRatio
            #          ==>  ny == (maxPixels / shapeRatio)**0.5
            ny = np.ceil((maxPixels / shapeRatio)**0.5)
            nx = int(maxPixels / ny)
            return (nx, ny)
        
    def _imageOffset(self):
        return self.osLen
    
    def _imageStride(self):
        return (self.scanStride[0] / self.downsample, 1)

    def _numRows(self):
        try:
            return self.imageShape[1]
        except RuntimeError:
            return self.scanShape[1]

    def _exposurePerUm2(self):
        pxArea = (self.pixelWidth * self.pixelHeight)
        samplesPerUm2 = 1e-12 * self.downsample / pxArea
        return samplesPerUm2 / self.sampleRate






class RectScanVideo:
    """
    Manages the system of equations necessary to define a sequence of rectangular scans.
    (note this appears to be a general-case loop)

    Input parameters:

        * # of frames
        * Frame exposure duration
        * Inter-frame duration
        * Frame rate
        * Total duration

    Output parameters:

        * total exposure time per um^2
        * position array, voltage array, laser mask array
        * scan offset, shape, strides
        * video offset, shape, strides
        * image transform


    """



class ScannerUtility:
    """
    1. Decombing routine for scanned images. 
    2. Compute scan voltages for a recangular region
    adding an overscan region.
    3. Create an image with overscan removed.
    """
    def __init__(self):
        self.scannerDev = None
        self.laserDev = None
        self.rectRoi = [pg.Point(0., 0.), pg.Point(0., 1e-4), pg.Point(1e-4, 0.)]
        self.pixelSize = 1e-6
        self.sampleRate = 100000. 
        self.downSample = 5
        self.overScan = 0.
        self.bidirectional = True
        
        # define set/get routines to control the parameters
    def setScannerDev(self, dev):
        self.scannerDev = dev
    
    def getScannerDev(self):
        return(self.scannerDev)
    
    def setLaserDev(self, dev):
        self.laserDev = dev
    
    def getLaserDev(self):
        return(self.laserDev)
    
    def setRectRoi(self, rect):
        if len(rect) == 3: # must specify all coordinates
            self.rectRoi = rect
        else:
            raise Exception("Scanner Utility: setRectRoi requires array of 3 values")
    
    def getRectRoi(self):
        return(self.rectRoi)
    
    def setPixelSize(self, size):
        self.pixelSize = size
        
    def getPixelSize(self):
        return(self.pixelSize)
    
    def setSampleRate(self, sampleRate):
        if sampleRate < 0:
            raise Exception("Scanner Utility: setSampleRate requires positive rate")
        self.sampleRate = sampleRate
    
    def getSampleRate(self):
        return(self.sampleRate)
    
    def setDownSample(self, downsample):
        if downsample < 1 or downsample > 100:
            raise Exception("Scanner Utility: setDownSample requires positive downsample number")
        self.downSample = downsample
        
    def getDownSample(self):
        return(self.downSample)

    def setOverScan(self, overscan):
        if overscan < 0 or overscan > 200:
            raise Exception("ScannerUtility: setOverScan requires number >0 and < 200")
        self.overScan = overscan
        
    def getOverScan(self):
        return self.overScan
    
    def setBidirectional(self, bidirection):
        self.bidirectional = bidirection
        
    def getBidirectional(self):
        return(self.bidirectional)

    def packScannerParams(self):
        """
        put the current scanner parameters into a dictionary with their names
        and return the value
        """
        scannerParams = {'scannerDev': self.scannerDev, 'laserDev': self.laserDev,
                         'rectRoi': self.rectRoi, 'pixelSize': self.pixelSize, 
                         'sampleRate': self.sampleRate, 'downSample': self.downSample,
                         'overScan': self.overScan, 'bidirectional': self.bidirectional}
        return scannerParams

    def setScannerParameters(self, sp):
        """
        set the paramereters from the dictionary retrieved by packScannerParameters
        """
        self.scannerDev = sp['scannerDev']
        self.laserDev = sp['laserDev']
        self.rectRoi = sp['rectRoi']
        self.pixelSize = sp['pixelSize']
        self.sampleRate = sp['sampleRate']
        self.downSample = sp['downSample']
        self.overScan = sp['overScan']
        self.bidirectional = sp['bidirectional']     
        return # just in case we want it as well...

    def getScanInfo(self):
        """
        convenience function - get several scan parameters after the scan
        as a dictionary
        This routine is used, for example in the Imaging (task) module to retrieve
        the scan parameters to reconstruct the image.
        """
        return {'pixelsPerRow': self.pixelsPerRow, 'overScanPixels': self.overScanPixels,
                'nPointsY': self.nPointsY, 'nPointsX': self.nPointsX,
                'samples': self.samples}
    
    def setScanInfo(self, sp):
        """
        convenience function - gst several scan parameters after the scan
        as a dictionary, if the form returned by getScanInfo
        This routine is used, for example in the Imaging (task) module to retrieve
        the scan parameters to reconstruct the image.
        """
        self.pixelsPerRow = sp['pixelsPerRow']
        self.overScanPixels  = sp['overScanPixels']
        self.nPointsY = sp['nPointsY']
        self.nPointsX = sp['nPointsX']       
        self.samples = sp['samples']
        
        
    def checkScannerParams(self):
        sp = self.packScannerParams()
        for p in sp.keys():
            if sp[p] is None:
                raise Exception("ScannerUtility: parameter %s is not set" % p)
        
    def packArgs(self, **kwargs):
        sp = self.packScannerParams() # get the current parameters
        for k, v in kwargs.iteritems():
            if k in sp.keys():
                sp[k] = v
        # now update the instance-specific values from the dictionary
        self.scannerDev = sp['scannerDev']
        self.laserDev = sp['laserDev']
        self.rectRoi = sp['rectRoi']
        self.pixelSize = sp['pixelSize']
        self.sampleRate = sp['sampleRate']
        self.downSample = sp['downSample']
        self.overScan = sp['overScan']
        self.bidirectional = sp['bidirectional']     
        return sp # just in case we want it as well...
    

        
    def designRectScan(self, **kwargs):
        """
        compute the scan voltages for the scanner, corrected by the laser calibration,
        to scan the rectangle specified in standard coordinates, with the rate,
        downsample, overscan and bidirectional flags as set. 
        Pulled from Imager.py, 11/21/2013.
        """
        prof = pg.debug.Profiler(disabled=False)
        self.packArgs(**kwargs) # update any specified arguments
        self.checkScannerParams() # verify all are loaded in in range.
        printPars = True
        if 'printPars' in kwargs.keys():
            printPars = kwargs['printPars']
        
        prof()
        pts = self.rectRoi
        xPos = pts[0][0]
        yPos = pts[0][1]

        width  = (pts[1] -pts[0]).length() # width is x in M
        height = (pts[2]- pts[0]).length() # heigh in M
        self.nPointsX = int(width/self.pixelSize)
        self.nPointsY = int(height/self.pixelSize)
        xScan = np.linspace(0., width, self.nPointsX)
        xScan += xPos
        #print 'design: width: ', width
        #print 'design: height: ', height
        #print 'overscan: ', self.overScan
        
        
        overScanWidth = width*self.overScan/100.
        self.overScanPixels = int((self.nPointsX / 2.) * (self.overScan/100.))
        
        self.pixelsPerRow = self.nPointsX + 2 * self.overScanPixels  ## make sure width is increased by an even number.
        samplesPerRow = self.pixelsPerRow * self.downSample
        self.samples = samplesPerRow * self.nPointsY
        if printPars:
            print 'rectRoi: ', self.rectRoi
            print 'pixelsPer Row: ', self.pixelsPerRow
            print 'nPointsX: ', self.nPointsX
            print 'nPointsY: ', self.nPointsY
            print 'overScan: ', self.overScan
            print 'overScanPixels: ', self.overScanPixels
            print 'downSample: ', self.downSample
            print 'overscanWidth: ', overScanWidth
            print 'samplesperrow: ', samplesPerRow
            print 'xPos, yPos: ', xPos, yPos
        useOldCode = False
        prof()
        if useOldCode:
            if not self.bidirectional:
                saw1 = np.linspace(0., width+overScanWidth, num=samplesPerRow)
                saw1 += xPos-overScanWidth/2.0
                xSaw = np.tile(saw1, (1, self.nPointsY))[0,:]
            else:
                saw1 = np.linspace(0., width+overScanWidth, num=samplesPerRow)
                saw1 += xPos-overScanWidth/2.0
                rows = [saw1, saw1[::-1]] * int(self.nPointsY/2)
            if len(rows) < self.nPointsY:
                rows.append(saw1)
            xSaw = np.concatenate(rows, axis=0)

            yvals = np.linspace(0., width, num=self.nPointsY)
            yvals += yPos
            yScan = np.empty(self.samples)
            for y in range(self.nPointsY):
                yScan[y*samplesPerRow:(y+1)*samplesPerRow] = yvals[y]
                # now translate this scan into scanner voltage coordinates...
            x, y = self.scannerDev.mapToScanner(xSaw, yScan, self.laserDev)
            xSaw = []
            yScan = []
            print 'Old code: x,y min max: ', np.min(x), np.min(y), ' max: ', np.max(x), np.max(y)
            print 'x, y shape: ', x.shape, y.shape

        
        
        ###----------------------------------------------------------------
        ## generate scan array using potentially rotated rectangular ROI
        ## with extended overscan regions.
        
        else:
            ny = self.nPointsY # get number of rows
            nx = samplesPerRow # get number of points per row, including overscan        
            dx = (pts[1]-pts[0])/(self.nPointsX*self.downSample) # (nx-1)
            dy = (pts[2]-pts[0])/self.nPointsY # (ny-1)            
            prof()
            r = np.mgrid[0:ny, 0:nx]
            r = np.roll(r, nx*ny) # swapping order of first axis , also could be r = r[::-1]
            prof()
            if self.bidirectional:
                r[0, 1::2] = r[0, 1::2, ::-1]
            prof()
            # convert image coordinates to physical coordinates to pass to scanner.
            v = np.array([[dx[0], dy[0]], [dx[1], dy[1]]]).reshape(2,2,1,1) 
            prof()
            q = (v*r).sum(axis=1)
            prof()
            trueOrigin = pts[0]-dx*self.overScanPixels*self.downSample
            #print 'trueOrigin: ', trueOrigin
            #print 'pts[0]: ', pts[0]
            q += np.array(trueOrigin).reshape(2,1,1)
            prof()
            x, y = self.scannerDev.mapToScanner(q[0].flatten(), q[1].flatten(), self.laserDev)
            prof()
        #----------------------------------------------------
        prof()
        return (x, y)
    
    def getPixelsPerRow(self):
        return self.pixelsPerRow
    
    def getnPointsY(self):
        return self.nPointsY

    def getOverScanPixels(self):
        print 'getOverScan Pixels has: ', self.overScanPixels
        return self.overScanPixels

    def getSamples(self):
        return self.samples
    
    def getScanXYSize(self):
        # return the size of the data array that the scan will fill
        # as a tuple
        return (self.pixelsPerRow, self.nPointsY)

    def adjustBidirectional(self, imgData, decombAutoFlag, decombShift):
        """
        If the data is from a bidirectional scan, do the decombing with the 
        fixed shift value.
        Optionally, compute the auto decomb value needed to optimize the image.
        Units of the shift coming in here are in seconds (not pixels)
        """
        print 'bidirectional: ', self.bidirectional
        if self.bidirectional:
            for y in range(1, self.nPointsY, 2): # reverse direction for alternate rows
                imgData[:,y] = imgData[::-1,y]
            print 'decomb auto: ', decombAutoFlag
            print 'self samplerate: ', self.sampleRate
            if decombAutoFlag:
                imgData, shift = self.decomb(imgData, minShift=0., maxShift=400e-6*self.sampleRate)  ## correct for mirror lag up to 200us
                decombShift = shift * self.sampleRate
            else:
                print 'shift, samplerate: ', decombShift, self.sampleRate
                imgData, shift = self.decomb(imgData, auto=False, shift=decombShift*self.sampleRate)
            print 'decombshift (microseconds): ', shift / self.sampleRate
        return imgData, shift / self.sampleRate
        

    def makeOverscanBlanking(self, imgData):
        """
        return an array of 1's and 0's where
        the data is 0 in the overscan space, and 1 in the 
        image space
        """
        blankData = np.zeros(imgData.shape)
        osp = self.getOverScanPixels()
        if osp > 0:
            blankData[:,osp:-osp] = 1
        else:
            blankData[:] = 1
        return blankData
    
    def removeOverscan(self, imgData, overscan = None):
        """
        Trim the overscan from the image array
        """
        if overscan is not None:
            osp = overscan
        else:
            osp = self.getOverScanPixels()
        if osp > 0:
            imgData = imgData[osp:-osp]
        return imgData
    
    def decomb(self, img, minShift=0., maxShift=100., auto=True, shift=0):
        ## split image into fields
        # units of the shift coming in here are in pixels (integer)

        nr = 2 * (img.shape[1] // 2)
        f1 = img[:,0:nr:2]
        f2 = img[:,1:nr+1:2]
        
        ## find optimal shift
        if auto:
            bestShift = None
            bestError = None
            #errs = []
            for shift in range(int(minShift), int(maxShift)):
                f2s = f2[:-shift] if shift > 0 else f2
                err1 = np.abs((f1[shift:, 1:]-f2s[:, 1:])**2).sum()
                err2 = np.abs((f1[shift:, 1:]-f2s[:, :-1])**2).sum()
                totErr = (err1+err2) / float(f1.shape[0]-shift)
                #errs.append(totErr)
                if totErr < bestError or bestError is None:
                    bestError = totErr
                    bestShift = shift
            #pg.plot(errs)
        else:
            bestShift = shift
        if bestShift is None: # nothing...
            return img, 0.
        ## reconstruct from shifted fields
        leftShift = bestShift // 2
        rightShift = int(leftShift + (bestShift % 2))
        if rightShift < 1:
            return img, 0
        decombed = np.zeros(img.shape, img.dtype)
        if leftShift > 0:
            decombed[:-leftShift, ::2] = img[leftShift:, ::2]
        else:
            decombed[:, ::2] = img[:, ::2]
        decombed[rightShift:, 1::2] = img[:-rightShift, 1::2]
        return decombed, bestShift
    

