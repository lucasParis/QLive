#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *

### All these classes should be in the same file as Fxs and Inputs

### This one should inherits from PyoObject
class ParameterParent:
    def __init__(self, name = "empty"):
#        PyoObject.__init__(self)

        self.name = name
#        self.min = min
#        self.max = max
#        self.unit = unit
#        self.exp = exp
#        self.value = value
        self.type = "slider" # possible types: slider, choice box, path selection
#        self.audioValue = SigTo(value,0.05, init = value)

#        self._base_objs = self.audioValue.getBaseObjects()

class SliderParameter(ParameterParent, PyoObject):
    def __init__(self, name = "empty", value = 0, min = 0, max = 1, unit = "hz", exp = 1):
        ParameterParent.__init__(self, name = name)
        PyoObject.__init__(self)

#        self.name = name
        self.min = min
        self.max = max
        self.unit = unit
        self.exp = exp
        self.value = value
        self.type = "slider" # possible types: slider, choice box, path selection
        self.audioValue = SigTo(value,0.05, init = value)

        self._base_objs = self.audioValue.getBaseObjects()

    def setValue(self, value):
        self.audioValue.setValue(value)
        self.value = value

    def getValue(self):
        return self.value
        
class ButtonParameter(ParameterParent):
    def __init__(self, name = "empty"):
        ParameterParent.__init__(self, name = name)
        self.type = "button"
        self.callback = None
        self.path = ""

#        self._base_objs = self.audioValue.getBaseObjects()
    def setCallback(self, function):
        self.callback = function
        
    def setValue(self, value):
#        self.audioValue.setValue(value)
        self.path = value
        if self.callback != None:
            self.callback()

    def getValue(self):
        return self.path

class ToggleParameter(ParameterParent):
    def __init__(self, name = "empty"):
        ParameterParent.__init__(self, name = name)
        self.type = "toggle"
        self.value = 0
        self.callback = None

#        self._base_objs = self.audioValue.getBaseObjects()
    def setCallback(self, function):
        self.callback = function
        
    def setValue(self, value):
#        self.audioValue.setValue(value)
        self.value = value
        print "toggle value", value
        if self.callback != None:
            self.callback(value)

    def getValue(self):
        return self.value
        
class PathParameter(ParameterParent):
    def __init__(self, name = "empty"):
        ParameterParent.__init__(self, name = name)
        self.path = None
        self.type = "path"
        self.callback = None
#        self.name = name
#        self.min = min
#        self.max = max
#        self.unit = unit
#        self.exp = exp
#        self.value = value
#        self.type = "slider" # possible types: slider, choice box, path selection
#        self.audioValue = SigTo(value,0.05, init = value)

#        self._base_objs = self.audioValue.getBaseObjects()
    def setCallback(self, function):
        self.callback = function
        
    def setValue(self, value):
#        self.audioValue.setValue(value)
        self.path = value
        if self.callback != None:
            self.callback(self.path)

    def getValue(self):
        return self.path

class ModuleParent(object):
    name = "empty"
    def __init__(self):
        self.parameters = []

        self.input = Sig([0,0])
        self.preOutput = Sig([0,0])
        self.ctrlDW = SliderParameter(name = "DryWet", value = 1, min = 0, max = 1, unit = "", exp = 1)
        self.addParameter(self.ctrlDW)
        self.output = Selector([self.input, self.preOutput], self.ctrlDW)
        self.bypass = False
        self.name = "empty"
        self.cues = []
        self.currentCue = 0

    def setName(self, name):
        self.name = name
        
    def removeDryWet(self):
        del self.parameters[0]
        
    def addParameter(self, param):
        self.parameters.append(param)

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
