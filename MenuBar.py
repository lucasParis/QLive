import wx
import os 

class MenuBar(wx.MenuBar):
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent
        menu1 = wx.Menu()
        menu1.Append(wx.NewId(), "Schtroumpf", "Schtroumpf")

        saveId = wx.ID_SAVE
        menu1.Append(saveId, "Save", "Save")
        self.Bind(wx.EVT_MENU, self.onSave, id = saveId)
        
        loadId = wx.ID_OPEN
        menu1.Append(loadId, "Open", "Open")
        self.Bind(wx.EVT_MENU, self.onLoad, id = loadId)


#        menu1.Append(wx.ID_EXIT, "Quit", "Quit")

        self.Append(menu1, 'file')
        pass
        
    def onSave(self, event):
        dlg = wx.FileDialog(self, "choose path to save Qlive projet", '', '', ".", wx.SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "saving:", self.parent.tracks.getSaveDict()
            dictSave = self.parent.tracks.getSaveDict()
            f = open(path, "w")
            f.write("dictSave = %s" % str(dictSave))
            f.close()
            pass
        dlg.Destroy()

        
    def onLoad(self, event):
        print "oo Loard"
        dlg = wx.FileDialog(self, "choose Qlive projet", '', '', ".", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            execfile(path, globals())
            print "opening: ", dictSave
            self.parent.tracks.setSaveDict(dictSave)
        dlg.Destroy()
        
if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.menuB = MenuBar(None)
            self.SetMenuBar(self.menuB)
#            self.pan = MixerPanel(self)
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()