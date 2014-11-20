#!/usr/bin/python
# encoding: utf-8

import wx
from pyo import *
from FxParent import FxParameter

#class FxParameter(PyoObject):
#    def __init__(self, name = "empty", value = 0, min = 0, max = 1, unit = "hz", exp = 1):
#        PyoObject.__init__(self)

#        self.name = name
#        self.min = min
#        self.max = max
#        self.unit = unit
#        self.exp = exp
#        self.value = value
#        
#        self.audioValue = Sig(value)

#        self._base_objs = self.audioValue.getBaseObjects()

#    def setValue(self, value):
#        self.audioValue.setValue(value)
#        print value
#        
#    def setFromFloat(self, float):
#        self.value = float**self.exp*(self.max-self.min)+self.min
#        self.audioValue = self.value

#    def setModelParameter(self, param):
#        # save model parameter? 
#        # register a callback on model parameter?
#        # 
#        pass

class InputParent(object):
    name = "empty"
    def __init__(self):
        self.input = Sig([0,0])
        self.output = Sig([0,0])
        self.bypass = False
        self.name = "empty"
        self.parameters = [] #append parameters here
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
        
    def makeModel(self):
        #should construct and return a model from it's paramaters
        return None
        
    def setName(self, name_):
        self.name = name_



if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s = Server().boot()
            self.s.start()
            self.fx = FxParent()
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()