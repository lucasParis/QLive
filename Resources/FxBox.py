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
        
    def setId(self, Id):
        self.id = Id
        
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
        if self.parent.PopupMenu(menu, event.GetPosition()):
            if menu.getSelection() is not None:
                self.initModule(menu.getSelection())
        menu.Destroy()
        
    def initModule(self, name):
        self.audio = self.creator().createByName(name)
        self.name = self.audio.name
        self.audio.setInput(self.audioIn)
        self.audioOut.setValue(self.audio.getOutput())
        # setup empty cues
        cuesPanel = QLiveLib.getVar("CuesPanel")
        numberOfCues = cuesPanel.getNumberOfCues()
        if numberOfCues > 1:
            currentCue = cuesPanel.getCurrentCue()
            self.audio.initCues(numberOfCues, currentCue)
        #self.parent.createConnections()

    def getSaveDict(self):
        if self.audio != None:
            dict = self.audio.getSaveDict()
            dict["name"] = self.name
            return dict
        else:
            return None

    def setSaveDict(self, saveDict):
        if saveDict != None:
            self.initModule(saveDict["name"])
            self.audio.setSaveDict(saveDict)
        else: # use case: empty fx/input, load default/empty
            pass
        
    def loadCue(self, cue):
        pass
        
    def copyCue(self, cueToCopy):
        pass
        
    def cueEvent(self, eventDict):
        if self.audio != None:
            self.audio.cueEvent(eventDict)
#        if eventDict["type"] == 'newCue':
#            print eventDict["currentCue"], eventDict["totalCues"]
#        elif eventDict["type"] == 'cueSelect':
#            print eventDict["selectedCue"]
#            dictEvent = {'type': "cueSelect", "selectedCue": self.currentCue}

class FxBox(ParentBox):
    def __init__(self, parent):
        ParentBox.__init__(self, parent)
        self.menu = FxBoxMenu
        self.creator = FxCreator

class InputBox(ParentBox):
    def __init__(self, parent):
        ParentBox.__init__(self, parent)
        self.audioOut.value = Sig([0]*NUM_CHNLS)
        self.menu = InputBoxMenu
        self.creator = InputCreator

if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s = Server().boot()
            self.s.start()
            self.but = InputBox(self)
            self.but.getOutput().out()
            self.but.setInput(Input([0,1]))
            self.Bind(wx.EVT_RIGHT_DOWN, self.rightClicked)

        def rightClicked(self, event):
            self.but.openMenu(event)

    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()