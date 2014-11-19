import wx

class FxTracksToolBar(wx.ToolBar):
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, size = (1000, 40))
#        self.remRowButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
#        self.remRowButton.SetLabel("-")    
        self.AddControl(wx.StaticText(self, label = "row"))
        self.remRowButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
        self.remRowButton.SetLabel("-")    
        self.AddControl(self.remRowButton)
        self.addRowButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
        self.addRowButton.SetLabel("+")    
        self.AddControl(self.addRowButton)
        
        self.AddControl(wx.StaticText(self, label = "column"))
        self.remColButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
        self.remColButton.SetLabel("-")    
        self.AddControl(self.remColButton)
        self.addColButton = wx.Button(self, size = (30,-1), pos = (-1,-1))
        self.addColButton.SetLabel("+")    
        self.AddControl(self.addColButton)

        self.Realize()
        


if __name__ == "__main__":
    class TestWindow(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            self.panel = wx.Panel(self)
            self.toolbar = FxTracksToolBar(self.panel)
            boxSizer = wx.BoxSizer(wx.VERTICAL)
            boxSizer.Add(self.toolbar, 1, wx.EXPAND)
            self.panel.SetSizer(boxSizer)

    app = wx.App()

    frame = TestWindow()
    frame.Show()

    app.MainLoop()