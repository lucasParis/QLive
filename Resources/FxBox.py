#!/usr/bin/python
# encoding: utf-8
import wx
from pyo64 import *
from constants import *
import QLiveLib
from AudioModule import FxCreator, InputCreator

class BoxMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.result = None

    def prepareMenu(self, names):
        id = BOX_MENU_ITEM_FIRST_ID
        for name in names:
            self.Append(id, name)
            id += 1
        self.Bind(wx.EVT_MENU, self.fxSelected, id=BOX_MENU_ITEM_FIRST_ID, id2=id)

    def fxSelected(self, evt):
        self.result = self.GetLabel(evt.GetId())
        
    def getSelection(self):
        return self.result

class FxBoxMenu(BoxMenu):
    def __init__(self, parent):
        BoxMenu.__init__(self, parent)
        self.prepareMenu(FxCreator().getNames())

class InputBoxMenu(BoxMenu):
    def __init__(self, parent):
        BoxMenu.__init__(self, parent)
        self.prepareMenu(InputCreator().getNames())

class ParentBox(object):
    def __init__(self, parent):
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.name = ""
        self.audio = None
        self.presets = None
        self.id = (0,0)
        self.audioIn = Sig([0] * NUM_CHNLS)
        self.audioOut = Sig(self.audioIn)    
 
    def isEnable(self):
        if self.audio == None:
            return True
        else:
            return self.audio.enable

    def setInput(self, input):
        self.audioIn.setValue(input)
        
    def getOutput(self):
        return self.audioOut
        
    def setId(self, id):
        self.id = id
        
    def getId(self):
        return self.id
        
    def setName(self, name):
        self.name = name

    def openView(self):
        if self.parent.viewPanelRef != None:
            if self.audio != None:
                if self.audio.name:
                    self.parent.viewPanelRef.openViewForAudioProcess(self.audio)

    def openMenu(self, event):
        menu = self.menu(self)
        fxTracks = QLiveLib.getVar("FxTracks")
        if fxTracks.PopupMenu(menu, event.GetPosition()):
            if menu.getSelection() is not None:
                self.initModule(menu.getSelection())
        menu.Destroy()
        
    def initModule(self, name):
        self.audio = self.creator().createByName(name)
        if self.audio is None:
            return False
        self.name = self.audio.name
        self.audio.setInput(self.audioIn)
        self.audioOut.setValue(self.audio.getOutput())
        # setup empty cues
        cuesPanel = QLiveLib.getVar("CuesPanel")
        numberOfCues = cuesPanel.getNumberOfCues()
        if numberOfCues > 1:
            currentCue = cuesPanel.getCurrentCue()
            self.audio.initCues(numberOfCues, currentCue)
        return True

    def getSaveDict(self):
        if self.audio != None:
            dict = self.audio.getSaveDict()
            dict["name"] = self.name
            return dict
        else:
            return None

    def setSaveDict(self, saveDict):
        if saveDict != None:
            if self.initModule(saveDict["name"]):
                self.audio.setSaveDict(saveDict)

    def cueEvent(self, eventDict):
        if self.audio != None:
            self.audio.cueEvent(eventDict)

class FxBox(ParentBox):
    def __init__(self, parent):
        ParentBox.__init__(self, parent)
        self.menu = FxBoxMenu
        self.creator = FxCreator

    def getRect(self):
        x = TRACK_COL_SIZE * self.id[0] + 135
        y = TRACK_ROW_SIZE * self.id[1]  + self.parent.trackPosition + 10
        return wx.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

class InputBox(ParentBox):
    def __init__(self, parent):
        ParentBox.__init__(self, parent)
        self.audioOut.value = Sig([0]*NUM_CHNLS)
        self.menu = InputBoxMenu
        self.creator = InputCreator

    def getRect(self):
        x = 35
        y = TRACK_ROW_SIZE * self.id[1] + self.parent.trackPosition + 10
        return wx.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
