# -*- coding: utf-8 -*-
from lib.drivers.nidaq import NIDAQ, SuperTask
from lib.devices.Device import *
import threading, time, traceback, sys
from protoGUI import *
from numpy import byte
from lib.util.debug import *

class NiDAQ(Device):
    def __init__(self, dm, config, name):
        Device.__init__(self, dm, config, name)
        ## make local copy of device handle
        self.n = NIDAQ
        print "Created NiDAQ handle, devices are %s" % repr(self.n.listDevices())
        self.lock = threading.RLock()
    
    def createTask(self, cmd):
        return Task(self, cmd)
        
    def setChannelValue(self, chan, value, block=False):
        self.reserve(block=block)
        #print "Setting channel %s to %f" % (chan, value)
        try:
            if 'ao' in chan:
                self.n.writeAnalogSample(chan, value)
            else:
                if value is True or value == 1:
                    value = 0xFFFFFFFF
                else:
                    value = 0
                self.n.writeDigitalSample(chan, value)
        except:
            printExc("Error while setting channel %s to %s:" % (chan, str(value)))
        finally:
            self.release()
        
    def getChannelValue(self, chan):
        self.reserve(block=True)
        #print "Setting channel %s to %f" % (chan, value)
        try:
            if 'ai' in chan:
                val = self.n.readAnalogSample(chan)
            else:
                val = self.n.readDigitalSample(chan)
                if val <= 0:
                    val = 0
                else:
                    val = 1
        except:
            printExc("Error while setting channel %s to %s:" % (chan, str(value)))
            raise
        finally:
            self.release()
        return val
        
    def protocolInterface(self, prot):
        return NiDAQProto(self, prot)
        
    #def listTriggerPorts(self):
        #p = self.n.listDILines()
        #return [x for x in p if 'PFI' in x]

class Task(DeviceTask):
    def __init__(self, dev, cmd):
        DeviceTask.__init__(self, dev, cmd)
        
        ## get DAQ device
        #daq = self.devm.getDevice(...)
        
        
        ## Create supertask from nidaq driver
        self.st = SuperTask(self.dev.n)
        
    def configure(self, tasks, startOrder):
        #print "daq configure", tasks
        ## Request to all devices that they create the channels they use on this task
        for dName in tasks:
            #print "Requesting %s create channels" % dName
            if hasattr(tasks[dName], 'createChannels'):
                tasks[dName].createChannels(self)
        
        ## If no devices requested buffered operations, then do not configure clock.
        ## This might eventually cause some triggering issues..
        if not self.st.hasTasks():
            return
        
        ## Determine the sample clock source, configure tasks
        self.st.configureClocks(rate=self.cmd['rate'], nPts=self.cmd['numPts'])

        ## Determine how the protocol will be triggered
        if 'triggerChan' in self.cmd:
            self.st.setTrigger(trigger)
        elif 'triggerDevice' in self.cmd:
            tDev = self.dev.dm.getDevice(self.cmd['triggerDevice'])
            self.st.setTrigger(tDev.getTriggerChannel(self.dev.name))
        #print "daq configure complete"
        
    def addChannel(self, *args, **kwargs):
        #print "Adding channel:", args
        return self.st.addChannel(*args, **kwargs)
        
    def setWaveform(self, *args, **kwargs):
        return self.st.setWaveform(*args, **kwargs)
        
    def start(self):
        if self.st.hasTasks():
            self.st.start()
        
    def isDone(self):
        if self.st.hasTasks():
            return self.st.isDone()
        else:
            return True
        
        
    def stop(self, wait=False, abort=False):
        if self.st.hasTasks():
            #print "stopping ST..."
            self.st.stop(wait=wait, abort=abort)
            #print "   ST stopped"
        
    def getResult(self):
        ## Results should be collected by individual devices using getData
        return None
        
    def storeResult(self, dirHandle):
        pass
        
    def getData(self, channel):
        """Return the data collected for a specific channel. Return looks like:
        {
          'data': ndarray,
          'info': {'rate': xx, 'numPts': xx, ...}
        }
        """
        
        res = self.st.getResult(channel)
        if 'downsample' in self.cmd:
            ds = self.cmd['downsample']
        else:
            ds = 1
            
        if res['info']['type'] in ['di', 'do']:
            res['data'] = (res['data'] > 0).astype(byte)
            
        if ds > 1:
            data = res['data']
            newLen = int(data.shape[0] / ds) * ds
            data = data[:newLen]
            data.shape = (data.shape[0]/ds, ds)
            if res['info']['type'] in ['di', 'do']:
                data = data.mean(axis=1).round().astype(byte)
            else:
                data = data.mean(axis=1)
            res['data'] = data
            res['info']['numPts'] = data.shape[0]
            res['info']['downsampling'] = ds
            res['info']['rate'] = res['info']['rate'] / ds
                
        return res
        
    def devName(self):
        return self.dev.name