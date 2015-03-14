#!/usr/bin/env python
# encoding: utf-8
import wx
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR, VuMeter
from AudioMixer import *
from constants import *

class QLiveControlSlider(ControlSlider):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), 
                 size=(200,16), log=False, outFunction=None, integer=False, 
                 powoftwo=False, backColour=None, orient=wx.HORIZONTAL):
        ControlSlider.__init__(self, parent, minvalue, maxvalue, init, pos, 
                               size, log, outFunction, integer, powoftwo, 
                               backColour, orient)
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
            self.setBackgroundColour(MIDILEARN_COLOUR)
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
        wx.Panel.__init__(self, parent, size=(800,200), style=wx.SUNKEN_BORDER)
        self.audioMixer = audioMixer
        self.SetBackgroundColour(BACKGROUND_COLOUR)

        self.inputSliders = []
        self.outputSliders = []
        self.inputMeters = []
        self.outputMeters = []
        
        ### INPUT SECTION
        inputBox = wx.BoxSizer(wx.VERTICAL)        
        inputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        inputBox.AddSpacer((-1,5))
        inputBox.Add(wx.StaticText(self, label="Input Channels"), 0, wx.LEFT|wx.EXPAND, 10)
        inputBox.Add(wx.StaticLine(self, size=(1, -1)), 0, wx.EXPAND|wx.ALL, 5)
        for i in range(NUM_INPUTS):
            channel = self.audioMixer.getInputChannel(i)
            slide = QLiveControlSlider(self, -80, 12, 0, orient=wx.VERTICAL, 
                                       outFunction=channel.setVolume)
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
        
        separator = wx.StaticLine(self, size=(1, -1), style=wx.LI_VERTICAL)

        #### OUTPUT SECTION
        outputBox = wx.BoxSizer(wx.VERTICAL)
        outputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        outputBox.AddSpacer((-1,5))
        outputBox.Add(wx.StaticText(self, label = "Output Channels"), 0, wx.LEFT|wx.EXPAND, 10)
        outputBox.Add(wx.StaticLine(self, size=(1, -1)), 0, wx.EXPAND|wx.ALL, 5)
        for i in range(NUM_OUTPUTS):
            channel = self.audioMixer.getOutputChannel(i)            
            slide = QLiveControlSlider(self, -80, 12, 0, orient=wx.VERTICAL, 
                                       outFunction=channel.setVolume)
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
        mainSizer.Add(separator, 0, wx.EXPAND|wx.ALL, 5)
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
    from pyo import *
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.Bind(wx.EVT_CLOSE, self.onClose)
            self.server = Server().boot().start()
            self.server.amp = 0.1
            self.mixer = AudioMixer()
            self.panel = MixerPanel(self, self.mixer)
            self.SetSize(self.panel.GetBestSize())
        def onClose(self, evt):
            self.server.stop()
            self.Destroy()
    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()
