#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from FxBox import *
import  wx.lib.scrolledpanel as scrolled


class FxTrack(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)
        
#        self.sizer = wx.GridBagSizer()
        self.buttonWidth = 80
        self.buttonHeight = 25
        self.connectionWidth = self.buttonWidth/10.
        self.connectionHeight = self.buttonHeight-8
        
        self.SetBackgroundColour(wx.Colour(100, 100, 100))
        cols = 5
        rows = 1
        self.buttons = []
        for i in range(rows):
            col = []
            for j in range(cols):
                but = FxBox(self)
                but.setId((j,i))
                col.append(but)
            self.buttons.append(col)
                
        self.SetSize((10+cols*100+10, 20+30+20))
        self.SetVirtualSize((10+cols*(self.buttonWidth+20)+10, 20+30+20))
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
        id = self.positionToId(pos)
        print id

    def leftClicked(self, event):
        pos = self.CalcUnscrolledPosition( event.GetPosition())
        id = self.positionToId(pos)
        if id[1] < len(self.buttons): #valid row
            if id[0] < len(self.buttons[id[1]]): #valid column
                buttonPos = self.idToPosition(id)
                if event.LeftDown():
                    if pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.connectionWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
                        pass
                        #input connection
                    elif pos[0] > buttonPos[0] + self.connectionWidth - self.buttonWidth and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
                        pass
                        #output connection
                    elif pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
                        self.buttons[id[1]][id[0]].buttonClicked(event)
                        if event.ShiftDown():
                            pass
                            #move effect to new position
                    
        
    def rightClicked(self, event):
        pos = self.CalcUnscrolledPosition( event.GetPosition() )
        id = self.positionToId(pos)
        if id[1] < len(self.buttons): #Y
            if id[0] < len(self.buttons[id[1]]): #X
                buttonPos = self.idToPosition(id)
                if pos[0] > buttonPos[0] and pos[0] < buttonPos[0] + self.buttonWidth and pos[1] > buttonPos[1] and pos[1] < buttonPos[1] + self.buttonHeight:
                    self.buttons[id[1]][id[0]].rightClicked(event)
                    self.Refresh()
        
    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        w, h = self.GetSize()
        dc.SetTextForeground("#000000")
#        dc.DrawRectangle(10,10,30,30)
        for i, row in enumerate(self.buttons):
            for j, button in enumerate(row):
                pos = self.idToPosition(button.getId())
                rect = wx.Rect(pos[0], pos[1], self.buttonWidth, self.buttonHeight)#(10+i*100,20)
                dc.DrawRoundedRectangleRect(rect, 5)
                rectIn = wx.Rect(pos[0], pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)#(10+i*100,20)
                rectOut = wx.Rect(pos[0]+(self.buttonWidth*9)/10., pos[1]+4, self.buttonWidth/10., self.buttonHeight-8)#(10+i*100,20)

                dc.DrawRoundedRectangleRect(rectIn, 2)
                dc.DrawRoundedRectangleRect(rectOut, 2)

                dc.DrawLabel(button.name, rect, wx.ALIGN_CENTER)

    def idToPosition(self, id):
        return (10+id[0]*100, id[1]*50+20)

    def positionToId(self, position):
        return (int((position[0]-10)/100.), int((position[1]-20)/50.))
                
    def onSize(self, event):
        pass

if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.fxTrack = FxTrack(self)


    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()