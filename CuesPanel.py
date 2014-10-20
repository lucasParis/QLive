#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *
import  wx.lib.scrolledpanel as scrolled

class CuesPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size = (100, 500))
        self.SetBackgroundColour((80,80,80))
        
        self.addCueButton = wx.Button(self)
        self.addCueButton.SetLabel("New Cue")

        #LAYOUT
        self.cueOptionsSizer = wx.GridSizer(2,2)
        self.cueOptionsSizer.Add(self.addCueButton)
        
        #CUESBUTTONS
        self.cuesPanel = scrolled.ScrolledPanel(self)
        self.cuesPanel.SetupScrolling()
        self.cuesPanelSizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(20):
            but = wx.Button(self.cuesPanel)
            but.SetLabel(str(i))
            self.cuesPanelSizer.Add(but)
        self.cuesPanel.SetSizer(self.cuesPanelSizer)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.cueOptionsSizer)
        self.mainSizer.Add(self.cuesPanel, 1, wx.EXPAND)

        self.SetSizer(self.mainSizer)
        pass





if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.panel = CuesPanel(self)
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()