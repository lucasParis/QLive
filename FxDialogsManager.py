#!/usr/bin/python
# encoding: utf-8
import wx
import  wx.lib.scrolledpanel as scrolled
from pyo import *
from FxSlidersView import *

"""
changing FxViewsPanel from panel to frame manager FxDialogsManager
"""


class FxDialogsManager(object):
    """
    only allow one frame open per FX
    """
    def __init__(self, parent):
        self.openViews = []
        pass

    def openViewForAudioProcess(self, audioProcess):
        # make sure it's not already opened
        view = FxSlidersView(self, audioProcess)
        view.Show()
        self.openViews.append(view)

        

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
            
            self.fxs = FxDialogsManager(self)    
            self.fxs.openViewForAudioProcess(self.fx)

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()