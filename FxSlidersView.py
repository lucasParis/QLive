#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from pyolib._wxwidgets import ControlSlider
import  wx.lib.scrolledpanel as scrolled

"""
- changed FxSlidersView from panel to Frame
"""
class WidgetParent(wx.Panel):
    def __init__(self, parameter, parent):
        wx.Panel.__init__(self, parent)
        self.parameter = parameter
        pass
        
    def setValue(self, value):
        pass
        
class SliderWidget(WidgetParent):
    def __init__(self, parameter, parent):
        WidgetParent.__init__(self, parameter, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.slider = ControlSlider(self, parameter.min, parameter.max, parameter.audioValue.get(), outFunction = parameter.setValue)
        self.sizer.Add(wx.StaticText(self, label = parameter.name), 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.slider, 0, wx.EXPAND | wx.ALL, 5)
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
        dlg = wx.FileDialog(self, "choose Qlive projet", '', '', ".", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
#            print path
            self.callback(path)
        dlg.Destroy()
        
    def setValue(self, value):
        pass        
  
def WidgetCreator(type):
    dict = {}
    dict["slider"] = SliderWidget
    dict["path"] = PathWidget  
    return dict[type]  
    
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

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = FxSlidersToolBar(self.panel)

        self.sizer.Add(self.toolbar,1, wx.EXPAND)
        ##init CTRLS
        self.widgets = []
        for i, param in enumerate(self.parameters):
            if param.type == "slider":
                slider = WidgetCreator(param.type)(param, self.panel)
                self.widgets.append(slider)
                self.sizer.Add(slider, 0, wx.EXPAND | wx.ALL, 2)
            elif param.type == "path":
                path = WidgetCreator(param.type)(param, self.panel)
                self.widgets.append(path)
                self.sizer.Add(path, 0, wx.EXPAND | wx.ALL, 2)
#                boxy = BoxSizer(wx.HORIZONTAL)
#                boxy.A
            
        self.panel.SetSizer(self.sizer)
        self.SetTitle(self.audio.name)
#        self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeave)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def refresh(self):
#        print "refreshing"
        for i, param in enumerate(self.parameters):
#            print "setting value:", param.getValue()
            self.widgets[i].setValue(param.getValue())

            
    def onLeave(self, event):
        print "leaver"
        pass
#        self.Show(True)

    def onClose(self, evt):
        # remove from the list here...
        index = self.parent.openViews.index(self)
        print "deleting", index
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