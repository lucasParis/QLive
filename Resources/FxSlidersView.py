#!/usr/bin/python
# encoding: utf-8
import wx, os
from pyo import *
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR
import  wx.lib.scrolledpanel as scrolled
from Widgets import *

"""
- changed FxSlidersView from panel to Frame
"""
class WidgetParent(wx.Panel):
    def __init__(self, parameter, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.parameter = parameter
        pass
        
    def setValue(self, value):
        pass
        
class SliderWidget(WidgetParent):
    def __init__(self, parameter, parent):
        WidgetParent.__init__(self, parameter, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.slider = QLiveControlKnob(self, parameter.min, parameter.max, 
                                       parameter.audioValue.get(), label=parameter.name,
                                       outFunction=parameter.setValue)
        self.sizer.Add(self.slider, 0, wx.ALL, 5)
        self.SetSizer(self.sizer)
        pass    
        
    def setValue(self, value):
        self.slider.SetValue(value)
        
class PathWidget(WidgetParent):
    def __init__(self, parameter, parent):
        WidgetParent.__init__(self, parameter, parent)

        self.callback = parameter.setValue
                
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.openButton = wx.Button(self, label = "open")
        self.openButton.Bind(wx.EVT_BUTTON, self.buttonEvent)


        self.text = wx.StaticText(self, label = "path")
        
        self.sizer.Add(self.openButton, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.text, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
         
    def buttonEvent(self, event):
        dlg = wx.FileDialog(self, "choose Qlive projet", os.path.expanduser("~"), style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.callback(path)
        dlg.Destroy()
        
    def setValue(self, value):
        pass 
               
class ButtonWidget(WidgetParent):
    def __init__(self, parameter, parent):
        WidgetParent.__init__(self, parameter, parent)

        self.callback = parameter.setValue
                
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.openButton = wx.Button(self, label = parameter.name)
        self.openButton.Bind(wx.EVT_BUTTON, self.buttonEvent)

        self.sizer.Add(self.openButton, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
         
    def buttonEvent(self, event):

        self.callback(1)
        
    def setValue(self, value):
        pass        
  
class ToggleWidget(WidgetParent):
    def __init__(self, parameter, parent):
        WidgetParent.__init__(self, parameter, parent)

        self.callback = parameter.setValue
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.openButton = wx.ToggleButton(self, label = parameter.name)
        self.openButton.Bind(wx.EVT_TOGGLEBUTTON, self.buttonEvent)

        self.sizer.Add(self.openButton, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
         
    def buttonEvent(self, event):
        print "vent"
        self.callback(self.openButton.GetValue())
        
    def setValue(self, value):
        self.openButton.SetValue(value)
               
def WidgetCreator(type):
    dict = {}
    dict["slider"] = SliderWidget
    dict["path"] = PathWidget 
    dict["button"] = ButtonWidget  
    dict["toggle"] = ToggleWidget  

    return dict[type]  
    
# What is its purpose?
class FxSlidersToolBar(wx.ToolBar):
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, size = (1000, 40))
        self.SetBackgroundColour(BACKGROUND_COLOUR)
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
        self.addColButton = wx.Button(self, size = (-1,-1), pos = (-1,-1))
        self.addColButton.SetLabel("Tool")    
        self.AddControl(self.addColButton)

        self.Realize()
        
class FxSlidersView(wx.Frame):
    """
    take the audioprocess object (FxParent) and shows all that should be controlled 
    """
    def __init__(self, parent, audioProcess):
        wx.Frame.__init__(self, None)
        self.parent = parent
        self.menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        closeitem = menu1.Append(wx.ID_ANY, "Close\tCtrl+W")
        self.Bind(wx.EVT_MENU, self.onClose, closeitem)
        self.menuBar.Append(menu1, 'File')
        self.SetMenuBar(self.menuBar)

        self.audio = audioProcess
        self.parameters = audioProcess.parameters
        
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BACKGROUND_COLOUR)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = FxSlidersToolBar(self.panel)
        self.sizer.Add(self.toolbar, 0, wx.EXPAND)

        ##init CTRLS
        self.widgets = []
        self.knobSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.knobSizer, 0, wx.EXPAND)
        for i, param in enumerate(self.parameters):
            if param.type == "slider":
                slider = WidgetCreator(param.type)(param, self.panel)
                self.widgets.append(slider)
                self.knobSizer.Add(slider, 0, wx.EXPAND | wx.ALL, 2)
            elif param.type == "path":
                path = WidgetCreator(param.type)(param, self.panel)
                self.widgets.append(path)
                self.sizer.Add(path, 0, wx.EXPAND | wx.ALL, 2)
            elif param.type == "button":
                butt = WidgetCreator(param.type)(param, self.panel)
                self.widgets.append(butt)
                self.sizer.Add(butt, 0, wx.EXPAND | wx.ALL, 2)
            elif param.type == "toggle":
                butt = WidgetCreator(param.type)(param, self.panel)
                self.widgets.append(butt)
                self.sizer.Add(butt, 0, wx.EXPAND | wx.ALL, 2)

        self.panel.SetSizer(self.sizer)
        self.SetTitle(self.audio.name)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.Show()

    def refresh(self):
        for i, param in enumerate(self.parameters):
            self.widgets[i].setValue(param.getValue())

    def onClose(self, evt):
        index = self.parent.openViews.index(self)
        self.parent.openViews.pop(index)
        self.Destroy()

if __name__ == "__main__":
    from Fxs import FxCreator
    from Inputs import InputCreator
    from FxDialogsManager import FxDialogsManager
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s = Server().boot()
            self.s.start()
            self.fx = InputCreator().create(1)
            self.fx.setInput(Input([0,1]))
            self.fx.getOutput().out()
            self.fxs = FxDialogsManager(self)    
            self.fxs.openViewForAudioProcess(self.fx)
#            self.fxs.openViewForAudioProcess(self.fx)
#            self.fxs.openViewForAudioProcess(self.fx)

#            self.view = FxSlidersView(self, self.fx)
#            self.view.Show(True)
            print "delloh"

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()