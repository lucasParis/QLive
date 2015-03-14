#!/usr/bin/env python
# encoding: utf-8
import wx
import wx.lib.scrolledpanel as scrolled
import QLiveLib

class CuesPanel(scrolled.ScrolledPanel):
    def __init__(self, parent=None):
        scrolled.ScrolledPanel.__init__(self, parent, size=(95, 500), style=wx.SUNKEN_BORDER)

        self.currentCue = 0
        self.cueButtons = []
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.newButton = wx.Button(self, label="New Cue", size=(70, -1))
        self.newButton.Bind(wx.EVT_BUTTON, self.onNewCue)
        self.mainSizer.Add(self.newButton, 0, wx.EXPAND|wx.ALL, 5)

        self.mainSizer.Add(wx.StaticLine(self, size=(1, 1)), 0, wx.EXPAND|wx.ALL, 5)        
        self.SetSizer(self.mainSizer)

        self.appendCueButton()

    def setSelectedCue(self, number):
        if number < len(self.cueButtons):
            self.cueButtons[number].SetDefault()
            self.currentCue = number
        
    def clearButtons(self):
        for button in self.cueButtons:
            self.mainSizer.Remove(button)
            button.Destroy()
        self.cueButtons = []
        self.mainSizer.Layout()

    def appendCueButton(self):
        number = str(len(self.cueButtons))
        self.currentCue = int(number)
        butHeight = self.GetTextExtent("9")[1] + 8
        but = wx.Button(self, size=(70, butHeight), label=number, name=number)
        but.Bind(wx.EVT_BUTTON, self.onCueSelection)
        but.SetDefault()
        self.mainSizer.Add(but, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.cueButtons.append(but)
        self.SetupScrolling()
        self.mainSizer.Layout()

    def onCueSelection(self, event):
        button = event.GetEventObject()
        button.SetDefault()
        self.currentCue = int(button.GetName())
        if QLiveLib.getVar("MainWindow") != None:
            dictEvent = {'type': "cueSelect", "selectedCue": self.currentCue}
            QLiveLib.getVar("MainWindow").tracks.cueEvent(dictEvent)
        
    def onNewCue(self, evt):
        if QLiveLib.getVar("MainWindow") != None:
            dictEvent = {'type': "newCue", "currentCue":self.currentCue, 
                                 "totalCues": len(self.cueButtons)}
            QLiveLib.getVar("MainWindow").tracks.cueEvent(dictEvent)
        self.appendCueButton()
        
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