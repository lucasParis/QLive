#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
# 
class ModuleParameter(PyoObject):
    def __init__(self, name = "empty", value = 0, min = 0, max = 1, unit = "hz", exp = 1):
        PyoObject.__init__(self)

        self.name = name
        self.min = min
        self.max = max
        self.unit = unit
        self.exp = exp
        self.value = value
        self.type = "slider" # possible types: slider, choice box, path selection
        self.audioValue = SigTo(value,1, init = value)

        self._base_objs = self.audioValue.getBaseObjects()

    def setValue(self, value):
#        print "seting"
        self.audioValue.setValue(value)
        self.value = value
#        print value
        
#    def setFromFloat(self, float):
#        self.value = float**self.exp*(self.max-self.min)+self.min
#        self.audioValue = self.value

    def getValue(self):
        return self.value

class ModuleParent(object):
    name = "empty"
    def __init__(self):
        self.input = Sig([0,0])
        self.output = Sig([0,0])
        self.bypass = False
        self.name = "empty"
        self.parameters = [] #append parameters here
        self.cues = []
        self.currentCue = 0
        pass
        
    def addParameter(self, param):
        self.parameters.append(param)
        
    def getInput(self):
        return self.input
        
    def setOutput(self, out):
        self.output.setValue(out)
        
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
#        if len(saveDict['values']) == len(self.parameters):
#            for i, value in enumerate(saveDict['values']):
#                self.parameters[i].setValue(value)
#        else:
#            print "error in moduleParent in setSaveDict"
            
    def cueEvent(self, eventDict):
        if eventDict["type"] == 'newCue':
#            print "audio got new cue"
#            print eventDict["currentCue"], eventDict["totalCues"]
            # on first cue save populate first cue
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