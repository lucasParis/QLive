import wx, time, os, pprint, copy, codecs
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
        self.SetTitle("QLive Session")
    
        self.audioServer = AudioServer()
        self.audioServer.start() ### Need a way to start/stop the audio backend

        self.currentProject = ""
        self.saveState = None

        # menubar
        menubar = wx.MenuBar()
        menu1 = wx.Menu()

        menu1.Append(wx.ID_NEW, "New\tCtrl+N")
        self.Bind(wx.EVT_MENU, self.onNew, id=wx.ID_NEW)        
        menu1.Append(wx.ID_OPEN, "Open\tCtrl+O")
        self.Bind(wx.EVT_MENU, self.onLoad, id=wx.ID_OPEN)
        # Open Recent here (when prefs and tmp directory added)

        self.submenu1 = wx.Menu()
        ID_OPEN_RECENT = 2000
        recentFiles = []
        filename = QLiveLib.ensureNFD(OPEN_RECENT_PATH)
        if os.path.isfile(filename):
            f = codecs.open(filename, "r", encoding="utf-8")
            for line in f.readlines():
                recentFiles.append(line.replace("\n", ""))
            f.close()
        if recentFiles:
            for file in recentFiles:
                self.submenu1.Append(ID_OPEN_RECENT, file)
                self.Bind(wx.EVT_MENU, self.openRecent, id=ID_OPEN_RECENT)
                ID_OPEN_RECENT += 1
        menu1.AppendMenu(1999, "Open Recent...", self.submenu1)

        menu1.AppendSeparator()
        menu1.Append(wx.ID_CLOSE, "Close\tCtrl+W")
        self.Bind(wx.EVT_MENU, self.onClose, id=wx.ID_CLOSE)        
        menu1.Append(wx.ID_SAVE, "Save\tCtrl+S")
        self.Bind(wx.EVT_MENU, self.onSave, id=wx.ID_SAVE)        
        menu1.Append(wx.ID_SAVEAS, "Save As...\tShift+Ctrl+S")
        self.Bind(wx.EVT_MENU, self.onSaveAs, id=wx.ID_SAVEAS)
        if PLATFORM != "darwin":
            menu1.AppendSeparator()
        prefItem = menu1.Append(wx.ID_PREFERENCES, "Preferences...\tCtrl+;")
        self.Bind(wx.EVT_MENU, self.openPrefs, prefItem)
        if PLATFORM != "darwin":
            menu1.AppendSeparator()
        quitItem = menu1.Append(wx.ID_EXIT, "Quit\tCtrl+Q")
        self.Bind(wx.EVT_MENU, self.OnClose, quitItem)
        menubar.Append(menu1, 'File')
        
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
        
        self.loadFile(NEW_FILE_PATH)

        self.Show()

    def getCurrentState(self):
        dictSave = {}
        dictSave["tracks"] = self.tracks.getSaveDict()
        dictSave["cues"] = self.cues.getSaveDict()
        dictSave["mixer"] = self.mixer.getSaveDict()
        return dictSave

    def saveFile(self, path):
        dictSave = self.getCurrentState()
        with open(path, "w") as f:
            f.write(QLIVE_MAGIC_LINE)
            f.write("### %s ###\n" % APP_VERSION)
            f.write("dictSave = %s" % pprint.pformat(dictSave, indent=4))

    def loadFile(self, path):
        with open(path, "r") as f:
            magicline = f.readline()
        if magicline != QLIVE_MAGIC_LINE:
            print "The file loaded is not a valid QLive file."
            return
        self.tracks.fxsView.closeAll()
        execfile(path, globals())
        QLiveLib.PRINT("opening: ", dictSave)
        if path == NEW_FILE_PATH:
            self.currentProject = ""
        else:
            self.currentProject = path
            self.newRecent(path)
        self.saveState = copy.deepcopy(dictSave)
        self.tracks.setSaveDict(dictSave["tracks"])
        self.cues.setSaveDict(dictSave["cues"])
        self.mixer.setSaveDict(dictSave["mixer"])

    def askForSaving(self):
        state = True
        if self.saveState != self.getCurrentState():
            msg = 'file %s has been modified. Do you want to save?' % self.currentProject
            dlg = wx.MessageDialog(None, msg, 'Warning!', wx.YES | wx.NO | wx.CANCEL)
            but = dlg.ShowModal()
            if but == wx.ID_YES:
                self.onSave(None)
            elif but == wx.ID_CANCEL:
                state = False
            dlg.Destroy()
        return state
        
    def onNew(self, evt):
        if self.askForSaving():
            self.loadFile(NEW_FILE_PATH)

    def onLoad(self, evt):
        if not self.askForSaving():
            return
        if self.currentProject:
            filepath = os.path.split(self.currentProject)[0]
        else:
            filepath = os.path.expanduser("~")
        dlg = wx.FileDialog(self, "Open Qlive Projet", filepath, "",
                            "QLive Project files (*.qlp)|*.qlp", style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.loadFile(path)
        dlg.Destroy()

    def openRecent(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id).GetLabel()
        if self.askForSaving():
            self.loadFile(file)

    def newRecent(self, file):
        filename = QLiveLib.ensureNFD(OPEN_RECENT_PATH)
        try:
            f = codecs.open(filename, "r", encoding="utf-8")
            lines = [line.replace("\n", "") for line in f.readlines()]
            f.close()
        except:
            lines = []
        if not file in lines:
            f = codecs.open(filename, "w", encoding="utf-8")
            lines.insert(0, file)
            if len(lines) > 20:
                lines = lines[0:20]
            for line in lines:
                f.write(line + '\n')
            f.close()
        subId = 2000
        if lines != []:
            for item in self.submenu1.GetMenuItems():
                self.submenu1.DeleteItem(item)
            for file in lines:
                self.submenu1.Append(subId, QLiveLib.toSysEncoding(file))
                subId += 1

    def onClose(self, evt):
        self.onNew(None)

    def onSave(self, evt):
        if not self.currentProject:
            self.onSaveAs(None)
        else:
            self.saveFile(self.currentProject)

    def onSaveAs(self, evt):
        if self.currentProject:
            filepath = os.path.split(self.currentProject)
        else:
            filepath = os.path.join(os.path.expanduser("~"), "qlive_project.qlp")
            filepath = os.path.split(filepath)
        dlg = wx.FileDialog(self, "Save Qlive Projet", 
                            filepath[0], filepath[1],
                            "QLive Project files (*.qlp)|*.qlp",
                            style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.saveFile(path)
        dlg.Destroy()
        
    def openPrefs(self, evt):
        print "Popup Preferences Windows..."

    def OnClose(self, evt):
        if not self.askForSaving():
            return
        self.tracks.fxsView.closeAll()
        self.audioServer.stop()
        time.sleep(0.25)
        self.audioServer.shutdown()
        time.sleep(0.25)
        self.Destroy()
