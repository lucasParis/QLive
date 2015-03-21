#!/usr/bin/env python
# encoding: utf-8
import wx
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR, VuMeter
from AudioMixer import *
from constants import *
import QLiveLib

class QLiveControlSlider(ControlSlider):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), 
                 size=(200,16), log=False, outFunction=None, integer=False, 
                 powoftwo=False, backColour=None, orient=wx.HORIZONTAL, 
                 linkedObject=None):
        ControlSlider.__init__(self, parent, minvalue, maxvalue, init, pos, 
                               size, log, self.localOutFunction, integer, powoftwo, 
                               backColour, orient)
        self.channelobject = None
        self.midiscanning = False
        self.linkedObject = None
        self.externalOutFunction = outFunction
        self.midiscan = MidiLearn(self.getMidiScan)
        self.Bind(wx.EVT_RIGHT_DOWN, self.MouseRightDown)
 
    def localOutFunction(self, value):
        if self.linkedObject:
            self.linkedObject.SetValue(value)
        self.externalOutFunction(value)

    def setLinkedObject(self, obj):
        self.linkedObject = obj

    def setChannelObject(self, obj):
        self.channelobject = obj

    def MouseRightDown(self, evt):
        if evt.ShiftDown():
            self.setMidiCtl(None)
            self.channelobject.stopMidiCtl()
            return
        if not self.midiscanning:
            self.midiscanning = True
            self.midiscan.scan()
            self.setBackgroundColour(MIDILEARN_COLOUR)
        else:
            self.midiscanning = False
            self.midiscan.stop()
            self.setBackgroundColour(BACKGROUND_COLOUR)
            
    def getMidiScan(self, ctlnum, midichnl):
        self.setMidiCtl(ctlnum)
        self.channelobject.setMidiCtl(ctlnum)
        self.setBackgroundColour(BACKGROUND_COLOUR)
        
