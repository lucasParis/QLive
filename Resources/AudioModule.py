#!/usr/bin/python
# encoding: utf-8
import wx, os
from pyo64 import *
from constants import *
import QLiveLib

######## Types of control parameters available in the FxView window ########

# possible types: slider, choice box, path selection
class ParameterParent:
    def __init__(self, name="empty"):
        self.name = name

class SliderParameter(ParameterParent, PyoObject):
    TYPE = "slider"
    def __init__(self, name="empty", value=0, min=0, max=1, unit="hz", exp=1):
        ParameterParent.__init__(self, name=name)
        PyoObject.__init__(self)
        self.min = min
        self.max = max
        self.unit = unit
        self.exp = exp
        self.value = value
        self.time = 0.01
        self.audioValue = SigTo(value, self.time, init=value)
        self.call = None
        self._base_objs = self.audioValue.getBaseObjects()

    # add new function for setValueFromUI (temporarly resets interp time to 0.05)
    def setValue(self, value):# this should only be used for save dict and cues, rename to setSaveValue ?
        # get and set value as pair list [value, interTime]
        self.audioValue.time = value[1]
        self.time = value[1]
        self.audioValue.setValue(value[0])
        self.value = value[0]

    def getValue(self):# this should only be used for save dict and cues, rename to getSaveValue ?
        return [self.audioValue.value, self.time]
        
    def getParameterValue(self):
        return self.value

    def setParameterValue(self, value):
        if self.call is not None:
            self.call.stop()
        time = self.audioValue.time
        self.audioValue.time = 0.01
        self.audioValue.setValue(value)
        self.value = value
        self.call = CallAfter(self.postTimeSet, 0.005)
#        self.call.play()
#        
    def postTimeSet(self):#used when interp time is temporarly reset to 0.01 for gui
        print "after"
        self.audioValue.time = self.time

    def getInterpTime(self):
        return self.audioValue.time
        
    def setInterpTime(self, value):
        self.audioValue.time = value

######## Parent class for fxs and input boxes ########
class AudioModule(object):
    name = "empty"
    def __init__(self):
        self.parameters = []
        self.enable = True

        self.input = Sig([0] * NUM_CHNLS)
        self.preOutput = Sig([0] * NUM_CHNLS)
        self.ctrlDW = SliderParameter(name="DryWet", value=1, min=0, max=1, 
                                      unit="", exp=1)
        self.addParameter(self.ctrlDW)
        self.output = Selector([self.input, self.preOutput], self.ctrlDW)

    def setName(self, name):
        self.name = name
        
    def removeDryWet(self):
        del self.parameters[0]
        
    def addParameter(self, param):
        self.parameters.append(param)

    def setEnable(self, state):
        if state:
            self.enable = True
            self.setOutput(self.process)
        else:
            self.enable = False
            self.setOutput(self.input)

    def setInput(self, input):
        self.input.setValue(input)
        
    def getInput(self):
        return self.input
        
    def setOutput(self, out):
        self.preOutput.setValue(out)

    def getOutput(self):
        return self.output


######## Available effect modules ########
class FxNone(AudioModule):
    name = "None"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("")
        self.removeDryWet()
        self.process = self.getInput()
        self.setOutput(self.getInput())

class FxLowpass(AudioModule):
    name = "Lowpass"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("Lowpass")
        #ctrls
        self.ctrlFreq = SliderParameter(name = "freq", value = 1000, min = 20, max = 20000, unit = "hz", exp = 2)
        self.addParameter(self.ctrlFreq)
        self.ctrlQ = SliderParameter(name = "Q", value = 2, min = 0.1, max = 40, unit = "", exp = 1)
        self.addParameter(self.ctrlQ)
        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = Biquad(self.getInput(), freq=self.ctrlFreq,q = self.ctrlQ, mul = self.dbValue)
        self.setOutput(self.process)

class FxHighpass(AudioModule):
    name = "Highpass"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("Highpass")
        #ctrls
        self.ctrlFreq = SliderParameter(name = "freq", value = 1000, min = 20, max = 20000, unit = "hz", exp = 2)
        self.addParameter(self.ctrlFreq)
        self.ctrlQ = SliderParameter(name = "Q", value = 2, min = 0.1, max = 40, unit = "", exp = 1)
        self.addParameter(self.ctrlQ)
        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = Biquad(self.getInput(), freq=self.ctrlFreq,q = self.ctrlQ, mul = self.dbValue, type = 1)
        self.setOutput(self.process)

class FxFreeVerb(AudioModule):
    name = "FreeVerb"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("FreeVerb")
        #ctrls
        self.size = SliderParameter(name = "size", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.size)
        self.damp = SliderParameter(name = "damp", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.damp)

        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = Freeverb(self.getInput(),self.size, self.damp, 1, mul = self.dbValue)
        self.setOutput(self.process)

