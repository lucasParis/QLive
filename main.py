#!/usr/bin/python
# simple.py
"""
- how will choice boxes and paths behave in dicts? for now only values are taken care of
- make parent class for both creators input and fxs

Code style:
    - always give other neccessary class through init argument ? never through parent.parent.parent... This facilitates creation of tests
"""
import time
import os
import wx
from pyo import *
from FxTrack import *
from CuesPanel import *
from SoundFilePanel import *
from MixerPanel import *
from FxTracksToolbar import *
from FxTracks import *

class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size = (1200, 700) )
        # There should be a AudioServer class created in 
        # its own file (all audio stuff manage there)
        self.s = Server()
        self.s.setMidiInputDevice(99)
        self.s.boot()
        self.s.start()
        
        # menubar
        menubar = wx.MenuBar()
        menu1 = wx.Menu()

        menu1.Append(wx.ID_SAVE, "Save\tCtrl+S")
        self.Bind(wx.EVT_MENU, self.onSave, id=wx.ID_SAVE)        
        menu1.Append(wx.ID_OPEN, "Open\tCtrl+O")
        self.Bind(wx.EVT_MENU, self.onLoad, id=wx.ID_OPEN)
        menu1.AppendSeparator()
        quitItem = menu1.Append(wx.ID_EXIT, "Quit\tCtrl+Q")
        self.Bind(wx.EVT_MENU, self.OnClose, quitItem)
        menubar.Append(menu1, 'file')
        
        self.SetMenuBar(menubar)
        # end of menubar

        self.tracks = FxTracks(self)
        self.cues = CuesPanel(self)
        self.audioMixer = AudioMixer()
        self.mixer = MixerPanel(self, self.audioMixer)
        self.tracks.connectAudioMixer(self.audioMixer)

        self.topCuesAndRestSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.topCuesAndRestSizer.Add(self.cues, 0, wx.EXPAND, 5)
        self.topCuesAndRestSizer.Add(self.tracks, 1, wx.EXPAND, 5)

        self.mainMixerVsRest = wx.BoxSizer(wx.VERTICAL)
        self.mainMixerVsRest.AddSizer(self.topCuesAndRestSizer, 2, wx.EXPAND, 5)
        self.mainMixerVsRest.Add(self.mixer, 0, wx.EXPAND, 5)
        self.SetSizer(self.mainMixerVsRest)

    def onSave(self, event):
        dlg = wx.FileDialog(self, "choose path to save Qlive projet", os.path.expanduser("~"), 
                            style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            
            dictSave = {}
            dictTracks = self.tracks.getSaveDict()
            dictCues = self.cues.getSaveDict()
            mixerValues = self.mixer.getSaveDict()
            dictSave["tracks"] = dictTracks
            dictSave["cues"] = dictCues
            dictSave["mixer"] = mixerValues

            f = open(path, "w")
            f.write("dictSave = %s" % str(dictSave))
            f.close()
        dlg.Destroy()

    def onLoad(self, event):
        dlg = wx.FileDialog(self, "choose Qlive projet", os.path.expanduser("~"), 
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            execfile(path, globals())
            print "opening: ", dictSave
#            dictSave["tracks"] = dictTracks
#            dictSave["cues"] = dictCues
            self.tracks.setSaveDict(dictSave["tracks"])
            self.cues.setSaveDict(dictSave["cues"])
            self.mixer.setSaveDict(dictSave["mixer"])
        dlg.Destroy()

    def OnClose(self, evt):
        self.s.stop()
        time.sleep(0.25)
        self.audioMixer.onQuit()
        time.sleep(0.25)
        self.s.shutdown()
        time.sleep(0.25)
        self.Destroy()


if __name__ == "__main__":


    app = wx.App()

    frame = MainWindow()
    frame.Show()

    app.MainLoop()
