#!/usr/bin/python
# encoding: utf-8

import wx
from pyo import *
from FxParent import FxParameter


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