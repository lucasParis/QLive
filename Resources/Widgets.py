import wx, math
from pyolib._wxwidgets import ControlSlider, BACKGROUND_COLOUR
from AudioMixer import *
from constants import *

def interpFloat(t, v1, v2):
    "interpolator for a single value; interprets t in [0-1] between v1 and v2"
    return (v2-v1)*t + v1

def tFromValue(value, v1, v2):
    "returns a t (in range 0-1) given a value in the range v1 to v2"
    return float(value-v1)/(v2-v1)

def clamp(v, minv, maxv):
    "clamps a value within a range"
    if v<minv: v=minv
    if v> maxv: v=maxv
    return v

def toLog(t, v1, v2):
    return math.log10(t/v1) / math.log10(v2/v1)

def toExp(t, v1, v2):
    return math.pow(10, t * (math.log10(v2) - math.log10(v1)) + math.log10(v1))

POWOFTWO = {2:1, 4:2, 8:3, 16:4, 32:5, 64:6, 128:7, 256:8, 512:9, 1024:10, 2048:11, 4096:12, 8192:13, 16384:14, 32768:15, 65536:16}
def powOfTwo(x):
    return 2**x

def powOfTwoToInt(x):
    return POWOFTWO[x]

class QLiveControlKnob(wx.Panel):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), 
                 size=(50,70), log=False, outFunction=None, integer=False, 
                 backColour=None, label=''):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, 
                          size=size, style=wx.NO_BORDER|wx.WANTS_CHARS)
        self.parent = parent
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetMinSize(self.GetSize())
        self.outFunction = outFunction
        self.integer = integer
        self.log = log
        self.label = label
        self.SetRange(minvalue, maxvalue)
        self.borderWidth = 1
        self.selected = False
        self._enable = True
        self.new = ''
        self.floatPrecision = '%.3f'
        self.mode = 0
        self.midiLearn = False
        self.midictlLabel = ""
        self.colours = {0: "#000000", 1: "#FF0000", 2: "#00FF00"}
        if backColour: self.backColour = backColour
        else: self.backColour = CONTROLSLIDER_BACK_COLOUR
        if init != None: 
            self.SetValue(init)
            self.init = init
        else: 
            self.SetValue(minvalue)
            self.init = minvalue
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.DoubleClick)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.LooseFocus)

        if PLATFORM == "win32":
            self.dcref = wx.BufferedPaintDC
        else:
            self.dcref = wx.PaintDC

    def setFloatPrecision(self, x):
        self.floatPrecision = '%.' + '%df' % x
        wx.CallAfter(self.Refresh)

    def getMinValue(self):
        return self.minvalue

    def getMaxValue(self):
        return self.maxvalue

    def setEnable(self, enable):
        self._enable = enable
        wx.CallAfter(self.Refresh)

    def getInit(self):
        return self.init

    def getLabel(self):
        return self.label

    def getLog(self):
        return self.log
        
    def SetRange(self, minvalue, maxvalue):   
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def getRange(self):
        return [self.minvalue, self.maxvalue]

    def SetValue(self, value):
        value = clamp(value, self.minvalue, self.maxvalue)
        if self.log:
            t = toLog(value, self.minvalue, self.maxvalue)
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        else:
            t = tFromValue(value, self.minvalue, self.maxvalue)
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        if self.integer:
            self.value = int(self.value)
        self.selected = False
        wx.CallAfter(self.Refresh)

    def GetValue(self):
        if self.log:
            t = tFromValue(self.value, self.minvalue, self.maxvalue)
            val = toExp(t, self.minvalue, self.maxvalue)
        else:
            val = self.value
        if self.integer:
            val = int(val)
        return val

    def LooseFocus(self, event):
        self.selected = False
        wx.CallAfter(self.Refresh)

    def keyDown(self, event):
        if self.selected:
            char = ''
            if event.GetKeyCode() in range(324, 334):
                char = str(event.GetKeyCode() - 324)
            elif event.GetKeyCode() == 390:
                char = '-'
            elif event.GetKeyCode() == 391:
                char = '.'
            elif event.GetKeyCode() == wx.WXK_BACK:
                if self.new != '':
                    self.new = self.new[0:-1]
            elif event.GetKeyCode() < 256:
                char = chr(event.GetKeyCode())
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.new += char
            elif char == '.' and not '.' in self.new:
                self.new += char
            elif char == '-' and len(self.new) == 0:
                self.new += char
            elif event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
                if self.new != '':
                    self.SetValue(eval(self.new))
                    self.new = ''
                self.selected = False
        wx.CallAfter(self.Refresh)

    def MouseDown(self, evt):
        if evt.ShiftDown():
            self.DoubleClick(evt)
            return
        if self._enable:
            rec = wx.Rect(5, 13, 45, 45)
            pos = evt.GetPosition()
            if rec.Contains(pos):
                self.clickPos = wx.GetMousePosition()
                self.oldValue = self.value
                self.CaptureMouse()
                self.selected = False
            wx.CallAfter(self.Refresh)
        evt.Skip()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def DoubleClick(self, event):
        if self._enable:
            w, h = self.GetSize()
            pos = event.GetPosition()
            reclab = wx.Rect(3, 60, w-3, 10)
            recpt = wx.Rect(self.knobPointPos[0]-3, self.knobPointPos[1]-3, 9, 9)
            if reclab.Contains(pos):
                self.selected = True
            elif recpt.Contains(pos):
                self.mode = (self.mode+1) % 3
            wx.CallAfter(self.Refresh)
        event.Skip()

    def MouseMotion(self, evt):
        if self._enable:
            if evt.Dragging() and evt.LeftIsDown() and self.HasCapture():
                pos = wx.GetMousePosition()
                offY = self.clickPos[1] - pos[1]
                off = offY
                off *= 0.005 * (self.maxvalue - self.minvalue)
                self.value = clamp(self.oldValue + off, self.minvalue, self.maxvalue)    
                self.selected = False
                wx.CallAfter(self.Refresh)

    def setbackColour(self, colour):
        self.backColour = colour
        wx.CallAfter(self.Refresh)

    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = self.dcref(self)
        gc = wx.GraphicsContext_Create(dc)

        if self._enable:
            backColour = self.backColour
            knobColour = CONTROLSLIDER_KNOB_COLOUR
        else:
            backColour = CONTROLSLIDER_DISABLE_BACK_COLOUR
            knobColour = CONTROLSLIDER_DISABLE_KNOB_COLOUR

        dc.Clear()
        gc.SetBrush(wx.Brush(backColour, wx.SOLID))

        # Draw background
        gc.SetPen(wx.Pen("#777777", width=self.borderWidth, style=wx.SOLID))
        gc.DrawRoundedRectangle(0, 0, w-1, h-1, 3)

        dc.SetFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        dc.SetTextForeground(CONTROLSLIDER_TEXT_COLOUR)

        # Draw text label
        reclab = wx.Rect(0, 1, w, 9)
        dc.DrawLabel(self.label, reclab, wx.ALIGN_CENTER_HORIZONTAL)

        recval = wx.Rect(0, 55, w, 14)

        if self.selected:
            gc.SetBrush(wx.Brush(CONTROLSLIDER_SELECTED_COLOUR, wx.SOLID))
            gc.SetPen(wx.Pen(CONTROLSLIDER_SELECTED_COLOUR, width=self.borderWidth, style=wx.SOLID))  
            gc.DrawRoundedRectangle(2, 55, w-4, 12, 2)

        r = math.sqrt(.1)
        val = tFromValue(self.value, self.minvalue, self.maxvalue) * 0.8
        ph = val * math.pi * 2 - (3 * math.pi / 2.2)
        X = r * math.cos(ph)*45
        Y = r * math.sin(ph)*45
        gc.SetBrush(wx.Brush(knobColour, wx.SOLID))
        gc.SetPen(wx.Pen(self.colours[self.mode], width=2, style=wx.SOLID))
        self.knobPointPos = (X+25, Y+35)
        R = math.sqrt(X*X + Y*Y)
        gc.DrawEllipse(25-R, 35-R, R*2, R*2)
        gc.StrokeLine(25, 35, X+25, Y+35)

        if not self.midiLearn:
            dc.SetFont(wx.Font(CONTROLSLIDER_FONT-1, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))    
            dc.DrawLabel(self.midictlLabel, wx.Rect(2, 12, 40, 40), wx.ALIGN_CENTER)
        else:
            dc.DrawLabel("?...", wx.Rect(2, 12, 40, 40), wx.ALIGN_CENTER)

        dc.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        # Draw text value
        if self.selected and self.new:
            val = self.new
        else:
            if self.integer:
                val = '%d' % self.GetValue()
            else:
                val = self.floatPrecision % self.GetValue()
        if PLATFORM == 'linux2':
            width = len(val) * (dc.GetCharWidth() - 3)
        else:
            width = len(val) * dc.GetCharWidth()
        dc.SetTextForeground(CONTROLSLIDER_TEXT_COLOUR)
        dc.DrawLabel(val, recval, wx.ALIGN_CENTER)

        # Send value
        if self.outFunction:
            self.outFunction(self.GetValue())

        evt.Skip()
        
if __name__ == "__main__":
    from pyo64 import *
    s = Server().boot()
    class TestFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            panel = wx.Panel(self)
            panel.SetBackgroundColour(BACKGROUND_COLOUR)
            knob = QLiveControlKnob(panel, 20, 20000, pos=(20,20), label="Freq")
            knob.setEnable(True)
            self.Show()
    app = wx.App()
    f = TestFrame()
    app.MainLoop()