#!/usr/bin/env python
# encoding: utf-8
import wx
import wx.lib.scrolledpanel as scrolled
from constants import *
import QLiveLib
from Widgets import TransportButtons, CueButton

class CueEvent:
    def __init__(self, type, current, old, total):
        self.type = type
        self.current = current
        self.old = old
        self.total = total

    def getType(self):
        return self.type

    def getCurrent(self):
        return self.current

    def getOld(self):
        return self.old

    def getTotal(self):
        return self.total

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(95, -1), style=wx.SUNKEN_BORDER)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.buttons = TransportButtons(self, 
                                        playCallback=QLiveLib.getVar("AudioServer").start,
                                        recordCallback=QLiveLib.getVar("AudioServer").record)
        self.mainSizer.Add(self.buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.mainSizer.Add(wx.StaticLine(self, size=(1, 1)), 0, 
                           wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)        

        title = wx.StaticText(self, label="-- CUES --")
        self.mainSizer.Add(title, 0, wx.ALIGN_CENTER, 5)

        bmp = wx.Bitmap(ICON_ADD, wx.BITMAP_TYPE_PNG)
        self.newButton = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.newButton.Bind(wx.EVT_BUTTON, self.onNewCue)
        self.buttonSizer.Add(self.newButton, 1)

        bmp = wx.Bitmap(ICON_DELETE, wx.BITMAP_TYPE_PNG)
        self.delButton = wx.BitmapButton(self, wx.ID_ANY, bmp)
        self.delButton.Bind(wx.EVT_BUTTON, self.onDelCue)
        self.buttonSizer.Add(self.delButton, 1)
        self.mainSizer.Add(self.buttonSizer, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizerAndFit(self.mainSizer)

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

        self.appendCueButton()

    def setSelectedCue(self, number):
        if number >= 0 and number < len(self.cueButtons):
            if self.currentCue < len(self.cueButtons):
                self.cueButtons[self.currentCue].select(False)
            self.cueButtons[number].select(True)
            self.currentCue = number
            self.SetupScrolling(scroll_x=False, scroll_y=True, scrollToTop=False)
            self.mainSizer.Layout()
            self.ScrollChildIntoView(self.cueButtons[self.currentCue])
            return True
        else:
            return False
        
    def clearButtons(self):
        for button in self.cueButtons:
            self.mainSizer.Remove(button)
            button.Destroy()
        self.cueButtons = []
        self.mainSizer.Layout()

    def appendCueButton(self):
        number = len(self.cueButtons)
        butHeight = self.GetTextExtent("9")[1] + 8
        but = CueButton(self, size=(50, butHeight), number=number, 
                        evtHandler=self.onCueSelection)
        self.mainSizer.Add(but, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.cueButtons.append(but)
        self.setSelectedCue(number)

    def sendCueEvent(self, evt):
        if QLiveLib.getVar("MainWindow") != None:
            QLiveLib.getVar("FxTracks").cueEvent(evt)
            QLiveLib.getVar("Soundfiles").cueEvent(evt)

    def onCueSelection(self, x):
        old = self.currentCue
        if self.setSelectedCue(x):
            evt = CueEvent(type=CUE_TYPE_SELECT, current=self.currentCue, 
                           old=old, total=len(self.cueButtons))
            self.sendCueEvent(evt)

    def loadCurrentCue(self):
            evt = CueEvent(type=CUE_TYPE_SELECT, current=self.currentCue, 
                           old=None, total=len(self.cueButtons))
            self.sendCueEvent(evt)
        
    def onDelCue(self):
        button = self.cueButtons.pop(self.currentCue)
        button.Destroy()
        self.mainSizer.Layout()
        if len(self.cueButtons) == 0:
            self.appendCueButton()
        for i, but in enumerate(self.cueButtons):
            but.setNumber(i)
        deletedCue = self.currentCue
        if self.currentCue > 0:
            selection = self.currentCue - 1
        else:
            selection = 0
        if self.setSelectedCue(selection):
            evt = CueEvent(type=CUE_TYPE_DELETE, current=self.currentCue, 
                           old=deletedCue, total=len(self.cueButtons))
            self.sendCueEvent(evt)

    def onSaveCue(self):
        evt = CueEvent(type=CUE_TYPE_SAVE, current=self.currentCue, 
                       old=None, total=len(self.cueButtons))
        self.sendCueEvent(evt)
        
    def onNewCue(self):
        old = self.currentCue
        self.appendCueButton()
        evt = CueEvent(type=CUE_TYPE_NEW, current=self.currentCue, 
                       old=old, total=len(self.cueButtons))
        self.sendCueEvent(evt)
        
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
