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
        self.SetSizer(self.sizer)

    def openViewForAudioProcess(self, audioProcess):
        # make sure it's not already opened
        view = FxSlidersView(self, audioProcess)
        self.openViews.append(view)
        self.sizer.Add(view)
        self.SetSizer(self.sizer)
        

if __name__ == "__main__":
    from pyo import *
    from Fxs import FxCreator
    
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s = Server().boot()
            self.s.start()
            self.fx = FxCreator().createFx(0)
            self.fx.setInput(Input([0,1]))
            self.fx.getOutput().out()
            
            self.fxs = FxViewsPanel(self)    
            self.fxs.openViewForAudioProcess(self.fx)

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()