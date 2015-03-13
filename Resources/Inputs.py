#!/usr/bin/python
# encoding: utf-8
import wx, os
from constants import *
from pyo import *
from ModuleParent import *

class InputIn(ModuleParent):
    name = "input"
    def __init__(self):
        ModuleParent.__init__(self)
        self.removeDryWet()
        self.setName("input")

        #ctrls
        self.ctrlGain = SliderParameter(name="gain", value=4, min=-90, max=24, 
                                        unit="db", exp=1)
        self.addParameter(self.ctrlGain)
        
        #audio
        self.dbValue = DBToA(self.ctrlGain)
        self.amp = Sig(self.input, mul = self.dbValue)
        self.setOutput(self.amp)

class Soundfile(ModuleParent):
    name = "Soundfile"
    def __init__(self):
        ModuleParent.__init__(self)
        self.removeDryWet()
        self.setName("Soundfile")
                
        #ctrls
        self.path = PathParameter(name = "path")
        self.addParameter(self.path)
        
        self.speed = SliderParameter(name="speed", value=1, min=0.25, max=4, unit="")
        self.addParameter(self.speed)
        
        self.ctrlGain = SliderParameter(name="gain", value=4, min=-90, max=24, 
                                        unit="db", exp=1)
        self.addParameter(self.ctrlGain)

        self.playButton = ButtonParameter(name = "play")
        self.addParameter(self.playButton)
        
        self.stopButton = ButtonParameter(name = "stop")
        self.addParameter(self.stopButton)

        self.loopButton = ToggleParameter(name = "loop")
        self.addParameter(self.loopButton)

        #audio
        filepath = os.path.join(SOUNDS_PATH, "silence.wav")
        self.sfPlayer = SfPlayer(filepath, speed=self.speed, loop=False, 
                                 offset=0, interp=2, mul=1, add=0)
        self.path.setCallback(self.loadPath)
        self.playButton.setCallback(self.sfPlayer.play)
        self.stopButton.setCallback(self.sfPlayer.stop)
        self.loopButton.setCallback(self.setLoop)

        self.dbValue = DBToA(self.ctrlGain)
        self.amp = Sig(self.sfPlayer, mul = self.dbValue)
        self.setOutput(self.amp)

    def loadPath(self, path):
        self.sfPlayer.setPath(path)

    def setLoop(self, onOff):
        self.sfPlayer.setLoop(onOff)
        
class InputCreator:
    def __init__(self):
        self.classes = []

        ### ADD FXs HERE
        self.classes.append(InputIn)
        self.classes.append(Soundfile)

        self.buildNames()
        
    def buildNames(self):
        self.names = [cls.name for cls in self.classes]
        
    def getNames(self):
        return self.names
        
    def create(self, index):
        if index < len(self.classes):
            return self.classes[index]()
