#!/usr/bin/python
# simple.py
"""
- cleanup call from fxbox to floating window
"""
import __builtin__
__builtin__.QLIVE_APP_OPENED = True

import wx
from pyo import *
from FxTrack import *
from CuesPanel import *
from SoundFilePanel import *
from MixerPanel import *
from FxTracksToolbar import *
from FxTracks import *
from MenuBar import *

class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size = (1200, 700) )
        self.s = Server().boot()
        self.s.start()
        self.menuB = MenuBar()
        self.SetMenuBar(self.menuB)
        
        # PANELS CREATION
#        self.tracksToolBar = FxTracksToolBar(self)
        self.tracks = FxTracks(self)
#        self.soundfilePlayer = SoundFilePanel(self)
        self.cues = CuesPanel(self)
        self.mixer = MixerPanel(self)


        # LAYOUT, SIZERS
#        self.tracksSizer = wx.BoxSizer(wx.VERTICAL)
#        self.tracksSizer.Add(self.tracksToolBar, 1, wx.EXPAND)
#        self.tracksSizer.Add(self.track, 1, wx.EXPAND)

        self.topCuesAndRestSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.topCuesAndRestSizer.Add(self.cues, 0, wx.EXPAND, 5)
        self.topCuesAndRestSizer.Add(self.tracks, 1, wx.EXPAND, 5)

        self.mainMixerVsRest = wx.BoxSizer(wx.VERTICAL)
        self.mainMixerVsRest.AddSizer(self.topCuesAndRestSizer, 2, wx.EXPAND, 5)
        self.mainMixerVsRest.Add(self.mixer, 0, wx.EXPAND, 5)
        self.SetSizer(self.mainMixerVsRest)




if __name__ == "__main__":


    app = wx.App()

    frame = MainWindow()
    frame.Show()

    app.MainLoop()
