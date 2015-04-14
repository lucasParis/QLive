#!/usr/bin/python
# encoding: utf-8
import wx
from constants import *
from FxBox import *
import wx.lib.scrolledpanel as scrolled
import Resources.QLiveLib as QLiveLib


class FxTrack(wx.ScrolledWindow):
    def __init__(self, parent, viewPanelRef, id = 0):
        wx.ScrolledWindow.__init__(self, parent)
        
        self.trackID = id        

        self.buttonWidth = 80
        self.buttonHeight = 25
        self.connectionWidth = self.buttonWidth/10.
        self.connectionHeight = self.buttonHeight-8
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        if self.trackID%2:
            self.SetBackgroundColour(TRACKS_BACKGROUND_COLOUR)
        else:
            self.SetBackgroundColour(TRACKS_BACKGROUND_COLOUR2)            
        self.cols = 5
        self.rows = 1
        self.createButtonBitmap()
        self.createButtonBitmap(False)
        self.createButtons()
        #self.createConnections()

        self.SetVirtualSize((10+(self.cols+1)*(self.buttonWidth+20)+10, 1000))
        w, h = self.GetVirtualSize()
        self.SetScrollbars(20, 20, w/20, h/20, 0, 0, False)

        self.viewPanelRef = viewPanelRef # to open fxSlidersView
        
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)

        self.Bind(wx.EVT_LEFT_DOWN, self.leftClicked)
        self.Bind(wx.EVT_RIGHT_DOWN, self.rightClicked)
        self.Bind(wx.EVT_MOTION, self.mouseMotion)

        if PLATFORM == "win32":
            self.dcref = wx.BufferedPaintDC
        else:
            self.dcref = wx.PaintDC

    def createButtonBitmap(self, enable=True):
        w, h = self.buttonWidth, self.buttonHeight
        b = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(b)
        dc.SetPen(wx.Pen(TRACKS_BACKGROUND_COLOUR, 1))
        dc.SetBrush(wx.Brush(TRACKS_BACKGROUND_COLOUR))
        dc.DrawRectangle(0, 0, w, h)
        gc = wx.GraphicsContext_Create(dc)
        gc.SetPen(wx.Pen(FXBOX_OUTLINE_COLOUR, 1, wx.SOLID))
        if enable:
            gc.SetBrush(wx.Brush(FXBOX_ENABLE_BACKGROUND_COLOUR, wx.SOLID))
        else:
            gc.SetBrush(wx.Brush(FXBOX_DISABLE_BACKGROUND_COLOUR, wx.SOLID))
        rect = wx.Rect(0, 0, w, h)
        rectIn = wx.Rect(0, 4, w/10., h-8)
        rectOut = wx.Rect(w*9/10., 4, w/10., h-8)
        gc.DrawRoundedRectangle(rect[0], rect[1], rect[2], rect[3], 5)
        gc.DrawRoundedRectangle(rectIn[0], rectIn[1], rectIn[2], rectIn[3], 2)
        gc.DrawRoundedRectangle(rectOut[0], rectOut[1], rectOut[2], rectOut[3], 2)
        dc.SelectObject(wx.NullBitmap)
        if enable:
            self.buttonBitmap = b
        else:
            self.disableButtonBitmap = b

    def createButtons(self):
        self.buttonsFxs = []
        self.buttonsInputs = []
        for i in range(self.rows):
            col = []
            for j in range(self.cols):
                but = FxBox(self)
                but.setId((j,i))
                col.append(but)
            self.buttonsFxs.append(col)
            but = InputBox(self)
            but.setId((0,i))
            self.buttonsInputs.append(but)

    def start(self):
        self.createConnections()

    def createConnections(self):
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                if j == 0:
                    button.setInput(self.buttonsInputs[i].getOutput())
                else:
                    button.setInput(row[j-1].getOutput())
        self.connectAudioMixer()

    def connectAudioMixer(self):
        audioMixer = QLiveLib.getVar("AudioMixer")
        # not supposed to be called every time
        # Connections should be handled more dynamically...
        #audioMixer.resetMixer()
        for but in self.buttonsInputs:
            but.setInput([audioMixer.getInputChannel(i).getOutput() for i in range(NUM_CHNLS)])
        for i, row in enumerate(self.buttonsFxs):
            for obj in row:
                if obj.name == "MonoOut":
                    audioMixer.addToMixer(0, row[-1].getOutput())
                if obj.name == "StereoOut":
                    audioMixer.addToMixer(0, row[-1].getOutput()[0])
                    audioMixer.addToMixer(1, row[-1].getOutput()[1])

    def refresh(self):
        wx.CallAfter(self.Refresh)

    def mouseMotion(self, event):
        pass
        #pos = self.CalcUnscrolledPosition( event.GetPosition())
        #id = self.positionToIdFX(pos)
                
    def leftClicked(self, event):
        self.trackSelected()
        pos = self.CalcUnscrolledPosition( event.GetPosition() )
        if pos[0] < 100: # inputs
            id = self.positionToIdInput(pos)
            if id[1] < len(self.buttonsInputs): # valid Y
                    buttonPos = self.idToPositionInput(id)
                    butRect = wx.Rect(buttonPos[0], buttonPos[1], self.buttonWidth, self.buttonHeight)
                    if butRect.Contains(pos):
                        self.buttonsInputs[id[1]].openView()
        else: # normal Fxs
            id = self.positionToIdFX(pos)
            if id[1] < len(self.buttonsFxs): # valid Y
                if id[0] < len(self.buttonsFxs[id[1]]): # valid X
                    buttonPos = self.idToPositionFX(id)
                    butRect = wx.Rect(buttonPos[0], buttonPos[1], self.buttonWidth, self.buttonHeight)
                    if butRect.Contains(pos):
                        self.buttonsFxs[id[1]][id[0]].openView()
                else:
                    but = FxBox(self)
                    but.setId((len(self.buttonsFxs[0]),0))
                    self.buttonsFxs[0].append(but)
                    wx.CallAfter(self.Refresh)

    def rightClicked(self, event):
        pos = self.CalcUnscrolledPosition( event.GetPosition() )
        if pos[0] < 100: # inputs
            id = self.positionToIdInput(pos)
            if id[1] < len(self.buttonsInputs): # valid Y
                    buttonPos = self.idToPositionInput(id)
                    butRect = wx.Rect(buttonPos[0], buttonPos[1], self.buttonWidth, self.buttonHeight)
                    if butRect.Contains(pos):
                        self.buttonsInputs[id[1]].openMenu(event)
                        wx.CallAfter(self.Refresh)
        else: # normal Fxs
            id = self.positionToIdFX(pos)
            if id[1] < len(self.buttonsFxs): # valid Y
                if id[0] < len(self.buttonsFxs[id[1]]): # valid X
                    buttonPos = self.idToPositionFX(id)
                    butRect = wx.Rect(buttonPos[0], buttonPos[1], self.buttonWidth, self.buttonHeight)
                    if butRect.Contains(pos):
                        self.buttonsFxs[id[1]][id[0]].openMenu(event)
                        wx.CallAfter(self.Refresh)
        
    def onPaint(self, event):
        w, h = self.GetSize()
        dc = self.dcref(self)
        gc = wx.GraphicsContext_Create(dc)
        dc.Clear()
        self.PrepareDC(dc)


        dc.SetTextForeground(FXBOX_FOREGROUND_COLOUR)

        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                pos = self.idToPositionFX(button.getId())
                rect = wx.Rect(pos[0], pos[1], self.buttonWidth, self.buttonHeight)
                if button.isEnable():
                    gc.DrawBitmap(self.buttonBitmap, rect[0], rect[1], rect[2], rect[3])
                else:
                    gc.DrawBitmap(self.disableButtonBitmap, rect[0], rect[1], rect[2], rect[3])
                dc.DrawLabel(button.name, rect, wx.ALIGN_CENTER)    
        for i, inputBut in enumerate(self.buttonsInputs):
            pos = self.idToPositionInput(inputBut.getId())
            rect = wx.Rect(pos[0], pos[1], self.buttonWidth, self.buttonHeight)
            gc.DrawBitmap(self.buttonBitmap, rect[0], rect[1], rect[2], rect[3])
            dc.DrawLabel(inputBut.name, rect, wx.ALIGN_CENTER)

        dc.SetTextForeground("#FFFFFF")
        dc.DrawLabel("Inputs", wx.Rect(0, 0, 100, 20), wx.ALIGN_CENTER)
        dc.DrawLabel("Fxs", wx.Rect(100, 0, 100, 20), wx.ALIGN_CENTER)

        dc.DrawLine(100, 0, 100, 1000)
        dc.DrawLine(0, 0, w, 0)


    def idToPositionFX(self, id):
        return (10+(id[0]+1)*100, (id[1])*50+20)

    def positionToIdFX(self, position):
        return (int((position[0]-10)/100.)-1, int((position[1]-20)/50.))
             
    def idToPositionInput(self, id):
        return (10, (id[1])*50+20)

    def positionToIdInput(self, position):
        return (int((position[0]-10)/100.), int((position[1]-20)/50.))
                   
    def onSize(self, event):
        event.Skip()
        
    def getSaveDict(self):
        #build dict with values, corresponding effect index, and index in matrix
        dict = {}
        matrix = []
        for i, row in enumerate(self.buttonsFxs):
            rowList = []
            for j, button in enumerate(row):
                rowList.append(button.getSaveDict())
            matrix.append(rowList)
            
        dict["inputValues"] = []
        for i, inputBut in enumerate(self.buttonsInputs):
            dict["inputValues"].append(inputBut.getSaveDict())

        dict["fxsValues"] = matrix
        dict["rows"] = self.rows
        dict["cols"] = self.cols
        return dict
        
    def setSaveDict(self, saveDict):
        #resize according to dict row col size
        self.rows = len(saveDict["fxsValues"])
        self.cols = len(saveDict["fxsValues"][0])
        self.createButtons()
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                button.setSaveDict(saveDict["fxsValues"][i][j])
        for i, inputBut in enumerate(self.buttonsInputs):
            inputBut.setSaveDict(saveDict["inputValues"][i])
        #self.createConnections()
        wx.CallAfter(self.Refresh)

    def loadCue(self, cue):
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                pass
        for i, inputBut in enumerate(self.buttonsInputs):
            pass
#        self.track.loadCue(cue)
        
    def copyCue(self, cueToCopy):
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                pass
        for i, inputBut in enumerate(self.buttonsInputs):
            pass
            
    def cueEvent(self, eventDict):
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                button.cueEvent(eventDict)
        for i, inputBut in enumerate(self.buttonsInputs):
            inputBut.cueEvent(eventDict)
            
    def trackSelected(self):
        QLiveLib.getVar("FxTracks").setActiveTrack(self.trackID)
#        self.SetBackgroundColour(TRACKS_BACKGROUND_COLOUR_HIGHLIGHTED)
#        self.Refresh()
        
    def setSelected(self, value):
        if value:
            self.SetBackgroundColour(TRACKS_BACKGROUND_COLOUR_HIGHLIGHTED)
        else:
            if self.trackID%2:
                self.SetBackgroundColour(TRACKS_BACKGROUND_COLOUR)
            else:
                self.SetBackgroundColour(TRACKS_BACKGROUND_COLOUR2)    
        self.Refresh()

        
    def setID(self, id):
        self.trackID = id

if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s= Server().boot()
            self.s.start()
            self.fxTrack = FxTrack(self)
    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()