#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from Fxs import FxCreator
from Inputs import InputCreator

class FxBoxMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent
        self.fxNames = FxCreator().getNames()
        self.idsIndexDict = {}
        for i, name in enumerate(self.fxNames):
            id = wx.NewId()
            self.idsIndexDict[id] = i
            self.Append(id, name)
            self.Bind(wx.EVT_MENU, self.fxSelected, id=id)
        self.result = None
            
    def fxSelected(self, event):
        print self.fxNames[self.idsIndexDict[event.GetId()]]
        self.result = self.idsIndexDict[event.GetId()]
        
    def getSelection(self):
        return self.result

class InputBoxMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent
        self.inputNames = InputCreator().getNames()
        self.idsIndexDict = {}
        for i, name in enumerate(self.inputNames):
            id = wx.NewId()
            self.idsIndexDict[id] = i
            self.Append(id, name)
            self.Bind(wx.EVT_MENU, self.fxSelected, id=id)
        self.result = None
            
    def fxSelected(self, event):
        print self.inputNames[self.idsIndexDict[event.GetId()]]
        self.result = self.idsIndexDict[event.GetId()]
        
    def getSelection(self):
        return self.result

class ParentBox(object):
    def __init__(self, parent):
        self.parent = parent
        self.name = ""
        
        self.audio = None
        self.presets = None

        self.id = (0,0)
             
    def setId(self, Id):
        self.id = Id
        
    def getId(self):
        return self.id
        
    def setName(self, name):
        self.name = name

    def openView(self):
        if self.parent.viewPanelRef != None:
            if self.audio != None:
                self.parent.viewPanelRef.openViewForAudioProcess(self.audio)

        
    def openMenu(self, event):
        pass
#        menu = FxBoxMenu(self)
#        if self.parent.PopupMenu(menu, event.GetPosition()):
#            print menu.getSelection()
#            # load FX
#            self.audio = FxCreator().createFx(menu.getSelection())
#            self.name = self.audio.name
#            self.audio.setInput(Input([0,1]))
#            self.audio.getOutput().out()
#        menu.Destroy()
        
        


class FxBox(ParentBox):
    def __init__(self, parent):
        ParentBox.__init__(self, parent)
        pass
        
    def openMenu(self, event):
        menu = FxBoxMenu(self)
        if self.parent.PopupMenu(menu, event.GetPosition()):
            # load FX            
            if not menu.getSelection() == None:
                self.audio = FxCreator().createFx(menu.getSelection())
                self.name = self.audio.name
                self.audio.setInput(Input([0,1]))
                self.audio.getOutput().out()
        menu.Destroy()
        
        

class InputBox(ParentBox):
    def __init__(self, parent):
        ParentBox.__init__(self, parent)
        pass
        
    def openMenu(self, event):
        menu = InputBoxMenu(self)
        if self.parent.PopupMenu(menu, event.GetPosition()):
            print menu.getSelection()
            # load FX
            if not menu.getSelection() == None:
                self.audio = InputCreator().createInput(menu.getSelection())
                self.name = self.audio.name
                self.audio.setInput(Input([0,1]))
                self.audio.getOutput().out()
        menu.Destroy()
        





if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            
            self.s = Server().boot()
            self.s.start()
            
            self.but = InputBox(self)
#            self.Bind(wx.EVT_LEFT_DOWN, self.leftClicked)
            self.Bind(wx.EVT_RIGHT_DOWN, self.rightClicked)

#        def leftClicked(self, event):
#            self.but.openView()

        def rightClicked(self, event):
            self.but.openMenu(event)


    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()