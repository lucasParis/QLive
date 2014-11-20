#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from FxParent import *

class FxLowpass(FxParent):
    name = "lowpass"
    def __init__(self):
        FxParent.__init__(self)
        self.setName("lowpass")
        #ctrls
        self.ctrlFreq = FxParameter(name = "freq", value = 1000, min = 20, max = 20000, unit = "hz", exp = 2)
        self.addParameter(self.ctrlFreq)
        self.ctrlGain= FxParameter(name = "gain", value = 4, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.lp = ButLP(self.getInput(), freq=self.ctrlFreq, mul = self.dbValue)
        self.setOutput(self.lp)

class FxFreeVerb(FxParent):
    name = "FreeVerb"
    def __init__(self):
        FxParent.__init__(self)
        self.setName("FreeVerb")
        #ctrls
        self.size = FxParameter(name = "size", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.size)
        self.damp = FxParameter(name = "damp", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.damp)
        self.balance = FxParameter(name = "balance", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.balance)
        self.ctrlGain= FxParameter(name = "gain", value = 4, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.verb = Freeverb(self.getInput(),self.size, self.damp, self.balance, mul = self.dbValue)
        self.setOutput(self.verb)





class FxCreator:
    def __init__(self):
        self.fxs = []

        ### ADD FXs HERE
        self.fxs.append(FxLowpass)
        self.fxs.append(FxFreeVerb)



        self.buildNames()
        
    def buildNames(self):
        self.names = [fx.name for fx in self.fxs]

        
    def getNames(self):
        return self.names
        
    def createFx(self, index):
        if index < len(self.fxs):
            return self.fxs[index]()
            

class InputCreator:
    def __init__(self):
        self.classes = []

        ### ADD FXs HERE
        self.classes.append(FxLowpass)
        self.classes.append(FxFreeVerb)



        self.buildNames()
        
    def buildNames(self):
        self.names = [cla.name for cla in classes.fxs]

        
    def getNames(self):
        return self.names
        
    def createInput(self, index):
        if index < len(self.classes):
            return self.classes[index]()


if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            print FxCreator().getNames()
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()