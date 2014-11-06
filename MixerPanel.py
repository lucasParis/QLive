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
        self.inSizer = wx.BoxSizer(wx.VERTICAL)
        self.inSizer.Add(wx.StaticText(self, label = "Input"), 0, wx.EXPAND, 10)
        for i in range(6):
            slide = ControlSlider(self, -80, 12, 0)
            self.inSizer.Add(slide, 0, wx.EXPAND, 10)
            self.inputSliders.append(slide)

        self.outputSliders = []
        self.outSizer = wx.BoxSizer(wx.VERTICAL)
        self.outSizer.Add(wx.StaticText(self, label = "Output"), 0, wx.EXPAND, 10)

        for i in range(6):
            slide = ControlSlider(self, -80, 12, 0)
            self.outSizer.Add(slide, 0, wx.EXPAND, 10)
            self.outputSliders.append(slide)
            
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(self.inSizer, 1, wx.EXPAND)
        self.mainSizer.Add(self.outSizer, 1, wx.EXPAND)
        self.SetSizer(self.mainSizer)







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
