import wx
from FxTrack import *
from FxView import FxViewManager

class FxTracksToolBar(wx.ToolBar):
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, size = (1000, 40))
        self.AddControl(wx.StaticText(self, label=" FxTracks Toolbar (what controls go here?)"))
        self.Realize()

class FxTracks(wx.Panel):
    def __init__(self, parent, size = (-1,800)):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.toolbar = FxTracksToolBar(self)

        # FX window manager
        self.fxsView = FxViewManager(self)
        
        # This should be an  array of FxTrack objects
        self.track = FxTrack(self, self.fxsView)

        self.sizer.Add(self.toolbar, 0, wx.EXPAND)
        self.sizer.Add(self.track, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def getSaveDict(self):
        # for now simple thru, later compile differents tracks into dict
        return self.track.getSaveDict()

    def setSaveDict(self, saveDict):
        self.track.setSaveDict(saveDict)
        
    def loadCue(self, cue):
        self.track.loadCue(cue)
        
    def copyCue(self, cueToCopy):
        self.track.copyCue(cueToCopy)
      
    def cueEvent(self, eventDict):
        self.track.cueEvent(eventDict)
        self.fxsView.refresh()
        
    def connectAudioMixer(self, audioMixer):
        self.track.connectAudioMixer(audioMixer)
        
if __name__ == "__main__":
    from CuesPanel import CuesPanel
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.server = Server().boot()
            panel = wx.Panel(self)
            self.cues = CuesPanel(panel)
            QLiveLib.setVar("CuesPanel", self.cues)
            self.tracks = FxTracks(panel)
            self.sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer.Add(self.cues,0, wx.EXPAND)
            self.sizer.Add(self.tracks,1, wx.EXPAND)
            panel.SetSizer(self.sizer)
    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()