#!/usr/bin/python
# encoding: utf-8
import wx
from pyo import *
from MixerPanel import *
#from FxBox import *
#import  wx.lib.scrolledpanel as scrolled

def dump():
    pass

class MidiLearn:
    def __init__(self, callback):
        self.callback = callback
        self.scanner = CtlScan2(self.scanned, False).stop()
    
    def scan(self):
        self.scanner.reset()
        self.scanner.play()

    def stop(self):
        self.scanner.stop()

    def scanned(self, ctlnum, midichnl):
        self.callback(ctlnum, midichnl)
        self.scanner.stop()

class AudioChannel:
    def __init__(self):
        self.midicallback = None
        self.oldMidiValue = 9999999
        self.midictl = Midictl(128, -80, 12).stop()
        self.midictl.setInterpolation(False)
        self.midipat = Pattern(self.midiout, time=0.06)
        self.input = Sig(0)
        self.inVolume = SigTo(0, init = 0)
        self.inDB = DBToA(self.inVolume)
        self.out = Sig(self.input, mul = self.inDB)
        self.ampOut = PeakAmp(self.out)

    def midiout(self):
        val = self.midictl.get()
        if self.midicallback != None and val != self.oldMidiValue:
            self.midicallback(val)
            self.oldMidiValue = val

    def setMidiCallback(self, callback):
        self.midicallback = callback

    def setMidiCtl(self, ctlnum):
        if ctlnum != None:
            self.midictl.setCtlNumber(ctlnum)
            self.midictl.play()
            self.midipat.play()

    def stopMidiCtl(self):
        self.midictl.setCtlNumber(128)
        self.midictl.stop()
        self.midipat.stop()
 
    def setMidiCtlValue(self, value):
        self.midictl.setValue(value)

    def setInput(self, input):
        self.input.setValue(input)
        
    def getOutput(self):
        return self.out
        
    def setVolume(self, value):
        self.inVolume.setValue(value)
        
    def setAmpCallback(self, call):
        self.ampOut.function = call

    def onQuit(self):
        self.midipat.function = dump

class AudioMixer:
    def __init__(self):
#        self.inVolumes = Sig([0 for i in range(2)])
#        self.inDb = DBToA(self.inVolumes)
#        
#        self.outVolumes = Sig([0 for i in range(2)])
#        self.outDb = DBToA(self.outVolumes)

        self.inChannels = []
        for i in range(2):
            channel = AudioChannel()
            channel.setInput(Input(i))
            self.inChannels.append(channel)
        
        self.outChannels = []
        for i in range(2):
            channel = AudioChannel()
            channel.getOutput().out()
            self.outChannels.append(channel)

    def getInputChannel(self, index):
        if index < len(self.inChannels):
            return self.inChannels[index]
        else:
            return None

    def getOutputChannel(self, index):
        if index < len(self.outChannels):
            return self.outChannels[index]
        else:
            return None

    def onQuit(self):
        for channel in self.inChannels:
            channel.onQuit()
        for channel in self.outChannels:
            channel.onQuit()
            
if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.s= Server().boot()
            self.s.start()
            self.mixer = AudioMixer()
            self.panel = MixerPanel(self, self.mixer)
#            self.fxTrack = FxTrack(self)


    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()