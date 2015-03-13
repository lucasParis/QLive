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
