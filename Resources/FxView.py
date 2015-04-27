#!/usr/bin/python
# encoding: utf-8
import wx, os
from constants import *
from pyolib._wxwidgets import BACKGROUND_COLOUR
from Widgets import *
import QLiveLib

class SliderWidget(wx.Panel):
    def __init__(self, parent, parameters, fxbox):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.fromUser = False
        self.parameters = parameters
        self.fxbox = fxbox
        self.name = parameters[0]
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.slider = QLiveControlKnob(self, parameters[2], parameters[3], 
                                       parameters[1], label=parameters[0],
                                       log=parameters[5],
                                       outFunction=self.outputValue)
        self.sizer.Add(self.slider, 0, wx.ALL, 5)
        
        self.interpKnob = QLiveControlKnob(self,INTERPTIME_MIN, INTERPTIME_MAX, 
                                       0.01, label=parameters[0], log=True,
                                       outFunction=self.outputInterpValue, 
                                       backColour = CONTROLSLIDER_BACK_COLOUR_INTERP)
        self.sizer.Add(self.interpKnob, 0, wx.ALL, 5)

        self.interpKnob.Hide()
        self.SetSizer(self.sizer)
        
    def outputValue(self, value):
        self.fxbox.setParamValue(self.name, value, self.fromUser)
        self.fromUser = True

    def setValue(self, value, propagate=False):
        self.fromUser = False
        self.slider.SetValue(value, propagate)
     
    def getValue(self):
        return self.slider.GetValue()

    def outputInterpValue(self, value):
        self.fxbox.setInterpValue(self.name, value)

    def setInterpValue(self, value, propagate=False):
        self.interpKnob.SetValue(value, propagate)

    def getInterpValue(self):
        return self.interpKnob.GetValue()

    def setShowMorph(self, bool):
        if bool:
            self.slider.Hide()
            self.interpKnob.Show()
        else:
            self.slider.Show()
            self.interpKnob.Hide()
        self.Layout()

class FxSlidersView(wx.Frame):
    """
    take the audioprocess object (FxParent) and shows all that should be controlled 
    """
    def __init__(self, parent, fxbox, parameters):
        style = wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT
        wx.Frame.__init__(self, parent, style=style)
        self.parent = parent
        self.fxbox = fxbox
        self.parameters = parameters
        self.last_enable = 1

        self.menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        closeitem = menu1.Append(wx.ID_ANY, "Close\tCtrl+W")
        self.Bind(wx.EVT_MENU, self.onClose, closeitem)
        self.menuBar.Append(menu1, 'File')
        self.SetMenuBar(self.menuBar)

        tabId = wx.NewId()
        self.prevId = wx.NewId()
        self.nextId = wx.NewId()
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL,  wx.WXK_TAB, tabId),
                                        (wx.ACCEL_NORMAL,  wx.WXK_LEFT, self.prevId),
                                        (wx.ACCEL_NORMAL,  wx.WXK_RIGHT, self.nextId)])
        self.SetAcceleratorTable(accel_tbl)
        
        self.Bind(wx.EVT_MENU, self.onTabulate, id=tabId)
        self.Bind(wx.EVT_MENU, self.onMoveCue, id=self.prevId, id2=self.nextId)
        
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BACKGROUND_COLOUR)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.headSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.knobSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.interpButton = wx.ToggleButton(self.panel, -1)
        self.interpButton.SetLabel("Morph Time")
        self.interpButton.Bind(wx.EVT_TOGGLEBUTTON, self.showMorphEvent)

        self.headSizer.Add(self.interpButton, 0, wx.TOP|wx.LEFT, 7)
        
        self.headSizer.AddStretchSpacer(1)

        self.enable = wx.CheckBox(self.panel, -1, "Enable FX:", style=wx.ALIGN_RIGHT)
        self.enable.SetValue(1)
        self.enable.Bind(wx.EVT_CHECKBOX, self.enableFx)
        self.headSizer.Add(self.enable, 0, wx.TOP|wx.RIGHT, 7)
        

        self.sizer.Add(self.headSizer, 0, wx.EXPAND)
        self.sizer.Add(self.knobSizer, 0, wx.EXPAND)

        ##init CTRLS
        self.widgets = []
        for param in self.parameters["ctrls"]:
            slider = SliderWidget(self.panel, param, fxbox)
            self.widgets.append(slider)
            self.knobSizer.Add(slider, 0, wx.EXPAND | wx.ALL, 2)

        self.sizer.Add(self.buttonSizer, 0, wx.EXPAND)
        self.panel.SetSizer(self.sizer)
        self.SetTitle(self.fxbox.name)

        frameSizer = wx.BoxSizer(wx.HORIZONTAL)
        frameSizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizerAndFit(frameSizer) 
        self.SetMinSize(self.GetSize())
    
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onTabulate(self, evt):
        QLiveLib.getVar("FxTracks").setSelectedTrack()

    def onMoveCue(self, evt):
        if QLiveLib.getVar("CanProcessCueKeys"):
            cues = QLiveLib.getVar("CuesPanel")
            current = cues.getCurrentCue()
            if evt.GetId() == self.prevId:
                if cues.setSelectedCue(current - 1):
                    cues.sendCueEvent()
            elif evt.GetId() == self.nextId:
                if cues.setSelectedCue(current + 1):
                    cues.sendCueEvent()

    def showMorphEvent(self, evt):
        for widget in self.widgets:
            if isinstance(widget, SliderWidget):
                widget.setShowMorph(self.interpButton.GetValue())

    def enableFx(self, evt):
        self.fxbox.setEnable(evt.GetInt(), fromUser=True)
        QLiveLib.getVar("FxTracks").drawAndRefresh()

    def setEnableState(self, x):
        self.enable.SetValue(x)
        if x != self.last_enable:
            self.last_enable = x
            QLiveLib.getVar("FxTracks").drawAndRefresh()

    def getWidgets(self):
        return self.widgets
                
    def onClose(self, evt):
        self.Hide()
