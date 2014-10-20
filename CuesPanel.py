#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *

class CuesPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size = (100, 500))
        self.SetBackgroundColour((80,80,80))
        pass





if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.panel = CuesPanel(self)
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()