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
        self.SetBackgroundColour(wx.Colour(100, 100, 100))
        cols = 5
        rows = 1
        self.buttons = []
        for i in range(cols):
            for j in range(rows):
                but = FxBox(self)
                but.setPosition((10+i*100,20))
                self.buttons.append(but)
                
        self.SetSize((10+cols*100+10, 20+30+20))
        self.SetVirtualSize((10+cols*(self.buttonWidth+20)+10, 20+30+20))
        self.SetScrollRate(1,1)

        self.viewPanelRef = None # to open fxSlidersView
        
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.SetupScrolling(self)

        self.Bind(wx.EVT_LEFT_DOWN, self.buttonClicked)
        self.Bind(wx.EVT_RIGHT_DOWN, self.rightClicked)

    def setViewPanelRef(self, ref):
        self.viewPanelRef = ref


    def buttonClicked(self, event):
        pos = self.CalcUnscrolledPosition( event.GetPosition() )
        for i, button in enumerate(self.buttons):
            if pos[0] > button.position[0] and pos[0] < button.position[0] + self.buttonWidth and pos[1] > button.position[1] and pos[1] < button.position[1] + 30:
                button.buttonClicked(event)
        
    def rightClicked(self, event):
        pos = self.CalcUnscrolledPosition( event.GetPosition() )
        for i, button in enumerate(self.buttons):
            if pos[0] > button.position[0] and pos[0] < button.position[0] + self.buttonWidth and pos[1] > button.position[1] and pos[1] < button.position[1] + 30:
                button.rightClicked(event)
                self.Refresh()
        
    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        w, h = self.GetSize()
        dc.SetTextForeground("#000000")
#        dc.DrawRectangle(10,10,30,30)
        for i, button in enumerate(self.buttons):
            rect = wx.Rect(button.position[0], button.position[1], self.buttonWidth, 30)
            dc.DrawRoundedRectangleRect(rect, 5)
            dc.DrawLabel(button.name, rect, wx.ALIGN_CENTER)


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