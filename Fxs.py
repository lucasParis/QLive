#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from ModuleParent import *

class FxLowpass(ModuleParent):
    name = "Lowpass"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("Lowpass")
        #ctrls
        self.ctrlFreq = ModuleParameter(name = "freq", value = 1000, min = 20, max = 20000, unit = "hz", exp = 2)
        self.addParameter(self.ctrlFreq)
        self.ctrlQ = ModuleParameter(name = "Q", value = 2, min = 0.1, max = 40, unit = "", exp = 1)
        self.addParameter(self.ctrlQ)
        self.ctrlGain= ModuleParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.lp = Biquad(self.getInput(), freq=self.ctrlFreq,q = self.ctrlQ, mul = self.dbValue)
        self.setOutput(self.lp)

class FxHighpass(ModuleParent):
    name = "Highpass"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("Highpass")
        #ctrls
        self.ctrlFreq = ModuleParameter(name = "freq", value = 1000, min = 20, max = 20000, unit = "hz", exp = 2)
        self.addParameter(self.ctrlFreq)
        self.ctrlQ = ModuleParameter(name = "Q", value = 2, min = 0.1, max = 40, unit = "", exp = 1)
        self.addParameter(self.ctrlQ)
        self.ctrlGain= ModuleParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.lp = Biquad(self.getInput(), freq=self.ctrlFreq,q = self.ctrlQ, mul = self.dbValue, type = 1)
        self.setOutput(self.lp)

class FxFreeVerb(ModuleParent):
    name = "FreeVerb"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("FreeVerb")
        #ctrls
        self.size = ModuleParameter(name = "size", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.size)
        self.damp = ModuleParameter(name = "damp", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.damp)
        self.balance = ModuleParameter(name = "balance", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.balance)
        self.ctrlGain= ModuleParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.verb = Freeverb(self.getInput(),self.size, self.damp, self.balance, mul = self.dbValue)
        self.setOutput(self.verb)



class FxStereoVerb(ModuleParent):
    name = "StereoVerb"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("StereoVerb")
        #ctrls
        self.inputPosition = ModuleParameter(name = "pan", value = 0.5, min = 0, max = 1, unit = "")
        self.addParameter(self.inputPosition)
        self.time = ModuleParameter(name = "time", value = 1, min = 0.05, max = 30, unit = "second")
        self.addParameter(self.time)
        self.balance = ModuleParameter(name = "balance", value = 0.5, min = 0, max = 1, unit = "hz", exp = 2)
        self.addParameter(self.balance)
#        self.roomSize = ModuleParameter(name = "room size", value = 0.5, min = 0.25, max = 4, unit = "")
#        self.addParameter(self.roomSize)
#        self.reflection = ModuleParameter(name = "reflection", value = -3, min = -90, max = 12, unit = "db")
#        self.addParameter(self.reflection)
        self.cutoff = ModuleParameter(name = "cutoff", value = 5000, min = 20, max = 20000, unit = "db")
        self.addParameter(self.cutoff)
        self.ctrlGain= ModuleParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.verb = STRev(self.getInput(), inpos=self.inputPosition, revtime=self.time, cutoff=self.cutoff, bal=self.balance, mul=self.ctrlGain)
        self.setOutput(self.verb)

class FxDisto(ModuleParent):
    name = "Distortion"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("Distortion")
        #ctrls
        self.drive = ModuleParameter(name = "drive", value = 0.5, min = 0, max = 1, unit = "", exp = 2)
        self.addParameter(self.drive)
        self.slope = ModuleParameter(name = "slope", value = 0.5, min = 0, max = 1, unit = "", exp = 2)
        self.addParameter(self.slope)
        self.ctrlGain= ModuleParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.disto = Disto(self.getInput(), drive=self.drive, slope=self.slope, mul = self.dbValue)
        self.setOutput(self.disto)

class FxDelay(ModuleParent):
    name = "Delay"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("Delay")
        #ctrls
        self.time = ModuleParameter(name = "time", value = 0.5, min = 0.01, max = 3, unit = "")
        self.addParameter(self.time)
        self.feedback = ModuleParameter(name = "feedback", value = 0.5, min = 0, max = 0.999, unit = "", exp = 2)
        self.addParameter(self.feedback)
        self.ctrlGain= ModuleParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.delay = Delay(self.getInput(), delay=self.time, feedback=self.feedback, maxdelay=3, mul=self.dbValue)
        self.setOutput(self.delay)

class FxCompressor(ModuleParent):
    name = "Compressor"
    def __init__(self):
        ModuleParent.__init__(self)
        self.setName("Compressor")
        #ctrls
        self.tresh = ModuleParameter(name = "tresh", value = -10, min = -90, max = 12, unit = "db")
        self.addParameter(self.tresh)
        self.ratio = ModuleParameter(name = "ratio", value = 2, min = 1, max = 100, unit = "", exp = 2)
        self.addParameter(self.ratio)
        self.attack= ModuleParameter(name = "attack", value = 0.01, min = 0, max = 1, unit = "s", exp = 1)
        self.addParameter(self.attack)
        self.decay = ModuleParameter(name = "decay", value = 0.1, min = 0, max = 1, unit = "s", exp = 1)
        self.addParameter(self.decay)
        self.ctrlGain= ModuleParameter(name = "gain", value = 0, min = -90, max = 24, unit = "db", exp = 1)
        self.addParameter(self.ctrlGain)
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.comp = Compress(self.getInput(), thresh=self.tresh, ratio=self.ratio, risetime=self.attack, falltime=self.decay, lookahead=5.00, knee=0, mul = self.dbValue)
        self.setOutput(self.comp)




class FxCreator:
    def __init__(self):
        self.fxs = []

        ### ADD FXs HERE
        self.fxs.append(FxLowpass)
        self.fxs.append(FxHighpass)
        self.fxs.append(FxFreeVerb)
        self.fxs.append(FxStereoVerb)
        self.fxs.append(FxDisto)
        self.fxs.append(FxDelay)
        self.fxs.append(FxCompressor)
        
        self.buildNames()
        
    def buildNames(self):
        self.names = [fx.name for fx in self.fxs]

        
    def getNames(self):
        return self.names
        
    def create(self, index):
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
        
    def create(self, index):
        if index < len(self.classes):
            return self.classes[index]()


if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s = Server().boot()
            self.effect = FxCreator().createFx(0)
#            print self.effect.getSaveDict()
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()