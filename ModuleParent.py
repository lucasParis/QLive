#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
# 

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

    def setValue(self, value):
        pass
#        self.audioValue.setValue(value)
#        self.value = value


    def getValue(self):
        pass
#        return self.value

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

#        self._base_objs = self.audioValue.getBaseObjects()
    def setCallback(self, function):
        self.callback = function
        
    def setValue(self, value):
#        self.audioValue.setValue(value)
#        self.path = value
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
        return self.path
        
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
        self.parameters = [] #append parameters here

        self.input = Sig([0,0])
        self.preOutput = Sig([0,0])
        self.ctrlDW = SliderParameter(name = "DryWet", value = 1, min = 0, max = 1, unit = "", exp = 1)
        self.addParameter(self.ctrlDW)
        self.output = Selector([self.input, self.preOutput], self.ctrlDW)
        self.bypass = False
        self.name = "empty"
        self.cues = []
        self.currentCue = 0
        
    def removeDryWet(self):
        del self.parameters[0]
        
    def addParameter(self, param):
        self.parameters.append(param)
        
    def getInput(self):
        return self.input
        
    def setOutput(self, out):
        self.preOutput.setValue(out)
        
    def setInput(self, in_):
        self.input.setValue(in_)
        
    def getOutput(self):
        return self.output
        
    def setName(self, name_):
        self.name = name_

    def getSaveDict(self):
        # save current
        list = []
        for i,  param in enumerate(self.parameters):
            list.append(param.getValue())
        self.cues[self.currentCue] = list
        
        #into dict
        dict = {'values': self.cues}
        return dict
        
    def setSaveDict(self, saveDict):
        self.cues = saveDict['values']
                    # in with the new
        self.currentCue = 0
        for i,  param in enumerate(self.parameters):
            param.setValue(self.cues[int(self.currentCue)][i])

            
    def cueEvent(self, eventDict):
        if eventDict["type"] == 'newCue':
            if len(self.cues) == 0:
                list = []
                for i,  param in enumerate(self.parameters): 
                    list.append(param.getValue())
                self.cues.append(list)

            #creating new Cue
            list = []
            for i,  param in enumerate(self.parameters):
                list.append(param.getValue())
            self.cues.append(list)
            self.currentCue = eventDict["totalCues"]
            
        elif eventDict["type"] == 'cueSelect':

            # saving current parameters
            list = []
            for i,  param in enumerate(self.parameters):
                list.append(param.getValue())
            self.cues[self.currentCue] = list
            
            # in with the new
            self.currentCue = eventDict["selectedCue"]
            for i,  param in enumerate(self.parameters):
                param.setValue(self.cues[int(self.currentCue)][i])
            

    def initCues(self, numberOfCues, currentCue):
        for i in range(numberOfCues):
            list = []
            for j,  param in enumerate(self.parameters):
                list.append(param.getValue())
            self.cues.append(list)
        self.currentCue = currentCue
        
    def loadCue(self, cue):
        pass
        # only save on cue change (and save) before changing
        
#        list = []
#        for i, param in enumerate(self.parameters):
#            list.append(param.getValue())
#        self.currentCue = cue
        
    def copyCue(self, cueToCopy):
        # need to know: current cue, max cues...
        pass
                  
if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s = Server().boot()
            self.s.start()
            self.module = ModuleParent()
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()
    

    app.MainLoop()