class MixerPanel(wx.Panel):
    def __init__(self, parent, audioMixer):
        wx.Panel.__init__(self, parent, size=(800,200), style=wx.SUNKEN_BORDER)
        self.audioMixer = audioMixer
        self.SetBackgroundColour(BACKGROUND_COLOUR)

        self.fileFormat = 0
        self.sampleType = 0
        self.inputLinked = False
        self.outputLinked = False
        self.inputSliders = []
        self.outputSliders = []
        self.inputMeters = []
        self.outputMeters = []
        
        ### INPUT SECTION
        inputBox = wx.BoxSizer(wx.VERTICAL)        
        inputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        inputBox.AddSpacer((-1,5))
        inputBox.Add(wx.StaticText(self, label="Input Channels"), 0, wx.LEFT|wx.EXPAND, 10)
        inputBox.Add(wx.StaticLine(self, size=(1, -1)), 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.inlinked = wx.CheckBox(self, -1, "linked --->")
        self.inlinked.Bind(wx.EVT_CHECKBOX, self.linkInputs)
        inputBox.Add(self.inlinked, 0, wx.EXPAND|wx.LEFT, 10)
        for i in range(NUM_INPUTS):
            channel = self.audioMixer.getInputChannel(i)
            slide = QLiveControlSlider(self, -60, 18, 0, orient=wx.VERTICAL, 
                                       outFunction=channel.setVolume)
            slide.setChannelObject(channel)
            channel.setMidiCallback(slide.SetValue)
            self.inputSliders.append(slide)
            meter = VuMeter(self, size=(200,200), numSliders=1, orient=wx.VERTICAL)
            channel.setAmpCallback(meter.setRms)
            self.inputMeters.append(meter)
            if i % 2 == 0:
                inputSliderBox.Add(slide, 0, wx.ALL, 2)
                inputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
                inputSliderBox.AddSpacer(15)
            else:
                inputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
                inputSliderBox.Add(slide, 0, wx.ALL, 2)
                inputSliderBox.AddSpacer(15)
        inputBox.Add(inputSliderBox, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        
        separator = wx.StaticLine(self, size=(1, -1), style=wx.LI_VERTICAL)
        separator2 = wx.StaticLine(self, size=(1, -1), style=wx.LI_VERTICAL)

        #### OUTPUT SECTION
        outputBox = wx.BoxSizer(wx.VERTICAL)
        outputSliderBox = wx.BoxSizer(wx.HORIZONTAL)
        outputBox.AddSpacer((-1,5))
        outputBox.Add(wx.StaticText(self, label = "Output Channels"), 0, wx.LEFT|wx.EXPAND, 10)
        outputBox.Add(wx.StaticLine(self, size=(1, -1)), 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.outlinked = wx.CheckBox(self, -1, "linked --->")
        self.outlinked.Bind(wx.EVT_CHECKBOX, self.linkOutputs)
        outputBox.Add(self.outlinked, 0, wx.EXPAND|wx.LEFT, 10)
        for i in range(NUM_OUTPUTS):
            channel = self.audioMixer.getOutputChannel(i)            
            slide = QLiveControlSlider(self, -60, 18, 0, orient=wx.VERTICAL, 
                                       outFunction=channel.setVolume)
            slide.setChannelObject(channel)
            channel.setMidiCallback(slide.SetValue)
            self.outputSliders.append(slide)
            meter = VuMeter(self, size=(200,200), numSliders=1, orient=wx.VERTICAL)
            channel.setAmpCallback(meter.setRms)

            self.outputMeters.append(meter)
            if i % 2 == 0:
                outputSliderBox.Add(slide, 0, wx.ALL, 2)
                outputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
                outputSliderBox.AddSpacer(15)
            else:
                outputSliderBox.Add(meter, 0, wx.EXPAND|wx.ALL, 2)
                outputSliderBox.Add(slide, 0, wx.ALL, 2)
                outputSliderBox.AddSpacer(15)
                
        outputBox.Add(outputSliderBox, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)

        # RECORDING SECTION
        recordingBox = wx.BoxSizer(wx.VERTICAL)
        
        recordingBox.AddSpacer((-1,5))
        recordingBox.Add(wx.StaticText(self, -1, "Record Settings"), 0, wx.LEFT|wx.EXPAND, 10)
        recordingBox.Add(wx.StaticLine(self, size=(1, -1)), 0, wx.EXPAND|wx.ALL, 5)
        recordingBox.AddSpacer((-1, 5))
        recSettingsBox = wx.BoxSizer(wx.HORIZONTAL)
        fileformatBox = wx.BoxSizer(wx.VERTICAL)
        fileformatText = wx.StaticText(self, -1, "File Format")
        fileformatBox.Add(fileformatText, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 5)
        self.pop_fileformat = wx.Choice(self, -1, choices=EXPORT_FORMATS, size=(80,-1))
        self.pop_fileformat.SetSelection(0)
        fileformatBox.Add(self.pop_fileformat, 0, wx.LEFT | wx.RIGHT, 5)
        sampletypeBox = wx.BoxSizer(wx.VERTICAL)
        sampletypeText = wx.StaticText(self, -1, "Sample Type")
        sampletypeBox.Add(sampletypeText, 0, wx.CENTER  | wx.LEFT | wx.RIGHT, 5)
        self.pop_sampletype = wx.Choice(self, -1, choices=EXPORT_TYPES)
        self.pop_sampletype.SetSelection(0)
        sampletypeBox.Add(self.pop_sampletype, 0, wx.LEFT | wx.RIGHT, 5)
        recSettingsBox.Add(fileformatBox, 0, wx.RIGHT | wx.BOTTOM, 5)
        recSettingsBox.Add(sampletypeBox, 0, wx.RIGHT | wx.BOTTOM, 5)
        recordingBox.Add(recSettingsBox, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        recordingBox.AddSpacer((-1, 5))

        rec1Box = wx.BoxSizer(wx.HORIZONTAL)

        self.tx_rec_folder = wx.TextCtrl( self, -1, "~/Desktop", size=(120, -1))
        rec1Box.Add(self.tx_rec_folder, 0, wx.LEFT, 5)
        self.but_folder = wx.ToggleButton(self, -1, "Choose", size=(65,-1))
        rec1Box.Add(self.but_folder, 0, wx.ALIGN_CENTER)

        rec2Box = wx.BoxSizer(wx.HORIZONTAL)

        self.tx_output = wx.TextCtrl( self, -1, "qlive_rec", size=(120, -1))
        rec2Box.Add(self.tx_output, 0, wx.LEFT, 5)
        self.tog_record = wx.ToggleButton(self, -1, "Start Rec", size=(65,-1))
        rec2Box.Add(self.tog_record, 0, wx.ALIGN_CENTER)
        
        recordingBox.Add(wx.StaticText(self, -1, "Destination"), 0, wx.LEFT, 6)
        recordingBox.Add(rec1Box, 0, wx.BOTTOM  | wx.RIGHT, 5)
        recordingBox.AddSpacer((-1, 5))
        recordingBox.Add(wx.StaticText(self, -1, "Filename"), 0, wx.LEFT, 6)
        recordingBox.Add(rec2Box, 0, wx.BOTTOM | wx.RIGHT, 5)

        self.pop_fileformat.Bind(wx.EVT_CHOICE, self.setFileFormat)
        self.pop_sampletype.Bind(wx.EVT_CHOICE, self.setSampleType)
        self.tx_output.Bind(wx.EVT_CHAR, self.handleOutput)
        self.tx_rec_folder.Bind(wx.EVT_CHAR, self.handleOutput)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.handleRecord, self.tog_record)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.chooseRecFolder, self.but_folder)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(inputBox, 1, wx.EXPAND)
        mainSizer.Add(separator, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(outputBox, 1, wx.EXPAND)
        mainSizer.Add(separator2, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(recordingBox, 0)
        self.SetSizer(mainSizer)

    def linkInputs(self, evt=None, set=None):
        if set is not None:
            if set:
                self.inputLinked = False
            else:
                self.inputLinked = True
        if self.inputLinked == False:
            self.inputLinked = True
            for i, sl in enumerate(self.inputSliders):
                if i%2 == 0:
                    sl.setLinkedObject(self.inputSliders[i+1])
        else:
            self.inputLinked = False
            for i, sl in enumerate(self.inputSliders):
                if i%2 == 0:
                    sl.setLinkedObject(None)

    def linkOutputs(self, evt=None, set=None):
        if set is not None:
            if set:
                self.outputLinked = False
            else:
                self.outputLinked = True
        if self.outputLinked == False:
            self.outputLinked = True
            for i, sl in enumerate(self.outputSliders):
                if i%2 == 0:
                    sl.setLinkedObject(self.outputSliders[i+1])
        else:
            self.outputLinked = False
            for i, sl in enumerate(self.outputSliders):
                if i%2 == 0:
                    sl.setLinkedObject(None)

    def getSaveDict(self):
        dict = {} 
        inputSliderValues = []
        inputSliderCtls = []
        for slide in self.inputSliders:
            inputSliderValues.append(slide.GetValue())
            inputSliderCtls.append(slide.getMidiCtl())
        dict["inputSliderValues"] = inputSliderValues
        dict["inputSliderCtls"] = inputSliderCtls

        outputSliderValues = []
        outputSliderCtls = []
        for slide in self.outputSliders:
            outputSliderValues.append(slide.GetValue())
            outputSliderCtls.append(slide.getMidiCtl())
        dict["outputSliderValues"] = outputSliderValues
        dict["outputSliderCtls"] = outputSliderCtls
        dict["inputLinked"] = self.inputLinked
        dict["outputLinked"] = self.outputLinked
        dict["fileFormat"] = self.fileFormat
        dict["sampleType"] = self.sampleType
        dict["outputDestination"] = self.tx_rec_folder.GetValue()
        dict["outputFilename"] = self.tx_output.GetValue()

        return dict
        
    def setSaveDict(self, dict):
        for i, slide in enumerate(self.inputSliders):
            val = dict["inputSliderValues"][i]
            ctl = dict["inputSliderCtls"][i]
            slide.SetValue(val)
            slide.setMidiCtl(ctl)
            self.audioMixer.getInputChannel(i).setMidiCtl(ctl)
            self.audioMixer.getInputChannel(i).setMidiCtlValue(val)
        for i, slide in enumerate(self.outputSliders):
            val = dict["outputSliderValues"][i]
            ctl = dict["outputSliderCtls"][i]
            slide.SetValue(val)
            slide.setMidiCtl(ctl)
            self.audioMixer.getOutputChannel(i).setMidiCtl(ctl)
            self.audioMixer.getOutputChannel(i).setMidiCtlValue(val)
        inlink = dict.get("inputLinked", False)
        outlink = dict.get("outputLinked", False)
        self.inlinked.SetValue(inlink)
        self.outlinked.SetValue(outlink)
        self.linkInputs(set=inlink)
        self.linkOutputs(set=outlink)
        self.setFileFormat(set=dict.get("fileFormat", 0))
        self.setSampleType(set=dict.get("sampleType", 0))
        outputDestination = dict.get("outputDestination", "~/Desktop")
        self.tx_rec_folder.SetValue(outputDestination)
        outputFilename = dict.get("outputFilename", "qlive_rec")
        self.tx_output.SetValue(outputFilename)

    def setFileFormat(self, evt=None, set=None):
        if set is not None:
            self.fileFormat = set
            self.pop_fileformat.SetSelection(set)
        else:
            self.fileFormat = evt.GetInt()

    def setSampleType(self, evt=None, set=None):
        if set is not None:
            self.sampleType = set
            self.pop_sampletype.SetSelection(set)
        else:
            self.sampleType = evt.GetInt()

    def handleOutput(self, evt):
        key = evt.GetKeyCode()
        if key == wx.WXK_TAB or key == wx.WXK_RETURN:
            QLiveLib.getVar("FxTracks").SetFocus()
        evt.Skip()

    def handleRecord(self, evt):
        if evt.GetInt() == 1:
            folder = self.tx_rec_folder.GetValue()
            if folder.startswith("~"):
                folder = folder.replace("~", os.path.expanduser("~"), 1)
            if os.path.isdir(folder):
                filename = os.path.join(folder, self.tx_output.GetValue())
            else:
                filename = self.tx_output.GetValue()
            QLiveLib.getVar("AudioServer").recStart(filename, self.fileFormat, self.sampleType)
            self.tog_record.SetLabel('Stop Rec')
        else:
            self.tog_record.SetLabel('Start Rec')
            QLiveLib.getVar("AudioServer").recStop()

    def chooseRecFolder(self, evt):
        dlg = wx.DirDialog(self, 
                           message="Choose a folder to record QLive's output sound...",
                           defaultPath=os.path.expanduser("~"))
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.tx_rec_folder.SetValue(QLiveLib.ensureNFD(path))
        dlg.Destroy()
        self.but_folder.SetValue(0)

if __name__ == "__main__":
    from pyo64 import *
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.Bind(wx.EVT_CLOSE, self.onClose)
            self.server = Server().boot().start()
            self.server.amp = 0.1
            self.mixer = AudioMixer()
            self.panel = MixerPanel(self, self.mixer)
            self.SetSize(self.panel.GetBestSize())
        def onClose(self, evt):
            self.server.stop()
            self.Destroy()
    app = wx.App()
    frame = TestWindow()
    frame.Show()
    app.MainLoop()
