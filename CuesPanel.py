#!/usr/bin/env python
# encoding: utf-8
import wx
from pyo import *
import  wx.lib.scrolledpanel as scrolled


class CuesToolBar(wx.ToolBar):
    def __init__(self, parent, parent2):
        wx.ToolBar.__init__(self, parent, size = (-1, -1), style = wx.TB_VERTICAL)
        self.parentForCallBacks = parent2
#        self.remRowButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
#        self.remRowButton.SetLabel("-")    
#        self.AddControl(wx.StaticText(self, label = "New \nCue"))
        self.remRowButton = wx.Button(self, size = (40,34), pos = (-1,-1))
        self.remRowButton.Bind(wx.EVT_BUTTON, self.onNewCue)
        self.remRowButton.SetLabel("New\nCue")
        self.AddControl(self.remRowButton)


        self.Realize()
        
    def onNewCue(self, event):
        self.parentForCallBacks.onNewCue(event)



class CuesPanel(wx.Panel):
    def __init__(self, parent = None):
        wx.Panel.__init__(self, parent, size = (150, 500))
        self.SetBackgroundColour((80,80,80))
        self.parent = parent
   
        self.panel = wx.Panel(self)
        self.toolbar = CuesToolBar(self.panel, self)
        boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer.Add(self.toolbar, 2, wx.EXPAND)
        self.panel.SetSizer(boxSizer)
        
        self.currentCue = 0
        
        #CUESBUTTONS
        self.cuesPanel = scrolled.ScrolledPanel(self)
        self.cuesPanel.SetupScrolling()
        self.cuesPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.cueButtons = []
        self.appendCueButton()

        
        self.cuesPanel.SetSizer(self.cuesPanelSizer)
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(self.panel, 0, wx.EXPAND)

        self.mainSizer.Add(self.cuesPanel, 1, wx.EXPAND)
        self.SetSizer(self.mainSizer)
            
        self.templateCueEvent = {'type': "empty"}
        """
        types:
            - addCue: 
            - setCue:
        """

    def appendCueButton(self):
        number = str(len(self.cueButtons))
        self.currentCue = number
        but = wx.Button(self.cuesPanel, size = (40, -1), label = number, name = number)
        but.Bind(wx.EVT_BUTTON, self.onCueSelection)
        but.SetDefault()
        self.cuesPanelSizer.Add(but, 1, wx.EXPAND|wx.ALL, 2)
        self.cueButtons.append(but)
        self.cuesPanelSizer.Layout()

    def onCueSelection(self, event):
        button = event.GetEventObject()
        button.SetDefault()
        number = int(button.GetName())
        self.currentCue = number
        if self.parent != None:
#            self.parent.tracks.loadCue(self.currentCue)
            dictEvent = {'type': "cueSelect", "selectedCue": self.currentCue}
            self.parent.tracks.cueEvent(dictEvent)
        
    def onNewCue(self, event):
        if self.parent != None:
#            self.parent.tracks.copyCue(self.currentCue)
            dictEvent = {'type': "newCue", "currentCue":self.currentCue, "totalCues": len(self.cueButtons)}
            self.parent.tracks.cueEvent(dictEvent)
        self.appendCueButton()
        



if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            
            self.cuesPanel = CuesPanel(self)

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()