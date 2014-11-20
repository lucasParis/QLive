#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from FxBox import *
import  wx.lib.scrolledpanel as scrolled


class FxTrack(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)
        
        self.buttonWidth = 80
        self.buttonHeight = 25
        self.connectionWidth = self.buttonWidth/10.
        self.connectionHeight = self.buttonHeight-8
        
        self.SetBackgroundColour(wx.Colour(100, 100, 100))
        cols = 5
        rows = 1
        self.buttonsFxs = []
        self.buttonsInputs = []
        for i in range(rows):
            col = []
            for j in range(cols):
                but = FxBox(self)
                but.setId((j,i))
                col.append(but)
            self.buttonsFxs.append(col)
            but = InputBox(self)
            but.setId((0,i))
            self.buttonsInputs.append(but)
            
        self.SetSize((10+cols*100+10, 20+30+20))
        self.SetVirtualSize((10+(cols+1)*(self.buttonWidth+20)+10, 20+30+20))
        self.SetScrollRate(1,1)

        self.viewPanelRef = None # to open fxSlidersView
        
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.SetupScrolling(self)

        self.Bind(wx.EVT_LEFT_DOWN, self.leftClicked)
        self.Bind(wx.EVT_RIGHT_DOWN, self.rightClicked)
#        self.Bind(wx.EVT_MOTION, self.mouseMotion)

    def setViewPanelRef(self, ref):
        self.viewPanelRef = ref

    def mouseMotion(self, event):
        pos = self.CalcUnscrolledPosition( event.GetPosition())
        id = self.positionToIdFX(pos)
        
        print pos

    def leftClicked(self, event):
        pos = self.CalcUnscrolledPosition( event.GetPosition() )
        if pos[0] < 100: # inputs
            id = self.positionToIdInput(pos)
            if id[1] < len(self.buttonsInputs): #valid Y
                    buttonPos = self.idToPositionInput(id)
                    if pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
                        self.buttonsInputs[id[1]].openView()
#                        self.Refresh()
        else: #normal Fxs
            id = self.positionToIdFX(pos)
            if id[1] < len(self.buttonsFxs): #valid Y
                if id[0] < len(self.buttonsFxs[id[1]]): #valid X
                    buttonPos = self.idToPositionFX(id)
                    if pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
                        self.buttonsFxs[id[1]][id[0]].openView()
                        self.Refresh()
        
#        if id[1] < len(self.buttonsFxs): #valid row
#            if id[0] < len(self.buttonsFxs[id[1]]): #valid column
#                buttonPos = self.idToPositionFX(id)
#                if event.LeftDown():
#                    if pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.connectionWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
#                        pass
#                        #input connection
#                    elif pos[0] > buttonPos[0] + self.connectionWidth - self.buttonWidth and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
#                        pass
#                        #output connection
#                    elif pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
#                        print "grorof"

#                        self.buttonsFxs[id[1]][id[0]].openView(event)
#                        if event.ShiftDown():
#                            pass
#                            #move effect to new position
                    
        
    def rightClicked(self, event):
        pos = self.CalcUnscrolledPosition( event.GetPosition() )
        if pos[0] < 100: # inputs
            id = self.positionToIdInput(pos)
            print id
            if id[1] < len(self.buttonsInputs): #valid Y
                    buttonPos = self.idToPositionInput(id)
                    if pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
                        self.buttonsInputs[id[1]].openMenu(event)
                        self.Refresh()
        else: #normal Fxs
            id = self.positionToIdFX(pos)
            if id[1] < len(self.buttonsFxs): #valid Y
                if id[0] < len(self.buttonsFxs[id[1]]): #valid X
                    buttonPos = self.idToPositionFX(id)
                    if pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
                        self.buttonsFxs[id[1]][id[0]].openMenu(event)
                        self.Refresh()
        
    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        w, h = self.GetSize()
        dc.SetTextForeground("#000000")
#        dc.DrawRectangle(10,10,30,30)
        for i, row in enumerate(self.buttonsFxs):
            for j, button in enumerate(row):
                pos = self.idToPositionFX(button.getId())
                rect = wx.Rect(pos[0], pos[1], self.buttonWidth, self.buttonHeight)#(10+i*100,20)
                dc.DrawRoundedRectangleRect(rect, 5)
                rectIn = wx.Rect(pos[0], pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)#(10+i*100,20)
                rectOut = wx.Rect(pos[0]+(self.buttonWidth*9)/10., pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)#(10+i*100,20)

                dc.DrawRoundedRectangleRect(rectIn, 2)
                dc.DrawRoundedRectangleRect(rectOut, 2)

                dc.DrawLabel(button.name, rect, wx.ALIGN_CENTER)
    
        for i, inputBut in enumerate(self.buttonsInputs):
#            print i
            pos = self.idToPositionInput(inputBut.getId())
#            print pos
            rect = wx.Rect(pos[0], pos[1], self.buttonWidth, self.buttonHeight)
            dc.DrawRoundedRectangleRect(rect, 5)
#            rectIn = wx.Rect(pos[0], pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)
            rectOut = wx.Rect(pos[0]+(self.buttonWidth*9)/10., pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)

            dc.DrawRoundedRectangleRect(rectIn, 2)
            dc.DrawRoundedRectangleRect(rectOut, 2)

            dc.DrawLabel(inputBut.name, rect, wx.ALIGN_CENTER)


        rect = wx.Rect(0, 0, 100, 20)#(10+i*100,20)
        dc.DrawLabel("Inputs", rect, wx.ALIGN_CENTER)

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
        pass
        
    def setSaveDict(self, saveDict):
        # look into dict to see how many collums/rows, create necessary Boxes
        pass
if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s= Server().boot()
            self.fxTrack = FxTrack(self)


    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()