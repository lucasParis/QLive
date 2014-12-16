#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *
import  wx.lib.scrolledpanel as scrolled
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR, VuMeter
from AudioMixer import *

class QLiveControlSlider(ControlSlider):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), size=(200,16), log=False, 
                 outFunction=None, integer=False, powoftwo=False, backColour=None, orient=wx.HORIZONTAL):
        ControlSlider.__init__(self, parent, minvalue, maxvalue, init, pos, size, log, outFunction, integer, 
                               powoftwo, backColour, orient)
        self.channelobject = None
        self.midiscanning = False
        self.midiscan = MidiLearn(self.getMidiScan)
        self.Bind(wx.EVT_RIGHT_DOWN, self.MouseRightDown)
 
    def setChannelObject(self, obj):
        self.channelobject = obj

    def MouseRightDown(self, evt):
        if evt.ShiftDown():
            self.setMidiCtl(None)
            self.channelobject.stopMidiCtl()
            return
        if not self.midiscanning:
            self.midiscanning = True
            self.midiscan.scan()
            self.setBackgroundColour("#FF2299")
        else:
            self.midiscanning = False
            self.midiscan.stop()
            self.setBackgroundColour(BACKGROUND_COLOUR)
            
    def getMidiScan(self, ctlnum, midichnl):
        self.setMidiCtl(ctlnum)
        self.channelobject.setMidiCtl(ctlnum)
        self.setBackgroundColour(BACKGROUND_COLOUR)
        
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
            slide = QLiveControlSlider(self, -80, 12, 0, orient=wx.VERTICAL, outFunction=channel.setVolume)
            slide.setChannelObject(channel)
            channel.setMidiCallback(slide.SetValue)
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
            slide = QLiveControlSlider(self, -80, 12, 0, orient=wx.VERTICAL, outFunction=channel.setVolume)
            slide.setChannelObject(channel)
            channel.setMidiCallback(slide.SetValue)
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

    def getSaveDict(self):
        dict = {} 
        inputSliderValues = []
        inputSliderCtls = []
        for slide in self.inputSliders:
            inputSliderValues.append(slide.GetValue())
            inputSliderCtls.append(slide.getMidiCtl())
        dict["inputSliderValues"] = inputSliderValues
        dict["inputSliderCtls"] = inputSliderCtls

        outputSliderValues = []
        outputSliderCtls = []
        for slide in self.outputSliders:
            outputSliderValues.append(slide.GetValue())
            outputSliderCtls.append(slide.getMidiCtl())
        dict["outputSliderValues"] = outputSliderValues
        dict["outputSliderCtls"] = outputSliderCtls

        return dict
        
    def setSaveDict(self, dict):
        for i, slide in enumerate(self.inputSliders):
            val = dict["inputSliderValues"][i]
            ctl = dict["inputSliderCtls"][i]
            slide.SetValue(val)
            slide.setMidiCtl(ctl)
            self.audioMixer.getInputChannel(i).setMidiCtl(ctl)
            self.audioMixer.getInputChannel(i).setMidiCtlValue(val)
        for i, slide in enumerate(self.outputSliders):
            val = dict["outputSliderValues"][i]
            ctl = dict["outputSliderCtls"][i]
            slide.SetValue(val)
            slide.setMidiCtl(ctl)
            self.audioMixer.getOutputChannel(i).setMidiCtl(ctl)
            self.audioMixer.getOutputChannel(i).setMidiCtlValue(val)
            
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
