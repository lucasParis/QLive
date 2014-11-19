import wx

class MenuBar(wx.MenuBar):
    def __init__(self):
        wx.MenuBar.__init__(self)
        menu1 = wx.Menu()
        menu1.Append(wx.NewId(), "Schtroumpf", "Schtroumpf")
#        menu1.Append(wx.ID_EXIT, "Quit", "Quit")

        self.Append(menu1, 'file')
        pass
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