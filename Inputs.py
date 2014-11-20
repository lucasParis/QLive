#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from ModuleParent import *


class InputIn(ModuleParent):
    name = "input"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("input")
        #ctrls
#        self.ctrlFreq = ModuleParameter(name = "freq", value = 1000, min = 20, max = 20000, unit = "hz", exp = 2)
#        self.addParameter(self.ctrlFreq)
        self.ctrlGain= ModuleParameter(name = "gain", value = 4, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.amp = Sig(self.getInput(),mul = self.dbValue)
        self.setOutput(self.amp)



class InputCreator:
    def __init__(self):
        self.classes = []

        ### ADD FXs HERE
        self.classes.append(InputIn)
#        self.classes.append(FxFreeVerb)



        self.buildNames()
        
    def buildNames(self):
        self.names = [cla.name for cla in self.classes]

        
    def getNames(self):
        return self.names
        
    def createInput(self, index):
        if index < len(self.classes):
            return self.classes[index]()


if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            print InputCreator().getNames()
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()