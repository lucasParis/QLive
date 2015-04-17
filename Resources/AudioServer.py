import time
from pyo64 import *
from constants import *
import QLiveLib

class SoundFilePlayer:
    def __init__(self, id, filename):
        self.id = id
        self.filename = filename
        sndfolder = os.path.join(QLiveLib.getVar("projectFolder"), "sounds")        
        path = os.path.join(sndfolder, self.filename)
        self.table = SndTable(path)
        self.dbgain = SigTo(0, time=0.02, init=0)
        self.gain = DBToA(self.dbgain)
        self.looper = Looper(self.table, mul=self.gain).stop()
        self.directout = False
        self.mixerInputId = -1

    def setAttributes(self, dict):
        self.looper.mode = dict[ID_COL_LOOPMODE]
        self.looper.pitch = dict[ID_COL_TRANSPO]
        self.dbgain.value = dict[ID_COL_GAIN]
        self.looper.start = dict[ID_COL_STARTPOINT]
        self.looper.dur = dict[ID_COL_ENDPOINT] - dict[ID_COL_STARTPOINT]
        self.looper.xfade = dict[ID_COL_CROSSFADE]
        if dict[ID_COL_PLAYING]:
            self.looper.reset()
            self.looper.play()
            if dict[ID_COL_DIRECTOUT] and not self.directout:
                self.directout = True
                audioMixer = QLiveLib.getVar("AudioMixer")
                for i in range(len(self.looper)):
                    chnl = (i + dict[ID_COL_CHANNEL]) % NUM_CHNLS
                    self.mixerInputId = audioMixer.addToMixer(chnl, self.looper[i])
            elif not dict[ID_COL_DIRECTOUT] and self.directout:
                self.directout = False
                audioMixer = QLiveLib.getVar("AudioMixer").delFromMixer(self,mixerInputId)
        else:
            self.looper.stop()

    def setAttribute(self, id, value):
        if id == ID_COL_LOOPMODE:
            self.looper.mode = value
        elif id == ID_COL_TRANSPO:
            self.looper.pitch = value
        elif id == ID_COL_GAIN:
            self.dbgain.value = value
        elif id == ID_COL_STARTPOINT:
            self.looper.start = value
        elif id == ID_COL_ENDPOINT:
            self.looper.dur = value - self.looper.start
        elif id == ID_COL_CROSSFADE:
            self.looper.xfade = value
        elif id == ID_COL_PLAYING:
            if value:
                self.looper.play()
            else:
                self.looper.stop()
        # handle ID_COL_PLAYING, ID_COL_DIRECTOUT and ID_COL_CHANNEL

class AudioServer:
    def __init__(self):
        self.server = Server(buffersize=64)
        self.server.setMidiInputDevice(99)
        self.server.boot()
        self.soundfiles = []

    def createSoundFilePlayers(self):
        objs = QLiveLib.getVar("Soundfiles").getSoundFileObjects()
        for obj in objs:
            id = obj.getId()
            filename = obj.getFilename()
            player = SoundFilePlayer(id, filename)
            player.setAttributes(obj.getAttributes())
            self.soundfiles.append(player)
            obj.setPlayerRef(player)

    def resetPlayerRefs(self):
        objs = QLiveLib.getVar("Soundfiles").getSoundFileObjects()
        for obj in objs:
            obj.setPlayerRef(None)

    def start(self, state):
        if state:
            self.createSoundFilePlayers()
            QLiveLib.getVar("FxTracks").start()
            self.server.start()
        else:
            self.server.stop()
            self.resetPlayerRefs()
            self.soundfiles = []

    def stop(self):
        self.server.stop()

    def shutdown(self):
        self.server.shutdown()

    def isStarted(self):
        return self.server.getIsStarted()

    def isBooted(self):
        return self.server.getIsBooted()

    def recStart(self, filename, fileformat=0, sampletype=0):
        self.server.recordOptions(fileformat=fileformat, sampletype=sampletype)
        filename, ext = os.path.splitext(filename)
        if fileformat >= 0 and fileformat < 8:
            ext = RECORD_EXTENSIONS[fileformat]
        else: 
            ext = ".wav"
        date = time.strftime('_%d_%b_%Y_%Hh%M')
        complete_filename = QLiveLib.toSysEncoding(filename+date+ext)
        self.server.recstart(complete_filename)

    def recStop(self):
        self.server.recstop()

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
