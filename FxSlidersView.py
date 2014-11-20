#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from pyolib._wxwidgets import ControlSlider
import  wx.lib.scrolledpanel as scrolled

"""
- changed FxSlidersView from panel to Frame
"""
class FxSlidersToolBar(wx.ToolBar):
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, size = (1000, 40))
#        self.remRowButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
#        self.remRowButton.SetLabel("-")    
#        self.AddControl(wx.StaticText(self, label = "row"))
#        self.remRowButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
#        self.remRowButton.SetLabel("-")    
#        self.AddControl(self.remRowButton)
#        self.addRowButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
#        self.addRowButton.SetLabel("+")    
#        self.AddControl(self.addRowButton)
#        
#        self.AddControl(wx.StaticText(self, label = "column"))
#        self.remColButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
#        self.remColButton.SetLabel("-")    
#        self.AddControl(self.remColButton)
        self.addColButton = wx.Button(self, size = (300,-1), pos = (-1,-1))
        self.addColButton.SetLabel("I am but a Tool")    
        self.AddControl(self.addColButton)

        self.Realize()
        
class FxSlidersView(wx.Frame):
    """
    take the audioprocess object (FxParent) and shows all that should be controlled 
    """
    def __init__(self, parent, audioProcess):
        wx.Frame.__init__(self, None)
        self.SetFocus()
        self.audio = audioProcess
        self.parameters = audioProcess.parameters
        
        self.panel = wx.Panel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = FxSlidersToolBar(self.panel)

        self.sizer.Add(self.toolbar,1, wx.EXPAND)
        ##init CTRLS
        sliders = []
        for i, param in enumerate(self.parameters):
            slide = ControlSlider(self.panel, param.min, param.max, param.audioValue.get(), outFunction = param.setValue)
            self.sizer.Add(wx.StaticText(self.panel, label = param.name), 0, wx.EXPAND | wx.ALL, 5)
            self.sizer.Add(slide, 0, wx.EXPAND | wx.ALL, 2)
            
        self.panel.SetSizer(self.sizer)
        self.SetTitle(self.audio.name)
#        self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeave)
#        
    def onLeave(self, event):
        print "leaver"
        pass
#        self.Show(True)

if __name__ == "__main__":
    from Fxs import FxCreator
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s = Server().boot()
            self.s.start()
            self.fx = FxCreator().createFx(0)
            self.fx.setInput(Input([0,1]))
            self.fx.getOutput().out()
            
            self.view = FxSlidersView(self, self.fx)
            self.view.Show(True)
            print "delloh"
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()