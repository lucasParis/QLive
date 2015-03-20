from pyo import *

class AudioServer:
    def __init__(self):
        self.server = Server(buffersize=64)
        self.server.setMidiInputDevice(99)
        self.server.boot()

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()

    def shutdown(self):
        self.server.shutdown()

    def isStarted(self):
        return self.server.getIsStarted()

    def isBooted(self):
        return self.server.getIsBooted()

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
