#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *
import  wx.lib.scrolledpanel as scrolled
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR, VuMeter

class MixerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size = (800,200))
        self.parent = parent
        self.SetBackgroundColour(BACKGROUND_COLOUR)

        self.inputSliders = []
        self.outputSliders = []
        self.inputMeters = []
        self.outputMeters = []
        
#        inputSliderCallbacks = [self.inputSlider1, self.inputSlider2, self.inputSlider3,
#                                self.inputSlider4, self.inputSlider5, self.inputSlider6]
        inputBox = wx.BoxSizer(wx.VERTICAL)        
        inputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        inputBox.Add(wx.StaticText(self, label = "Input"), 0, wx.EXPAND, 10)
        for i in range(6):
            slide = ControlSlider(self, -80, 12, 0, orient=wx.VERTICAL, outFunction=None)#inputSliderCallbacks[i]
            self.inputSliders.append(slide)
            inputSliderBox.Add(slide, 0, wx.ALL, 2)
            meter = VuMeter(self, size=(200,200), numSliders=2, orient=wx.VERTICAL)
            self.inputMeters.append(meter)
            inputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
            inputSliderBox.AddSpacer(15)
        inputBox.Add(inputSliderBox, 0, wx.EXPAND|wx.ALL, 5)

        outputBox = wx.BoxSizer(wx.VERTICAL)
        outputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        outputBox.Add(wx.StaticText(self, label = "Output"), 0, wx.EXPAND, 10)
        for i in range(6):
            slide = ControlSlider(self, -80, 12, 0, orient=wx.VERTICAL)
            outputSliderBox.Add(slide, 0, wx.ALL, 2)
            self.outputSliders.append(slide)
            meter = VuMeter(self, size=(200,200), numSliders=2, orient=wx.VERTICAL)
            self.outputMeters.append(meter)
            outputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
            outputSliderBox.AddSpacer(15)
        outputBox.Add(outputSliderBox, 0, wx.EXPAND|wx.ALL, 5)
            
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(inputBox, 1, wx.EXPAND)
        mainSizer.Add(outputBox, 1, wx.EXPAND)
        self.SetSizer(mainSizer)

#    def getInputMeterCallback(self, which):
#        return self.inputMeters[which].setRms

#    def inputSlider1(self, value):
#        self.parent.gens[0].gain.value = 10**(value*0.05)
#    def inputSlider2(self, value):
#        self.parent.gens[1].gain.value = 10**(value*0.05)
#    def inputSlider3(self, value):
#        self.parent.gens[2].gain.value = 10**(value*0.05)
#    def inputSlider4(self, value):
#        self.parent.gens[3].gain.value = 10**(value*0.05)
#    def inputSlider5(self, value):
#        self.parent.gens[4].gain.value = 10**(value*0.05)
#    def inputSlider6(self, value):
#        self.parent.gens[5].gain.value = 10**(value*0.05)

if __name__ == "__main__":
    class Generator:
        def __init__(self, freq=100):
            self.gain = SigTo(1, 0.025, 1)
            self.rnd = Randi(0, 0.7, [0.8,0.6], mul=self.gain)
            self.osc = SineLoop(freq=[freq,freq*1.01], feedback=0.05, mul=self.rnd).out()
            self.peak = PeakAmp(self.osc)
        def setMeterCallback(self, callback):
            self.peak.function = callback

    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, size=(1000,200))
            self.Bind(wx.EVT_CLOSE, self.onClose)
            self.pan = MixerPanel(self)
            self.gens = [Generator(freq=i*100) for i in range(1,7)]
#            [gen.setMeterCallback(self.pan.getInputMeterCallback(i)) for i, gen in enumerate(self.gens)]
            
        def onClose(self, evt):
            s.stop()
            self.Destroy()

    s = Server().boot().start()
    s.amp = 0.1
    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()
