#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from MixerPanel import *
#from FxBox import *
#import  wx.lib.scrolledpanel as scrolled
class AudioChannel:
    def __init__(self):
        self.input = Sig(0)
        self.inVolume = SigTo(0, init = 0)
        self.inDB = DBToA(self.inVolume)
        self.out = Sig(self.input, mul = self.inDB)
        self.ampOut = PeakAmp(self.out)
        
    def setInput(self, input):
        self.input.setValue(input)
        
    def getOutput(self):
        return self.out
        
    def setVolume(self, value):
        self.inVolume.setValue(value)
        
    def setAmpCallback(self, call):
        self.ampOut.function = call

class AudioMixer:
    def __init__(self):
#        self.inVolumes = Sig([0 for i in range(2)])
#        self.inDb = DBToA(self.inVolumes)
#        
#        self.outVolumes = Sig([0 for i in range(2)])
#        self.outDb = DBToA(self.outVolumes)
        self.inChannels = []
        for i in range(2):
            channel = AudioChannel()
            channel.setInput(Input(i))
            self.inChannels.append(channel)
        
        self.outChannels = []
        for i in range(2):
            channel = AudioChannel()
            channel.getOutput().out()
            self.outChannels.append(channel)
            
    def getInputChannel(self, index):
        if index < len(self.inChannels):
            return self.inChannels[index]
        else:
            return None

    def getOutputChannel(self, index):
        if index < len(self.outChannels):
            return self.outChannels[index]
        else:
            return None

        
if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s= Server().boot()
            self.s.start()
            self.mixer = AudioMixer()
            self.panel = MixerPanel(self, self.mixer)
#            self.fxTrack = FxTrack(self)


    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()