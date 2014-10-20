#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *

class MixerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size = (800,200))
        self.SetBackgroundColour((180,180,180))
        pass







if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()