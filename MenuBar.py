import wx

class MenuBar(wx.MenuBar):
    def __init__(self):
        wx.MenuBar.__init__(self)
        menu1 = wx.Menu()
        menu1.Append(wx.NewId(), "Schtroumpf", "Schtroumpf")

        saveId = wx.NewId()
        menu1.Append(saveId, "Save", "Save")
        self.Bind(wx.EVT_MENU, self.onSave, id = saveId)
        
        loadId = wx.NewId()
        menu1.Append(loadId, "Load", "Load")
        self.Bind(wx.EVT_MENU, self.onLoad, id = loadId)


#        menu1.Append(wx.ID_EXIT, "Quit", "Quit")

        self.Append(menu1, 'file')
        pass
        
    def onSave(self, event):
        print "our savior"
        
    def onLoad(self, event):
        print "oo Loard"

if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.menuB = MenuBar()
            self.SetMenuBar(self.menuB)
#            self.pan = MixerPanel(self)
            pass

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()