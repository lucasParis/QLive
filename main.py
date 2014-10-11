#!/usr/bin/python
# simple.py

import __builtin__
__builtin__.QLIVE_APP_OPENED = True

import wx
from pyo import *




class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size = (1200, 700))
        pass
#        self.fx = FxLibLowpass()
#        

#        
#        self.cuesView = wx.Panel(self)
#        self.chainsView = wx.Panel(self)
#        self.fxView = FxParametersView(self.fx, self)        
#        #sizer
#        self.sizerTop = wx.BoxSizer(wx.HORIZONTAL)
#        self.sizerTop.Add(self.cuesView,1)        
#        self.sizerTop.Add(self.chainsView,1)        
#        self.sizerTop.Add(self.fxView,2, wx.EXPAND)                    
#        self.SetSizer(self.sizerTop)
#        self.slider = ControlSlider(self)

        

if __name__ == "__main__":
    app = wx.App()

#    fx = FxLibLowpass
    frame = MainWindow()
#    view = FxParametersView(fx)
    frame.Show()

    app.MainLoop()
