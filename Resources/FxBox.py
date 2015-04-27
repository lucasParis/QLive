#!/usr/bin/python
# encoding: utf-8
import wx, weakref
from constants import *
from fxbox_def import *
import QLiveLib
from FxView import FxSlidersView

class BaseFxBox(object):
    def __init__(self, parent):
        self.parent = parent
        self.name = ""
        self.audioRef = None
        self.id = [0,0]
        self.enable = 1
        self.view = None
        self.cues = {}
        self.currentCue = 0

    def setAudioRef(self, obj):
        if obj is None:
            self.audioRef = None
        else:
            self.audioRef = weakref.ref(obj)

    def getEnable(self):
        return self.enable

    def setInput(self, input):
        if self.audioRef is not None:
            audio = self.audioRef()
            audio.setInput(input)
        
    def getOutput(self):
        if self.audioRef is not None:
            audio = self.audioRef()
            return audio.getOutput()
        return None

    def setParamValue(self, name, value, fromUser):
        if self.audioRef is not None:
            audio = self.audioRef()
            if name == "gain":
                value = pow(10, value * 0.05)
            if fromUser:
                getattr(audio, name).time = 0.01
            getattr(audio, name).value = value

    def setInterpValue(self, name, value):
        if self.audioRef is not None:
            audio = self.audioRef()
            getattr(audio, name).time = value

    def setEnable(self, x, fromUser=False):
        self.enable = x
        if self.audioRef is not None:
            audio = self.audioRef()
            audio.setEnable(x)
        if not fromUser and self.view is not None:
            self.view.setEnableState(x)
        
    def setId(self, id):
        self.id = id
        
    def getId(self):
        return self.id
        
    def setName(self, name):
        self.name = name

    def openView(self):
        if self.view is not None:
            self.view.Show()

    def openMenu(self, event):
        fxTracks = QLiveLib.getVar("FxTracks")
        menu = wx.Menu()
        id = BOX_MENU_ITEM_FIRST_ID
        for name in self.choices:
            menu.Append(id, name)
            id += 1
        fxTracks.Bind(wx.EVT_MENU, self.select, id=BOX_MENU_ITEM_FIRST_ID, id2=id)
        fxTracks.PopupMenu(menu, event.GetPosition())
        menu.Destroy()

    def select(self, evt):
        sel = self.choices[evt.GetId() - BOX_MENU_ITEM_FIRST_ID]
        self.initModule(sel)
        
    def initModule(self, name):
        self.name = name
        self.createView()
        currentCue = QLiveLib.getVar("CuesPanel").getCurrentCue()
        self.addCue(currentCue)

    def createView(self):
        if self.name:
            parameters = self.module_dict[self.name]
            self.view = FxSlidersView(QLiveLib.getVar("MainWindow"), self, parameters)

    def delete(self):
        if self.view is not None:
            self.view.Destroy()

    def getParams(self):
        if self.view is not None:
            widgets = self.view.getWidgets()
            params = [widget.getValue() for widget in widgets]
            inters = [widget.getInterpValue() for widget in widgets]
            return (params, inters, self.enable)
        else:
            return None

    def setParams(self, params):
        if self.view is not None:
            widgets = self.view.getWidgets()
            for i, widget in enumerate(widgets):
                widget.setInterpValue(params[1][i], propagate=True)
                widget.setValue(params[0][i], propagate=True)
            if len(params) > 2:
                self.setEnable(params[2])

    def saveCue(self):
        self.cues[self.currentCue] = self.getParams()

    def addCue(self, x):
        self.currentCue = x
        self.saveCue()

    def delCue(self, old, new):
        del self.cues[old]
        for i in range(old+1, len(self.cues)):
            if i in self.cues:
                self.cues[i-1] = self.cues[i]
                del self.cues[i]
        self.loadCue(new)

    def getCues(self):
        return self.cues

    def loadCue(self, x):
        if x in self.cues:
            self.setParams(self.cues[x])
        else:
            c = x
            while (c >= 0):
                if c in self.cues:
                    self.setParams(self.cues[c])
                    break
                c -= 1
        self.currentCue = x

    def cueEvent(self, evt):
        tp = evt.getType()
        if tp == CUE_TYPE_DELETE:
            self.delCue(evt.getOld(), evt.getCurrent())
        elif tp == CUE_TYPE_SELECT:
            self.saveCue()
            self.loadCue(evt.getCurrent())
        elif tp == CUE_TYPE_NEW:
            self.saveCue()
            self.addCue(evt.getCurrent())

    def getSaveDict(self):
        self.saveCue()
        return {'name': self.name,
                'id': self.id,
                'cues': self.cues}

    def setSaveDict(self, saveDict):
        self.name = saveDict["name"]
        self.id = saveDict["id"]
        self.cues = saveDict["cues"]
        self.createView()
        self.loadCue(0)

class FxBox(BaseFxBox):
    def __init__(self, parent):
        BaseFxBox.__init__(self, parent)
        self.module_dict = FX_DICT
        self.choices = FX_LIST

    def getRect(self):
        x = TRACK_COL_SIZE * self.id[0] + 135
        y = TRACK_ROW_SIZE * self.id[1]  + self.parent.trackPosition + 10
        return wx.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

class InputBox(BaseFxBox):
    def __init__(self, parent):
        BaseFxBox.__init__(self, parent)
        self.module_dict = INPUT_DICT
        self.choices = INPUT_LIST

    def getRect(self):
        x = 35
        y = TRACK_ROW_SIZE * self.id[1] + self.parent.trackPosition + 10
        return wx.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
