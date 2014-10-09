#!/usr/bin/python
# encoding: utf-8
import wx
import  wx.lib.scrolledpanel as scrolled
from pyo import *
from FxSlidersView import *

class FxViewsPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.openViews = []
        pass
    def openViewForAudioProcess(self, audioProcess):
        # make sure it's not already opened
        
        pass

if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
#            self.s = Server().boot()
#            self.s.start()
            
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()