#!/usr/bin/env python
# encoding: utf-8
import wx
import wx.grid

class ActionMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.actions = ["None", "Play", "Stop"]
        self.idsIndexDict = {}
        for i, name in enumerate(self.actions):
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

class SoundFilePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour((140,140,140))
#        self.sizerGrid = wx.GridSizer(3,4)
#        self.sizerGrid.AddMany([
#                                (wx.StaticText(self), wx.EXPAND),
#                                (wx.StaticText(self, label = "soundfile"), wx.EXPAND),                              
#                                (wx.StaticText(self, label = "action"), wx.EXPAND)
#                                ])      
#        self.SetSizer(self.sizerGrid)
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(4,2)
        self.grid.SetColLabelValue(0, "soundfile")
        self.grid.SetColLabelValue(1, "action")
        self.grid.GetGridWindow().Bind(wx.EVT_RIGHT_DOWN,self.onRightClick)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.grid, 2, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.grid.AutoSize()

    def onRightClick(self, event):
        x, y = self.grid.CalcUnscrolledPosition(event.GetX(), event.GetY())
        row, col = self.grid.XYToCell(x, y)
        if(col == 1):
            menu = ActionMenu(self)
            self.PopupMenu(menu, event.GetPosition())
        print row , col

if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.panel = SoundFilePanel(self)

    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()