class FxStereoVerb(AudioModule):
    name = "StereoVerb"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("StereoVerb")
        #ctrls
        self.inputPosition = SliderParameter(name = "pan", value = 0.5, min = 0, max = 1, unit = "")
        self.addParameter(self.inputPosition)
        self.time = SliderParameter(name = "time", value = 1, min = 0.05, max = 30, unit = "second")
        self.addParameter(self.time)

        self.cutoff = SliderParameter(name = "cutoff", value = 5000, min = 20, max = 20000, unit = "db")
        self.addParameter(self.cutoff)
        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = STRev(self.getInput(), inpos=self.inputPosition, revtime=self.time, cutoff=self.cutoff, bal=1, mul=self.dbValue)
        self.setOutput(self.process)

class FxDisto(AudioModule):
    name = "Distortion"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("Distortion")
        #ctrls
        self.drive = SliderParameter(name = "drive", value = 0.5, min = 0, max = 1, unit = "", exp = 2)
        self.addParameter(self.drive)
        self.slope = SliderParameter(name = "slope", value = 0.5, min = 0, max = 1, unit = "", exp = 2)
        self.addParameter(self.slope)
        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = Disto(self.getInput(), drive=self.drive, slope=self.slope, mul = self.dbValue)
        self.setOutput(self.process)

class FxDelay(AudioModule):
    name = "Delay"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("Delay")
        #ctrls
        self.time = SliderParameter(name = "time", value = 0.5, min = 0.01, max = 3, unit = "")
        self.addParameter(self.time)
        self.feedback = SliderParameter(name = "feedback", value = 0.5, min = 0, max = 0.999, unit = "", exp = 2)
        self.addParameter(self.feedback)
        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = Delay(self.getInput(), delay=self.time, feedback=self.feedback, maxdelay=3, mul=self.dbValue)
        self.setOutput(self.process)

class FxCompressor(AudioModule):
    name = "Compressor"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("Compressor")
        #ctrls
        self.tresh = SliderParameter(name = "tresh", value = -10, min = -90, max = 12, unit = "db")
        self.addParameter(self.tresh)
        self.ratio = SliderParameter(name = "ratio", value = 2, min = 1, max = 100, unit = "", exp = 2)
        self.addParameter(self.ratio)
        self.attack= SliderParameter(name = "attack", value = 0.01, min = 0, max = 1, unit = "s", exp = 1)
        self.addParameter(self.attack)
        self.decay = SliderParameter(name = "decay", value = 0.1, min = 0, max = 1, unit = "s", exp = 1)
        self.addParameter(self.decay)
        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = Compress(self.getInput(), thresh=self.tresh, ratio=self.ratio, risetime=self.attack, falltime=self.decay, lookahead=5.00, knee=0, mul = self.dbValue)
        self.setOutput(self.process)

class FxFreqShift(AudioModule):
    name = "FreqShift"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("FreqShift")
        #ctrls
        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        self.ctrlShift= SliderParameter(name = "shift", value = 0, min = -5000, max = 5000, unit = "hz", exp = 1)
        self.addParameter(self.ctrlShift)
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = FreqShift(self.getInput(), self.ctrlShift, mul = self.dbValue)
        self.setOutput(self.process)

class FxHarmonizer(AudioModule):
    name = "Harmonizer"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("Harmonizer")
        #ctrls
        self.ctrlGain= SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        self.ctrlTranspo= SliderParameter(name = "transpo", value = 0, min = -24, max = 24, unit = "", exp = 1)
        self.addParameter(self.ctrlTranspo)
        self.ctrlFeed= SliderParameter(name = "feedback", value = 0, min = 0, max = 1, unit = "", exp = 1)
        self.addParameter(self.ctrlFeed)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = Harmonizer(self.getInput(), self.ctrlTranspo, self.ctrlFeed, mul = self.dbValue)
        self.setOutput(self.process)

class FxMonoOut(AudioModule):
    name = "MonoOut"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("MonoOut")
        self.removeDryWet()
        #ctrls
        self.ctrlGain = SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = Sig(self.getInput().mix(1), mul = self.dbValue)
        self.setOutput(self.process)

class FxStereoOut(AudioModule):
    name = "StereoOut"
    def __init__(self):
        AudioModule.__init__(self)
        self.setName("StereoOut")
        self.removeDryWet()
        #ctrls
        self.ctrlGain = SliderParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        self.ctrlPan = SliderParameter(name = "pan", value = 0.5, min = 0, max = 1, unit = "", exp = 1)
        self.addParameter(self.ctrlPan)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.process = SPan(self.getInput().mix(2), 2, self.ctrlPan, mul = self.dbValue)
        self.setOutput(self.process)

######## Available input modules ########
class InputIn(AudioModule):
    name = "input"
    def __init__(self):
        AudioModule.__init__(self)
        self.removeDryWet()
        self.setName("input")

        #ctrls
        self.ctrlGain = SliderParameter(name="gain", value=0, min=-90, max=24, 
                                        unit="db", exp=1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.amp = Sig(self.input, mul = self.dbValue)
        self.setOutput(self.amp)
        