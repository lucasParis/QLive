#!/usr/bin/python
# simple.py
"""
- how will choice boxes and paths behave in dicts? for now only values are taken care of
- make parent class for both creators input and fxs

"""
import wx
from Resources.constants import *
import Resources.QLiveLib as QLiveLib
from Resources.MainWindow import MainWindow

class QLiveApp(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        sysx = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        sysy = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        if sysx < 900:
            sizex = sysx - 40
        else:
            sizex = 900
        if sysy < 670:
            sizey = sysy - 40
        else:
            sizey = 670
        self.frame = MainWindow(pos=(20, 20), size=(sizex, sizey))
        QLiveLib.setVar("MainWindow", self.frame)

    def MacOpenFiles(self, filenames):
        if type(filenames) != ListType:
            filenames = [filenames]
        self.frame.loadFile(QLiveLib.ensureNFD(filenames[0]))

    def MacReopenApp(self):
        try:
            self.frame.Raise()
        except:
            pass

if __name__ == "__main__":
    qlfile = None
    if len(sys.argv) > 1:
        qlfile = sys.argv[1]
    app = QLiveApp()
    if qlfile:
        wx.CallAfter(app.frame.loadFile, QLiveLib.ensureNFD(qlfile))
    app.MainLoop()
