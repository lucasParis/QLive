#!/usr/bin/env python
# encoding: utf-8
import wx
import wx.lib.scrolledpanel as scrolled
import QLiveLib

class CuesToolBar(wx.ToolBar):
    def __init__(self, parent, newCueCallback):
        wx.ToolBar.__init__(self, parent, size = (-1, -1), style = wx.TB_VERTICAL)
        self.newCueCallback = newCueCallback
#        self.remRowButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
#        self.remRowButton.SetLabel("-")    
#        self.AddControl(wx.StaticText(self, label = "New \nCue"))
        self.remRowButton = wx.Button(self, size = (40,34), pos = (-1,-1))
        self.remRowButton.Bind(wx.EVT_BUTTON, self.onNewCue)
        self.remRowButton.SetLabel("New\nCue")
        self.AddControl(self.remRowButton)
        self.Realize()
        
    def onNewCue(self, event):
        self.newCueCallback()

class CuesPanel(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, size=(150, 500))
   
        self.panel = wx.Panel(self)
        self.toolbar = CuesToolBar(self.panel, self.onNewCue)
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
#        self.appendCueButton()
#        self.appendCueButton()
#        self.clearButtons()
#        self.appendCueButton()
#        self.appendCueButton()
#        self.setSelectedCue(0)
        
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
    def setSelectedCue(self, number):
        if number < len(self.cueButtons):
            self.cueButtons[number].SetDefault()
            self.currentCue = number
        
    def clearButtons(self):
        for i, button in enumerate(self.cueButtons):
            button.Unbind(wx.EVT_BUTTON) # why ?
            self.cuesPanelSizer.Remove(button)
            button.Destroy()
        self.cueButtons = []
        self.cuesPanelSizer.Layout()

    def appendCueButton(self):
        number = str(len(self.cueButtons))
        self.currentCue = int(number)
        but = wx.Button(self.cuesPanel, size = (40, -1), label = number, name = number)
        but.Bind(wx.EVT_BUTTON, self.onCueSelection)
        but.SetDefault()
        self.cuesPanelSizer.Add(but, 0, wx.EXPAND|wx.ALL, 2)
        self.cueButtons.append(but)
        self.cuesPanelSizer.Layout()

    def onCueSelection(self, event):
        button = event.GetEventObject()
        button.SetDefault()
        number = int(button.GetName())
        self.currentCue = number
        if QLiveLib.getVar("MainWindow") != None:
#            QLiveLib.getVar("MainWindow").tracks.loadCue(self.currentCue)
            dictEvent = {'type': "cueSelect", "selectedCue": self.currentCue}
            QLiveLib.getVar("MainWindow").tracks.cueEvent(dictEvent)
        
    def onNewCue(self):
        if QLiveLib.getVar("MainWindow") != None:
#            QLiveLib.getVar("MainWindow").tracks.copyCue(self.currentCue)
            dictEvent = {'type': "newCue", "currentCue":self.currentCue, 
                                 "totalCues": len(self.cueButtons)}
            QLiveLib.getVar("MainWindow").tracks.cueEvent(dictEvent)
        self.appendCueButton()
        
    def setNumberOfCues(self, numbers):
        return len(self.cueButtons)        

    def getNumberOfCues(self):
        return len(self.cueButtons)
        
    def getCurrentCue(self):
        return self.currentCue

    def setSaveDict(self, dict):
        self.clearButtons()
        for i in range(dict["numberOfCues"]):
            self.appendCueButton()
        self.setSelectedCue(0)
            
        
    def getSaveDict(self):
        dict = {}
        dict["numberOfCues"] = len(self.cueButtons)
        return dict
        
if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.cuesPanel = CuesPanel(self)
            self.cuesPanel.parent = None
    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()