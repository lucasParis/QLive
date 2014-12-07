#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *
import  wx.lib.scrolledpanel as scrolled
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR, VuMeter
from AudioMixer import *

class MixerPanel(wx.Panel):
    def __init__(self, parent, audioMixer):
        wx.Panel.__init__(self, parent, size = (800,200))
        self.parent = parent
        self.audioMixer = audioMixer
        self.SetBackgroundColour(BACKGROUND_COLOUR)

        self.inputSliders = []
        self.outputSliders = []
        self.inputMeters = []
        self.outputMeters = []
        
        ### INPUT SECTION
        inputBox = wx.BoxSizer(wx.VERTICAL)        
        inputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        inputBox.Add(wx.StaticText(self, label = "Input"), 0, wx.EXPAND, 10)
        for i in range(2):
            channel = self.audioMixer.getInputChannel(i)
            slide = ControlSlider(self, -80, 12, 0, orient=wx.VERTICAL, outFunction=channel.setVolume)
            self.inputSliders.append(slide)
            meter = VuMeter(self, size=(200,200), numSliders=1, orient=wx.VERTICAL)
            channel.setAmpCallback(meter.setRms)
            self.inputMeters.append(meter)
            if i % 2 == 0:
                inputSliderBox.Add(slide, 0, wx.ALL, 2)
                inputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
                inputSliderBox.AddSpacer(15)
            else:
                inputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
                inputSliderBox.Add(slide, 0, wx.ALL, 2)
                inputSliderBox.AddSpacer(15)
        inputBox.Add(inputSliderBox, 0, wx.EXPAND|wx.ALL, 5)
        
        #### OUTPUT SECTION
        outputBox = wx.BoxSizer(wx.VERTICAL)
        outputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        outputBox.Add(wx.StaticText(self, label = "Output"), 0, wx.EXPAND, 10)
        for i in range(2):
            channel = self.audioMixer.getOutputChannel(i)
            
            slide = ControlSlider(self, -80, 12, 0, orient=wx.VERTICAL, outFunction=channel.setVolume)

            self.outputSliders.append(slide)
            meter = VuMeter(self, size=(200,200), numSliders=1, orient=wx.VERTICAL)
            channel.setAmpCallback(meter.setRms)

            self.outputMeters.append(meter)
            if i % 2 == 0:
                outputSliderBox.Add(slide, 0, wx.ALL, 2)
                outputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
                outputSliderBox.AddSpacer(15)
            else:
                outputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
                outputSliderBox.Add(slide, 0, wx.ALL, 2)
                outputSliderBox.AddSpacer(15)
                
        outputBox.Add(outputSliderBox, 0, wx.EXPAND|wx.ALL, 5)
            
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(inputBox, 1, wx.EXPAND)
        mainSizer.Add(outputBox, 1, wx.EXPAND)
        self.SetSizer(mainSizer)


if __name__ == "__main__":

    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, size=(1000,200))
            self.Bind(wx.EVT_CLOSE, self.onClose)
            self.mixer = AudioMixer()
            self.pan = MixerPanel(self, self.mixer)

            
        def onClose(self, evt):
            s.stop()
            self.Destroy()

    s = Server().boot().start()
    s.amp = 0.1
    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()
