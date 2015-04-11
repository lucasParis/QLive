#!/usr/bin/env python
# encoding: utf-8
import wx
import wx.lib.scrolledpanel as scrolled
from constants import *
import QLiveLib
from Widgets import TransportButtons

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(95, -1), style=wx.SUNKEN_BORDER)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        #self.startButton = wx.ToggleButton(self, label="Audio off", size=(70, -1))
        #self.mainSizer.Add(self.startButton, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        #self.startButton.Bind(wx.EVT_TOGGLEBUTTON, self.audioStartStop)
        self.buttons = TransportButtons(self)
        self.mainSizer.Add(self.buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.mainSizer.Add(wx.StaticLine(self, size=(1, 1)), 0, 
                           wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)        

        title = wx.StaticText(self, label="-- CUES --")
        self.mainSizer.Add(title, 0, wx.ALIGN_CENTER, 5)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR, (24, 24))
        self.newButton = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.newButton.Bind(wx.EVT_BUTTON, self.onNewCue)
        self.buttonSizer.Add(self.newButton, 1)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR, (24, 24))
        self.delButton = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.delButton.Bind(wx.EVT_BUTTON, self.onDelCue)
        self.buttonSizer.Add(self.delButton, 1)
        self.mainSizer.Add(self.buttonSizer, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizerAndFit(self.mainSizer)

    def audioStartStop(self, evt):
        if evt.GetInt() == 1:
            QLiveLib.getVar("AudioServer").start()
            self.startButton.SetLabel("Audio on")
        else:
            QLiveLib.getVar("AudioServer").stop()
            self.startButton.SetLabel("Audio off")

    def onDelCue(self, evt):
        QLiveLib.getVar("CuesPanel").onDelCue()

    def onNewCue(self, evt):
        QLiveLib.getVar("CuesPanel").onNewCue()

class CuesPanel(scrolled.ScrolledPanel):
    def __init__(self, parent=None, size=(95, 500)):
        scrolled.ScrolledPanel.__init__(self, parent, size=size, style=wx.SUNKEN_BORDER)

        self.currentCue = 0
        self.cueButtons = []
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

    def setSelectedCue(self, number):
        if number < len(self.cueButtons):
            if self.currentCue < len(self.cueButtons):
                self.cueButtons[self.currentCue].SetBackgroundColour(CUEBUTTON_UNSELECTED_COLOUR)
            self.cueButtons[number].SetBackgroundColour(CUEBUTTON_SELECTED_COLOUR)
            self.currentCue = number
            self.SetupScrolling(scroll_x=False, scroll_y=True, scrollToTop=False)
            self.mainSizer.Layout()
            self.ScrollChildIntoView(self.cueButtons[self.currentCue])
        
    def clearButtons(self):
        for button in self.cueButtons:
            self.mainSizer.Remove(button)
            button.Destroy()
        self.cueButtons = []
        self.mainSizer.Layout()

    def appendCueButton(self):
        number = str(len(self.cueButtons))
        butHeight = self.GetTextExtent("9")[1] + 8
        but = wx.Button(self, size=(50, butHeight), label=number, name=number)
        but.Bind(wx.EVT_BUTTON, self.onCueSelection)
        self.mainSizer.Add(but, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.cueButtons.append(but)
        self.setSelectedCue(int(number))
        
    def onCueSelection(self, event):
        button = event.GetEventObject()
        self.setSelectedCue(int(button.GetName())) 
        if QLiveLib.getVar("MainWindow") != None:
            dictEvent = {"type": "cueSelect", 
                         "selectedCue": self.currentCue}
            QLiveLib.getVar("MainWindow").tracks.cueEvent(dictEvent)

    def onDelCue(self):
        button = self.cueButtons.pop(self.currentCue)
        button.Destroy()
        self.mainSizer.Layout()
        if len(self.cueButtons) == 0:
            self.appendCueButton()
        for i, but in enumerate(self.cueButtons):
            but.SetLabel(str(i))
            but.SetName(str(i))
        deletedCue = self.currentCue
        if self.currentCue > 0:
            selection = self.currentCue - 1
        else:
            selection = 0
        self.setSelectedCue(selection)
        if QLiveLib.getVar("MainWindow") != None:
            dictEvent = {"type": "deleteCue", 
                         "currentCue": self.currentCue,
                         "deletedCue" : deletedCue,
                         "totalCues": len(self.cueButtons)}
            QLiveLib.getVar("MainWindow").tracks.cueEvent(dictEvent)

    def onNewCue(self):
        self.appendCueButton()
        if QLiveLib.getVar("MainWindow") != None:
            dictEvent = {"type": "newCue", 
                         "currentCue": self.currentCue, 
                         "totalCues": len(self.cueButtons)}
            QLiveLib.getVar("MainWindow").tracks.cueEvent(dictEvent)
        
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