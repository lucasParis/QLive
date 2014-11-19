import wx
from FxTracksToolbar import *
from FxTrack import *

class FxTracks(wx.Panel):
    def __init__(self, parent, size = (-1,800)):
        wx.Panel.__init__(self, parent)
        self.toolbar = FxTracksToolBar(self)
        self.track = FxTrack(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.toolbar,1, wx.EXPAND)
        self.sizer.Add(self.track,1, wx.EXPAND)
        self.SetSizer(self.sizer)

if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.tracks = FxTracks(self)
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(self.tracks,1, wx.EXPAND)
            self.SetSizer(self.sizer)
        
#            self.pan = MixerPanel(self)
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()