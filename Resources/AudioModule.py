#!/usr/bin/python
# encoding: utf-8
import wx, os
from constants import *
from pyo import *

######## Types of control parameters available in the FxView window ########

# possible types: slider, choice box, path selection
class ParameterParent:
    def __init__(self, name="empty"):
        # What is the difference between name and type?
        self.name = name
        self.type = "slider"

class SliderParameter(ParameterParent, PyoObject):
    def __init__(self, name="empty", value=0, min=0, max=1, unit="hz", exp=1):
        ParameterParent.__init__(self, name=name)
        PyoObject.__init__(self)
        self.type = "slider"
        self.min = min
        self.max = max
        self.unit = unit
        self.exp = exp
        self.value = value
        self.audioValue = SigTo(value, 0.05, init=value)
        self._base_objs = self.audioValue.getBaseObjects()

    def setValue(self, value):
        self.audioValue.setValue(value)
        self.value = value

    def getValue(self):
        return self.value
        
class ButtonParameter(ParameterParent):
    def __init__(self, name="empty"):
        ParameterParent.__init__(self, name=name)
        self.type = "button"
        self.callback = None
        self.path = "" # Is there really a path in the button widget?

    def setCallback(self, function):
        self.callback = function
        
    def setValue(self, value):
        self.path = value
        if self.callback != None:
            self.callback()

    def getValue(self):
        return self.path

class ToggleParameter(ParameterParent):
    def __init__(self, name="empty"):
        ParameterParent.__init__(self, name=name)
        self.type = "toggle"
        self.value = 0
        self.callback = None

    def setCallback(self, function):
        self.callback = function
        
    def setValue(self, value):
        self.value = value
        if self.callback != None:
            self.callback(value)

    def getValue(self):
        return self.value
        
class PathParameter(ParameterParent):
    def __init__(self, name="empty"):
        ParameterParent.__init__(self, name=name)
        self.type = "path"
        self.path = ""
        self.callback = None

    def setCallback(self, function):
        self.callback = function
        
    def setValue(self, value):
        self.path = value
        if self.callback != None:
            self.callback(self.path)

    def getValue(self):
        return self.path

######## Parent class for fxs and input boxes ########
class AudioModule(object):
    name = "empty"
    def __init__(self):
        self.name = "empty"
        self.parameters = []
        self.bypass = False
        self.cues = []
        self.currentCue = 0

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
            self.setOutput(self.process)
        else:
            self.setOutput(self.input)

    def setInput(self, input):
        self.input.setValue(input)
        
    def getInput(self):
        return self.input
        
    def setOutput(self, out):
        self.preOutput.setValue(out)

    def getOutput(self):
        return self.output

    def getSaveDict(self):
        if len(self.cues) <= self.currentCue:
            self.appendCurrentState()
        else:
            self.saveCurrentState(self.currentCue)
        dict = {'values': self.cues}
        return dict
        
    def setSaveDict(self, saveDict):
        self.cues = saveDict['values']
        self.currentCue = 0
        self.loadingCurrentCue()

    def saveCurrentState(self, cue):
        self.cues[cue] = [param.getValue() for param in self.parameters]

    def appendCurrentState(self):
        l = [param.getValue() for param in self.parameters]
        self.cues.append(l)

    def loadingCurrentCue(self):
        for i, param in enumerate(self.parameters):
            param.setValue(self.cues[self.currentCue][i])
        
    def cueEvent(self, eventDict):
        if eventDict["type"] == 'newCue':
            # save current state
            if len(self.cues) == 0:
                self.appendCurrentState()
            else:
                self.saveCurrentState(self.currentCue)
            # append a copy of the current state
            self.appendCurrentState()
            self.currentCue = eventDict["totalCues"] - 1
        elif eventDict["type"] == 'cueSelect':
            # save current state
            self.saveCurrentState(self.currentCue)
            # load the selected cue
            self.currentCue = eventDict["selectedCue"]
            self.loadingCurrentCue()
        elif eventDict["type"] == 'deleteCue':
            # remove the current cue
            self.cues.pop(eventDict["deletedCue"])
            # load the new selected cue
            self.currentCue = eventDict["currentCue"]
            self.loadingCurrentCue()

    def initCues(self, numberOfCues, currentCue):
        for i in range(numberOfCues):
            l = [param.getValue() for param in self.parameters]
            self.cues.append(l)
        self.currentCue = currentCue

######## Available effect modules ########
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

class FxCreator:
    def __init__(self):
        self.fxs = []

        ### Add FXs here
        self.fxs.append(FxLowpass)
        self.fxs.append(FxHighpass)
        self.fxs.append(FxFreeVerb)
        self.fxs.append(FxStereoVerb)
        self.fxs.append(FxDisto)
        self.fxs.append(FxDelay)
        self.fxs.append(FxCompressor)
        self.fxs.append(FxFreqShift)
        self.fxs.append(FxHarmonizer)

        self.buildNames()
        
    def buildNames(self):
        self.names = [fx.name for fx in self.fxs]

    def getNames(self):
        return self.names
        
    def create(self, index):
        if index < len(self.fxs):
            return self.fxs[index]()

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

class Soundfile(AudioModule):
    name = "Soundfile"
    def __init__(self):
        AudioModule.__init__(self)
        self.removeDryWet()
        self.setName("Soundfile")
                
        #ctrls
        self.path = PathParameter(name = "path")
        self.addParameter(self.path)
        
        self.speed = SliderParameter(name="speed", value=1, min=0.25, max=4, unit="")
        self.addParameter(self.speed)
        
        self.ctrlGain = SliderParameter(name="gain", value=0, min=-90, max=24, 
                                        unit="db", exp=1)
        self.addParameter(self.ctrlGain)

        self.playButton = ToggleParameter(name="play")
        self.addParameter(self.playButton)

        self.loopButton = ToggleParameter(name = "loop")
        self.addParameter(self.loopButton)

        #audio
        filepath = os.path.join(SOUNDS_PATH, "silence.wav")
        self.sfPlayer = SfPlayer(filepath, speed=self.speed, loop=False, 
                                 offset=0, interp=2, mul=1, add=0).stop()
        self.path.setCallback(self.loadPath)
        self.playButton.setCallback(self.setPlay)
        self.loopButton.setCallback(self.setLoop)

        self.dbValue = DBToA(self.ctrlGain)
        self.amp = Sig(self.sfPlayer, mul = self.dbValue)
        self.setOutput(self.amp)

    def loadPath(self, path):
        self.sfPlayer.setPath(path)

    def setPlay(self, state):
        if state:
            self.sfPlayer.play()
        else:
            self.sfPlayer.stop()

    def setLoop(self, onOff):
        self.sfPlayer.setLoop(onOff)
        
class InputCreator:
    def __init__(self):
        self.classes = []

        ### Add inputs here
        self.classes.append(InputIn)
        self.classes.append(Soundfile)

        self.buildNames()
        
    def buildNames(self):
        self.names = [cls.name for cls in self.classes]
        
    def getNames(self):
        return self.names
        
    def create(self, index):
        if index < len(self.classes):
            return self.classes[index]()
