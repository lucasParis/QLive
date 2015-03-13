import wx, time, os, pprint
from constants import *
import QLiveLib
from AudioServer import AudioServer
from AudioMixer import AudioMixer
from FxTracks import FxTracks
from CuesPanel import CuesPanel
from MixerPanel import MixerPanel

class MainWindow(wx.Frame):
    def __init__(self, pos, size):
        wx.Frame.__init__(self, None, pos=pos, size=size)
        
        self.SetMinSize((600, 400))

        self.audioServer = AudioServer()
        self.audioServer.start() ### Need a way to start/stop the audio backend

        # menubar
        menubar = wx.MenuBar()
        menu1 = wx.Menu()

        menu1.Append(wx.ID_NEW, "New\tCtrl+N")
        self.Bind(wx.EVT_MENU, self.onNew, id=wx.ID_NEW)        
        menu1.Append(wx.ID_SAVE, "Save\tCtrl+S")
        self.Bind(wx.EVT_MENU, self.onSave, id=wx.ID_SAVE)        
        menu1.Append(wx.ID_OPEN, "Open\tCtrl+O")
        self.Bind(wx.EVT_MENU, self.onLoad, id=wx.ID_OPEN)
        menu1.AppendSeparator()
        quitItem = menu1.Append(wx.ID_EXIT, "Quit\tCtrl+Q")
        self.Bind(wx.EVT_MENU, self.OnClose, quitItem)
        menubar.Append(menu1, 'file')
        
        self.SetMenuBar(menubar)
        # end of menubar

        self.audioMixer = AudioMixer()

        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        self.tracks = FxTracks(self.mainPanel)
        self.tracks.connectAudioMixer(self.audioMixer)
        self.cues = CuesPanel(self.mainPanel)
        QLiveLib.setVar("CuesPanel", self.cues)
        self.mixer = MixerPanel(self.mainPanel, self.audioMixer)

        self.topCuesAndRestSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.topCuesAndRestSizer.Add(self.cues, 0, wx.EXPAND, 5)
        self.topCuesAndRestSizer.Add(self.tracks, 1, wx.EXPAND, 5)

        self.mainMixerVsRest = wx.BoxSizer(wx.VERTICAL)
        self.mainMixerVsRest.AddSizer(self.topCuesAndRestSizer, 2, wx.EXPAND, 5)
        self.mainMixerVsRest.Add(self.mixer, 0, wx.EXPAND, 5)
        self.mainPanel.SetSizer(self.mainMixerVsRest)
        
        self.Show()

    def onNew(self, evt):
        # if self.modified:
        #     ask for saving
        self.loadFile(NEW_FILE_PATH)

    def onSave(self, evt):
        dlg = wx.FileDialog(self, "Save Qlive Projet", 
                            os.path.expanduser("~"), "",
                            "QLive Project files (*.qlp)|*.qlp",
                            style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            
            dictSave = {}
            dictSave["tracks"] = self.tracks.getSaveDict()
            dictSave["cues"] = self.cues.getSaveDict()
            dictSave["mixer"] = self.mixer.getSaveDict()

            with open(path, "w") as f:
                f.write(QLIVE_MAGIC_LINE)
                f.write("### %s ###\n" % APP_VERSION)
                f.write("dictSave = %s" % pprint.pformat(dictSave, indent=4))
        dlg.Destroy()

    def loadFile(self, path):
        with open(path, "r") as f:
            magicline = f.readline()
        if magicline != QLIVE_MAGIC_LINE:
            print "The file loaded is not a valid QLive file."
            return
        execfile(path, globals())
        QLiveLib.PRINT("opening: ", dictSave)
        self.tracks.setSaveDict(dictSave["tracks"]) # there's a bug here... (on new)
        self.cues.setSaveDict(dictSave["cues"])
        self.mixer.setSaveDict(dictSave["mixer"])
        
    def onLoad(self, evt):
        dlg = wx.FileDialog(self, "Open Qlive Projet", 
                            os.path.expanduser("~"), "",
                            "QLive Project files (*.qlp)|*.qlp",
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.loadFile(path)
        dlg.Destroy()

    def OnClose(self, evt):
        self.tracks.fxsView.closeAll()
        self.audioServer.stop()
        time.sleep(0.25)
        self.audioServer.shutdown()
        time.sleep(0.25)
        self.Destroy()
