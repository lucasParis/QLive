#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *



class SoundFilePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour((140,140,140))
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