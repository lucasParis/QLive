#!/usr/bin/python
# simple.py

import __builtin__
__builtin__.QLIVE_APP_OPENED = True

import wx
from pyo import *
from FxTrack import *
from FxDialogsManager import *
from CuesPanel import *
from SoundFilePanel import *
from MixerPanel import *


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size = (1200, 700) )
        self.s = Server().boot()
        self.s.start()
        
        # PANELS CREATION
        self.track = FxTrack(self)
        self.soundfilePlayer = SoundFilePanel(self)
        self.cues = CuesPanel(self)
        self.mixer = MixerPanel(self)


        # LAYOUT, SIZERS
        self.trackSoundfileSizer = wx.BoxSizer(wx.VERTICAL)
        self.trackSoundfileSizer.Add(self.track, 1, wx.EXPAND, 5)
        self.trackSoundfileSizer.Add(self.soundfilePlayer, 1, wx.EXPAND, 5)

        self.topCuesAndRestSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.topCuesAndRestSizer.Add(self.cues, 0, wx.EXPAND, 5)
        self.topCuesAndRestSizer.AddSizer(self.trackSoundfileSizer, 2, wx.EXPAND, 5)

        self.mainMixerVsRest = wx.BoxSizer(wx.VERTICAL)
        self.mainMixerVsRest.AddSizer(self.topCuesAndRestSizer, 2, wx.EXPAND, 5)
        self.mainMixerVsRest.Add(self.mixer, 0, wx.EXPAND, 5)
        self.SetSizer(self.mainMixerVsRest)


        # FX WINDOW MANAGER
        self.fxsView = FxDialogsManager(self)
        self.track.setViewPanelRef(self.fxsView)


if __name__ == "__main__":


    app = wx.App()

    frame = MainWindow()
    frame.Show()

    app.MainLoop()
