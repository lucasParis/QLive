#!/usr/bin/python
# encoding: utf-8
import wx
from constants import *
from FxBox import *
import  wx.lib.scrolledpanel as scrolled

class FxTrack(scrolled.ScrolledPanel):
    def __init__(self, parent, viewPanelRef):
        scrolled.ScrolledPanel.__init__(self, parent)
        
        self.buttonWidth = 80
        self.buttonHeight = 25
        self.connectionWidth = self.buttonWidth/10.
        self.connectionHeight = self.buttonHeight-8
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self.SetBackgroundColour(wx.Colour(100, 100, 100))
        self.cols = 5
        self.rows = 1
        self.createButtons()
        self.createConnections()

        self.SetSize((10+self.cols*100+10, 20+30+20))
        self.SetVirtualSize((10+(self.cols+1)*(self.buttonWidth+20)+10, 20+30+20))
        self.SetScrollRate(1,1)
        self.SetupScrolling(self)

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

    def createConnections(self):
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                if j == len(row)-1:
                    button.setInput(row[j-1].getOutput())
                elif j != 0:
                    button.setInput(row[j-1].getOutput())
                else:
                    button.setInput(self.buttonsInputs[0].getOutput())
        # test case
        self.outputTest = self.buttonsFxs[0][4].getOutput().out()

    def connectAudioMixer(self, audioMixer):
        for but in self.buttonsInputs:
            but.setInput([audioMixer.getInputChannel(i).getOutput() for i in range(NUM_CHNLS)])
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                if j == len(row)-1:
                    output = button.getOutput()
                    [audioMixer.getOutputChannel(k).setInput(output[k]) for k in range(NUM_CHNLS)]

    def mouseMotion(self, event):
        pass
        #pos = self.CalcUnscrolledPosition( event.GetPosition())
        #id = self.positionToIdFX(pos)
                
    def leftClicked(self, event):
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
        dc = self.dcref(self)
        gc = wx.GraphicsContext_Create(dc)
        dc.Clear()
        self.PrepareDC(dc)

        w, h = self.GetSize()
        dc.SetTextForeground(FXBOX_FOREGROUND_COLOUR)
        gc.SetPen(wx.Pen(FXBOX_OUTLINE_COLOUR, 1, wx.SOLID))
        gc.SetBrush(wx.Brush(FXBOX_BACKGROUND_COLOUR, wx.SOLID))
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                pos = self.idToPositionFX(button.getId())
                rect = wx.Rect(pos[0], pos[1], self.buttonWidth, self.buttonHeight)
                rectIn = wx.Rect(pos[0], pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)
                rectOut = wx.Rect(pos[0]+self.buttonWidth*9/10., pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)
                gc.DrawRoundedRectangle(rect[0], rect[1], rect[2], rect[3], 5)
                gc.DrawRoundedRectangle(rectIn[0], rectIn[1], rectIn[2], rectIn[3], 2)
                gc.DrawRoundedRectangle(rectOut[0], rectOut[1], rectOut[2], rectOut[3], 2)

                dc.DrawLabel(button.name, rect, wx.ALIGN_CENTER)
    
        for i, inputBut in enumerate(self.buttonsInputs):
            pos = self.idToPositionInput(inputBut.getId())
            rect = wx.Rect(pos[0], pos[1], self.buttonWidth, self.buttonHeight)
            rectOut = wx.Rect(pos[0]+(self.buttonWidth*9)/10., pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)
            gc.DrawRoundedRectangle(rect[0], rect[1], rect[2], rect[3], 5)
            gc.DrawRoundedRectangle(rectOut[0], rectOut[1], rectOut[2], rectOut[3], 2)

            dc.DrawLabel(inputBut.name, rect, wx.ALIGN_CENTER)

        dc.SetTextForeground("#FFFFFF")
        dc.DrawLabel("Inputs", wx.Rect(0, 0, 100, 20), wx.ALIGN_CENTER)
        dc.DrawLabel("Fxs", wx.Rect(100, 0, 100, 20), wx.ALIGN_CENTER)

        dc.DrawLine(100, 0, 100, h)

    def idToPositionFX(self, id):
        return (10+(id[0]+1)*100, (id[1])*50+20)

    def positionToIdFX(self, position):
        return (int((position[0]-10)/100.)-1, int((position[1]-20)/50.))
             
    def idToPositionInput(self, id):
        return (10, (id[1])*50+20)

    def positionToIdInput(self, position):
        return (int((position[0]-10)/100.), int((position[1]-20)/50.))
                   
    def onSize(self, event):
        pass
        
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
        print saveDict
        self.rows = len(saveDict["fxsValues"])
        self.cols = len(saveDict["fxsValues"][0])
        self.createButtons()
        self.createConnections()
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                button.setSaveDict(saveDict["fxsValues"][i][j])
        for i, inputBut in enumerate(self.buttonsInputs):
            inputBut.setSaveDict(saveDict["inputValues"][i])
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