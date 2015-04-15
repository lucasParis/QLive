#!/usr/bin/python
# encoding: utf-8
import wx, os
from constants import *
import  wx.lib.filebrowsebutton as filebrowse
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR
import  wx.lib.scrolledpanel as scrolled
from Widgets import *
import QLiveLib

class WidgetParent(wx.Panel):
    def __init__(self, parameter, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.parameter = parameter
        
    def setValue(self, value):
        pass
        
class SliderWidget(WidgetParent):
    def __init__(self, parameter, parent):
        WidgetParent.__init__(self, parameter, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.slider = QLiveControlKnob(self, parameter.min, parameter.max, 
                                       parameter.getParameterValue(), label=parameter.name,
                                       outFunction=parameter.setParameterValue)
        self.sizer.Add(self.slider, 0, wx.ALL, 5)
        
        self.interpKnob = QLiveControlKnob(self,INTERPTIME_MIN, INTERPTIME_MAX, 
                                       parameter.getInterpTime(), label=parameter.name,
                                       outFunction=self.interpolationTimeCallback, backColour = CONTROLSLIDER_BACK_COLOUR_INTERP)
        # INTERP add another knob for interpolation time, toggle between display of value knob and interp knob
        self.sizer.Add(self.interpKnob, 0, wx.ALL, 5)

        self.interpKnob.Hide()
        self.SetSizer(self.sizer)
        
    def setValue(self, value):
        self.slider.SetValue(value)
        
    def setParameterInterpolationTime(self, value):
        self.interpKnob.SetValue(value)

        
    def interpolationTimeCallback(self, value):
        self.parameter.setInterpTime(value)
        
    def setShowMorph(self, bool):
        if bool:
            self.slider.Hide()
            self.interpKnob.Show()
        else:
            self.slider.Show()
            self.interpKnob.Hide()
            
        self.Layout()
        
class PathWidget(WidgetParent):
    def __init__(self, parameter, parent):
        WidgetParent.__init__(self, parameter, parent)

        self.callback = parameter.setValue
                
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fbb = filebrowse.FileBrowseButton(self, -1, labelText="Path", 
                                               size=(400,-1), fileMode=wx.OPEN, 
                                               fileMask=AUDIO_FILE_WILDCARD,
                                               initialValue=parameter.getValue(),
                                               changeCallback=self.pathCallback)
        self.fbb.SetBackgroundColour(BACKGROUND_COLOUR)
        
        self.sizer.Add(self.fbb, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.sizer)

    def pathCallback(self, evt):
        path = evt.GetString()
        if os.path.isfile(path):
            self.callback(path)

    def setValue(self, value):
        self.ffb.SetValue(value, callBack=1)
               
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
        self.button = wx.ToggleButton(self, label=parameter.name)
        self.button.Bind(wx.EVT_TOGGLEBUTTON, self.buttonEvent)

        self.setValue(parameter.getValue())

        self.sizer.Add(self.button, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer)
         
    def buttonEvent(self, event):
        self.callback(self.button.GetValue())
        
    def setValue(self, value):
        self.button.SetValue(value)
               
def WidgetCreator(type):
    dict = {}
    dict["slider"] = SliderWidget
    dict["path"] = PathWidget 
    dict["button"] = ButtonWidget  
    dict["toggle"] = ToggleWidget
    return dict[type]  

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
        
        # INTERP add button for setInterpTime mode, to show only interpKnobs
        
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
        for param in self.parameters:
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
                self.buttonSizer.Add(butt, 0, wx.EXPAND | wx.ALL, 2)
            elif param.type == "toggle":
                butt = WidgetCreator(param.type)(param, self.panel)
                self.widgets.append(butt)
                self.buttonSizer.Add(butt, 0, wx.EXPAND | wx.ALL, 2)

        self.sizer.Add(self.buttonSizer, 0, wx.EXPAND)
        self.panel.SetSizer(self.sizer)
        self.SetTitle(self.audio.name)

        frameSizer = wx.BoxSizer(wx.HORIZONTAL)
        frameSizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizerAndFit(frameSizer) 
        self.SetMinSize(self.GetSize())
    
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.Show()
        
    def showMorphEvent(self, evt):
        for widget in self.widgets:
            if isinstance(widget, SliderWidget):
                widget.setShowMorph(self.interpButton.GetValue())

    def enableFx(self, evt):
        self.audio.setEnable(evt.GetInt())
        QLiveLib.getVar("FxTracks").refresh()
            
    def refresh(self):
        for i, param in enumerate(self.parameters):
            if param.type == "slider":
                self.widgets[i].setValue(param.getParameterValue())
                self.widgets[i].setParameterInterpolationTime(param.getInterpTime())

            else:
                self.widgets[i].setValue(param.getValue())
                
    def onClose(self, evt):
        index = self.parent.openViews.index(self)
        self.parent.openViews.pop(index)
        self.Destroy()

class FxViewManager(object):
    def __init__(self, parent):
        self.openViews = []
        
    def openViewForAudioProcess(self, audioProcess):
        for view in self.openViews:
            if view.audio == audioProcess:
                view.Raise()
                return
        view = FxSlidersView(self, audioProcess)
        self.openViews.append(view)
        
    def refresh(self):
        for view in self.openViews:
            view.refresh()

    def closeAll(self):
        for view in self.openViews:
            view.Destroy()
