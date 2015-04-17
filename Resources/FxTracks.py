import wx
from FxTrack import *
from FxView import FxViewManager

class FxTracks(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self.SetBackgroundColour(TRACKS_BACKGROUND_COLOUR)

        self.selectedTrack = 0

        # FX window manager
        self.fxsView = FxViewManager(self)
        
        self.createTracks(2)

        self.SetVirtualSize((5000, 1000))
        w, h = self.GetVirtualSize()
        self.SetScrollbars(20, 20, w/20, h/20, 0, 0, False)

        self.setFont()
        self.createButtonBitmap()
        self.createButtonBitmap(False)

        self.prepareBuffer()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.leftClicked)
        self.Bind(wx.EVT_RIGHT_DOWN, self.rightClicked)

    def createTracks(self, num):
        self.tracks = []
        x = 25
        h = TRACK_ROW_SIZE * 2
        for i in range(num):
            track = FxTrack(self, self.fxsView, i)
            track.setTrackPosition(x)
            track.setTrackHeight(h)
            self.tracks.append(track)
            x += h

    def addTrack(self):
        prevTrack = self.tracks[-1]
        x = prevTrack.getTrackPosition() + prevTrack.getTrackHeight()
        h = TRACK_ROW_SIZE * 2
        track = FxTrack(self, self.fxsView, len(self.tracks))
        track.setTrackPosition(x)
        track.setTrackHeight(h)
        self.tracks.append(track)
        self.doDrawAndRefresh()
        
    def setFont(self, ptsize=10):
        self.font = wx.Font(ptsize, wx.FONTFAMILY_DEFAULT, wx.NORMAL, 
                            wx.FONTWEIGHT_NORMAL, face="Monospace")

    def createButtonBitmap(self, enable=True):
        w, h = BUTTON_WIDTH, BUTTON_HEIGHT
        b = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(b)
        dc.SetPen(wx.Pen(TRACKS_BACKGROUND_COLOUR, 1))
        dc.SetBrush(wx.Brush(TRACKS_BACKGROUND_COLOUR))
        dc.DrawRectangle(0, 0, w, h)
        gc = wx.GraphicsContext_Create(dc)
        gc.SetPen(wx.Pen(FXBOX_OUTLINE_COLOUR, 1, wx.SOLID))
        if enable:
            gc.SetBrush(wx.Brush(FXBOX_ENABLE_BACKGROUND_COLOUR, wx.SOLID))
        else:
            gc.SetBrush(wx.Brush(FXBOX_DISABLE_BACKGROUND_COLOUR, wx.SOLID))
        rect = wx.Rect(0, 0, w, h)
        rectIn = wx.Rect(0, 4, w/12., h-8)
        rectOut = wx.Rect(w*11/12., 4, w/12., h-8)
        gc.DrawRoundedRectangle(rect[0], rect[1], rect[2], rect[3], 5)
        gc.DrawRoundedRectangle(rectIn[0], rectIn[1], rectIn[2], rectIn[3], 2)
        gc.DrawRoundedRectangle(rectOut[0], rectOut[1], rectOut[2], rectOut[3], 2)
        dc.SelectObject(wx.NullBitmap)
        if enable:
            self.buttonBitmap = b
        else:
            self.disableButtonBitmap = b

    def prepareBuffer(self):
        self.buffer = wx.EmptyBitmap(5000, 1000)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DoDrawing(dc)

    def doDrawAndRefresh(self):
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DoDrawing(dc)
        wx.CallAfter(self.Refresh)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        
    def DoDrawing(self, dc):
        dc.BeginDrawing()

        dc.SetFont(self.font)
        dc.SetTextForeground("#FFFFFF")

        dc.DrawLabel("Inputs", wx.Rect(0, 2, 100, 22), wx.ALIGN_CENTER)
        dc.DrawLabel("Fxs", wx.Rect(100, 2, 100, 22), wx.ALIGN_CENTER)
        dc.SetPen(wx.Pen("#333333", 1))
        dc.DrawLine(2, 25, 4098, 25)

        for track in self.tracks:
            track.onPaint(dc, self.buttonBitmap, self.disableButtonBitmap,
                            self.selectedTrack)

        dc.EndDrawing()

    def leftClicked(self, evt):
        pos = self.CalcUnscrolledPosition(evt.GetPosition())
        trackFounded = buttonFounded = selection = None
        for track in self.tracks:
            if pos[1] > track.getTrackPosition() and \
               pos[1] < track.getTrackPosition() + track.getTrackHeight():
                trackFounded = track
                break
        if trackFounded is not None:
            buttonFounded = None
            if pos[0] < 25:
                self.setSelectedTrack(track.getId())
                selection = track.getId()
            elif pos[0] < 125:
                for but in track.buttonsInputs:
                    if but.getRect().Contains(pos):
                        buttonFounded = but
                        break
            else:
                for but in track.buttonsFxs:
                    if but.getRect().Contains(pos):
                        buttonFounded = but
                        break
        if buttonFounded is not None:
            buttonFounded.openView()
        elif selection is not None:
            pass
        else:
            track.createFx(pos)
            self.doDrawAndRefresh()
        evt.Skip()

    def rightClicked(self, evt):
        pos = self.CalcUnscrolledPosition(evt.GetPosition())
        trackFounded = buttonFounded = None
        for track in self.tracks:
            if pos[1] > track.getTrackPosition() and \
               pos[1] < track.getTrackPosition() + track.getTrackHeight():
                trackFounded = track
                break
        if trackFounded is not None:
            buttonFounded = None
            if pos[0] < 100:
                for but in track.buttonsInputs:
                    if but.getRect().Contains(pos):
                        buttonFounded = but
                        break
            else:
                for but in track.buttonsFxs:
                    if but.getRect().Contains(pos):
                        buttonFounded = but
                        break
        if buttonFounded is not None:
            buttonFounded.openMenu(evt)
            self.doDrawAndRefresh()
        evt.Skip()

    def getSaveDict(self):
        return {"tracks": [track.getSaveDict() for track in self.tracks]}

    def setSaveDict(self, saveDict):
        self.createTracks(len(saveDict["tracks"]))
        for i in range(len(self.tracks)):
            self.tracks[i].setSaveDict(saveDict["tracks"][i])
        self.doDrawAndRefresh()
            
        self.selectedTrack = 0

    def cueEvent(self, eventDict):
        for track in self.tracks:
            track.cueEvent(eventDict)
        self.fxsView.refresh()
 
    def start(self):
        for track in self.tracks:
            track.start()

    def removeTrack(self):
        del self.tracks[self.selectedTrack]
        if not self.tracks:
            self.createTracks(1)

        self.selectedTrack -= 1
        if self.selectedTrack < 0:
            self.selectedTrack = 0
                
        [track.setId(i) for i, track in enumerate(self.tracks)]
        x = 25
        for track in self.tracks:
            track.setTrackPosition(x)
            x += track.getTrackHeight()

        self.doDrawAndRefresh()
        
    def setSelectedTrack(self, id):        
        self.selectedTrack = id
        self.doDrawAndRefresh()