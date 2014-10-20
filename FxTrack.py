#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from FxBox import *
import  wx.lib.scrolledpanel as scrolled


class FxTrack(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.GridBagSizer()
        self.SetBackgroundColour(wx.Colour(100, 100, 100))
        cols = 5
        rows = 1
        self.buttons = []
        for i in range(cols):
            for j in range(rows):
                but = FxBox(self)
                self.buttons.append(but)
                self.sizer.Add(but, (j,i))
                
        self.SetSizer(self.sizer)
        
        self.viewPanelRef = None

    def setViewPanelRef(self, ref):
        self.viewPanelRef = ref



if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            print "quelquechose"
            self.fxTrack = FxTrack(self)


    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()