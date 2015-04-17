#!/usr/bin/python
# encoding: utf-8
import wx
from constants import *
from FxBox import *
import Resources.QLiveLib as QLiveLib

class FxTrack:
    def __init__(self, parent, viewPanelRef, id=0):
        
        self.id = id
        self.trackPosition = 0
        self.trackHeight = TRACK_ROW_SIZE * 2
        self.cols = 1
        self.rows = 1

        self.setFont()
        self.createButtons()

        self.viewPanelRef = viewPanelRef

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setTrackPosition(self, x):
        self.trackPosition = x

    def getTrackPosition(self):
        return self.trackPosition

    def setTrackHeight(self, h):
        self.trackHeight = h

    def getTrackHeight(self):
        return self.trackHeight

    def setFont(self, ptsize=8):
        self.font = wx.Font(ptsize, wx.FONTFAMILY_DEFAULT, wx.NORMAL, 
                            wx.FONTWEIGHT_NORMAL, face="Monospace")

    def createButtons(self):
        # Buttons should be created at a position derived according to ther ids
        self.buttonsFxs = []
        self.buttonsInputs = []
        for i in range(self.rows):
            for j in range(self.cols):
                but = FxBox(self)
                but.setId((j,i))
                self.buttonsFxs.append(but)
            but = InputBox(self)
            but.setId((0,i))
            self.buttonsInputs.append(but)

    def createFx(self, pos):
        but = FxBox(self)
        # need to retrieve the correct id from the position
        but.setId((len(self.buttonsFxs), 0))
        self.buttonsFxs.append(but)

    def start(self):
        self.createConnections()

    def createConnections(self):
        for i, button in enumerate(self.buttonsFxs):
            if i == 0: # Should be based on the id...
                button.setInput(self.buttonsInputs[i].getOutput())
            else:
                button.setInput(self.buttonsFxs[i-1].getOutput())
        self.connectAudioMixer()

    def connectAudioMixer(self):
        audioMixer = QLiveLib.getVar("AudioMixer")
        for but in self.buttonsInputs:
            but.setInput([audioMixer.getInputChannel(i).getOutput() for i in range(NUM_CHNLS)])
        for i, obj in enumerate(self.buttonsFxs):
            if obj.name == "MonoOut":
                audioMixer.addToMixer(0, obj.getOutput())
            if obj.name == "StereoOut":
                audioMixer.addToMixer(0, obj.getOutput()[0])
                audioMixer.addToMixer(1, obj.getOutput()[1])

    def onPaint(self, dc, buttonBitmap, disableButtonBitmap, selectedTrack):
        gc = wx.GraphicsContext_Create(dc)

        dc.SetFont(self.font)

        # grid
        dc.SetPen(wx.Pen("#3F3F3F", 1))
        for i in range(1, self.rows+1):
            y = TRACK_ROW_SIZE * i + self.trackPosition
            dc.DrawLine(27, y, 124, y)
            dc.DrawLine(127, y, MAX_WIDTH-127, y)
        for i in range(1, MAX_WIDTH/(TRACK_COL_SIZE-1)):
            x = i * TRACK_COL_SIZE + 125
            dc.DrawLine(x, self.trackPosition, x, self.trackPosition+self.trackHeight)

        if self.id == selectedTrack:
            rect = wx.Rect(1, self.trackPosition+1, MAX_WIDTH-2, self.trackHeight-2)
            gc.SetPen(wx.Pen("#BBBBBB", 1.5))
            gc.SetBrush(wx.Brush(TRACKS_BACKGROUND_COLOUR, style=wx.TRANSPARENT))
            gc.DrawRoundedRectangle(rect[0], rect[1], rect[2], rect[3], 3)

        dc.SetTextForeground("#FFFFFF")
        rect = wx.Rect(0, self.trackPosition, 25, self.trackHeight)
        dc.DrawLabel(str(self.id), rect, wx.ALIGN_CENTER)    

        dc.SetTextForeground(FXBOX_FOREGROUND_COLOUR)
        for i, inputBut in enumerate(self.buttonsInputs):
            rect = inputBut.getRect()
            gc.DrawBitmap(buttonBitmap, rect[0], rect[1], rect[2], rect[3])
            dc.DrawLabel(inputBut.name, rect, wx.ALIGN_CENTER)

        for i, button in enumerate(self.buttonsFxs):
            rect = button.getRect()
            if button.isEnable():
                gc.DrawBitmap(buttonBitmap, rect[0], rect[1], rect[2], rect[3])
            else:
                gc.DrawBitmap(disableButtonBitmap, rect[0], rect[1], rect[2], rect[3])
            dc.DrawLabel(button.name, rect, wx.ALIGN_CENTER)    

        dc.SetPen(wx.Pen("#222222", 1))
        y = self.trackPosition + self.trackHeight
        dc.DrawLine(0, y, MAX_WIDTH, y)
 
    def getSaveDict(self):
        dict = {}
        dict["fxsValues"] = []
        for i, button in enumerate(self.buttonsFxs):
            dict["fxsValues"].append(button.getSaveDict())
            
        dict["inputValues"] = []
        for i, inputBut in enumerate(self.buttonsInputs):
            dict["inputValues"].append(inputBut.getSaveDict())

        dict["trackPosition"] = self.trackPosition
        dict["trackHeight"] = self.trackHeight
        dict["rows"] = self.rows
        dict["cols"] = self.cols
        return dict
        
    def setSaveDict(self, saveDict):
        self.rows = saveDict["rows"]
        self.cols = len(saveDict["fxsValues"]) # saveDict["cols"]
        self.trackPosition = saveDict.get("trackPosition", 0)
        self.trackHeight = saveDict.get("trackHeight", TRACK_ROW_SIZE * 2)
        self.createButtons()
        for i, button in enumerate(self.buttonsFxs):
            button.setSaveDict(saveDict["fxsValues"][i])
        for i, inputBut in enumerate(self.buttonsInputs):
            inputBut.setSaveDict(saveDict["inputValues"][i])
            
    def cueEvent(self, eventDict):
        for i, button in enumerate(self.buttonsFxs):
            button.cueEvent(eventDict)
        for i, inputBut in enumerate(self.buttonsInputs):
            inputBut.cueEvent(eventDict)
