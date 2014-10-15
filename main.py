#!/usr/bin/python
# simple.py

import __builtin__
__builtin__.QLIVE_APP_OPENED = True

import wx
from pyo import *
from FxTrack import *
from FxViewsPanel import *


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size = (1200, 700))
        pass


if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None )
            self.s = Server().boot()
            self.s.start()

            self.mainSizerVer = wx.BoxSizer(wx.HORIZONTAL)
            self.track = FxTrack(self)
            self.mainSizerVer.Add(self.track, 1, wx.EXPAND, 5)
            
            self.fxsView = FxViewsPanel(self)
            self.mainSizerVer.Add(self.fxsView, 1, wx.EXPAND, 5)
            
            self.track.setViewPanelRef(self.fxsView)

            self.SetSizer(self.mainSizerVer)
            

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()
