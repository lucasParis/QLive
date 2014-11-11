#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *
import  wx.lib.scrolledpanel as scrolled
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR

class MixerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size = (800,200))
        self.SetBackgroundColour(BACKGROUND_COLOUR)

        self.inputSliders = []
        self.outputSliders = []
        
        inputBox = wx.BoxSizer(wx.VERTICAL)        
        inputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        inputBox.Add(wx.StaticText(self, label = "Input"), 0, wx.EXPAND, 10)
        for i in range(6):
            slide = ControlSlider(self, -80, 12, 0, orient=wx.VERTICAL)
            inputSliderBox.Add(slide, 0, wx.ALL, 2)
            self.inputSliders.append(slide)
        inputBox.Add(inputSliderBox, 0, wx.EXPAND)

        outputBox = wx.BoxSizer(wx.VERTICAL)
        outputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        outputBox.Add(wx.StaticText(self, label = "Output"), 0, wx.EXPAND, 10)
        for i in range(6):
            slide = ControlSlider(self, -80, 12, 0, orient=wx.VERTICAL)
            outputSliderBox.Add(slide, 0, wx.ALL, 2)
            self.outputSliders.append(slide)
        outputBox.Add(outputSliderBox, 0, wx.EXPAND)
            
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(inputBox, 1, wx.EXPAND)
        mainSizer.Add(outputBox, 1, wx.EXPAND)
        self.SetSizer(mainSizer)







if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.pan = MixerPanel(self)
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()
