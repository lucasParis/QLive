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

        self.ctrlGain= SliderParameter(name = "gain", value = 4, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.amp = Sig(self.input, mul = self.dbValue)
        self.setOutput(self.amp)

class Soundfile(ModuleParent):
    name = "Soundfile"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("Soundfile")
        #ctrls

        self.ctrlGain= SliderParameter(name = "gain", value = 4, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        self.path= PathParameter(name = "gain")
        self.addParameter(self.path)
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.amp = Sig(self.input, mul = self.dbValue)
        self.setOutput(self.amp)



class InputCreator:
    def __init__(self):
        self.classes = []

        ### ADD FXs HERE
        self.classes.append(InputIn)
        self.classes.append(Soundfile)



        self.buildNames()
        
    def buildNames(self):
        self.names = [cla.name for cla in self.classes]

        
    def getNames(self):
        return self.names
        
    def create(self, index):
        if index < len(self.classes):
            return self.classes[index]()


if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s = Server().boot()
            self.s.start()
            print InputCreator().getNames()
            self.input = InputCreator().create(0)
            self.input.getOutput().out()
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()