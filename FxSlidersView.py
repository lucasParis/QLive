#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from pyolib._wxwidgets import ControlSlider


class FxSlidersView(wx.Panel):
    """
    take the audioprocess object (FxParent) and shows all that should be controlled 
    """
    def __init__(self, parent, audioProcess):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.audio = audioProcess
        self.parameters = audioProcess.parameters
        sliders = []
        for i, param in enumerate(self.parameters):
            slide = ControlSlider(self, param.min, param.max, param.audioValue.get(), outFunction = param.setValue)
            self.sizer.Add(slide)
            
        self.SetSizer(self.sizer)

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
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()