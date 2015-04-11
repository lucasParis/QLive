import wx
from FxTrack import *
from FxView import FxViewManager

class FxTracksToolBar(wx.ToolBar):
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, size = (1000, 40))
        self.AddControl(wx.StaticText(self, 
                        label=" FxTracks Toolbar (what controls go here?)"))
        self.Realize()

class FxTracks(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.selectedTrack = 0
        #self.toolbar = FxTracksToolBar(self)

        # FX window manager
        self.fxsView = FxViewManager(self)
        
        # This should be an  array of FxTrack objects
        self.tracks = [FxTrack(self, self.fxsView, i) for i in range(2)]
        self.tracks[0].setSelected(True)

        #self.sizer.Add(self.toolbar, 0, wx.EXPAND)
        for track in self.tracks:
            self.sizer.Add(track, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def refresh(self):
        self.track.refresh()

    def getSaveDict(self):
        # for now simple thru, later compile differents tracks into dict
        dict = {}
        dict["tracks"] = [track.getSaveDict() for track in self.tracks]
        return dict

    def setSaveDict(self, saveDict):
        for track in self.tracks:
            print self.sizer.Detach(track)
        self.sizer.Clear()

        self.tracks = [FxTrack(self, self.fxsView, i) for i in range(len(saveDict["tracks"]))]
        for i in range(len(self.tracks)):
            self.tracks[i].setSaveDict(saveDict["tracks"][i])
            self.sizer.Add(self.tracks[i], 1, wx.EXPAND)
            
        self.tracks[0].setSelected(True)
        self.selectedTrack = 0

        self.sizer.Layout()
#        self.SetSizer(self.sizer)

#        [track.getSaveDict() for track in self.tracks]
#        self.track.setSaveDict(saveDict)
        
    def loadCue(self, cue):
        for track in self.tracks:
            track.loadCue(cue)
        
    def copyCue(self, cueToCopy):        
        for track in self.tracks:
            track.copyCue(cueToCopy)
      
    def cueEvent(self, eventDict):
        for track in self.tracks:
            track.cueEvent(eventDict)
        self.fxsView.refresh()
        
    # no more used...
    def connectAudioMixer(self, audioMixer):
        self.track.connectAudioMixer(audioMixer)
        
    def addTrack(self):
        self.tracks.append(FxTrack(self, self.fxsView, len(self.tracks)))
        self.sizer.Add(self.tracks[-1], 1, wx.EXPAND)
            
#        self.tracks[-1].setSelected(True)
#        self.selectedTrack = len(self.tracks)-1
        self.setActiveTrack(len(self.tracks)-1)
        self.sizer.Layout()
        pass
        
    def removeTrack(self):
        if len(self.tracks) > 1:
            self.sizer.Detach(self.tracks[self.selectedTrack])
            
            self.tracks[self.selectedTrack].Destroy()            
            del self.tracks[self.selectedTrack]
            
            self.selectedTrack = self.selectedTrack-1
            if self.selectedTrack < 0:
                self.selectedTrack = 0
                
            [track.setID(i)  for i, track in enumerate(self.tracks)]
            self.setActiveTrack(self.selectedTrack)
            self.sizer.Layout()

        
    def setActiveTrack(self, id):
        
        self.selectedTrack = id
        for i, track in enumerate(self.tracks):
            if id == i:
                track.setSelected(True)
            else:
                track.setSelected(False)                
        
        
    
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