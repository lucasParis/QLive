import time
from pyo64 import *
from constants import *
import QLiveLib

class AudioServer:
    def __init__(self):
        self.server = Server(buffersize=64)
        self.server.setMidiInputDevice(99)
        self.server.boot()

    def start(self, state):
        if state:
            QLiveLib.getVar("FxTracks").start()
            self.server.start()
        else:
            self.server.stop()

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
