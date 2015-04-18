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

class MeterControlSlider(wx.Panel):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), size=(200,16), log=False,
                 outFunction=None, integer=False, powoftwo=False, backColour=None, orient=wx.HORIZONTAL):
        if size == (200,16) and orient == wx.VERTICAL:
            size = (24, 200)
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size,
                            style=wx.NO_BORDER | wx.WANTS_CHARS | wx.EXPAND)
        self.parent = parent
        if backColour:
            self.backgroundColour = backColour
        else:
            self.backgroundColour = BACKGROUND_COLOUR
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(self.backgroundColour)
        self.orient = orient
        if self.orient == wx.VERTICAL:
            self.knobSize = 15
            self.knobHalfSize = 7
            self.sliderWidth = size[0] - 23
        else:
            self.knobSize = 40
            self.knobHalfSize = 20
            self.sliderHeight = size[1] - 5
        self.outFunction = outFunction
        self.integer = integer
        self.log = log
        self.powoftwo = powoftwo
        if self.powoftwo:
            self.integer = True
            self.log = False
        self.SetRange(minvalue, maxvalue)
        self.borderWidth = 1
        self.selected = False
        self._enable = True
        self.propagate = True
        self.midictl = None
        self.new = ''
        if init != None:
            self.SetValue(init)
            self.init = init
        else:
            self.SetValue(minvalue)
            self.init = minvalue
        self.clampPos()
        self.amplitude = [0]
        self.createBitmaps()
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.DoubleClick)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.LooseFocus)

        if sys.platform == "win32":
            self.dcref = wx.BufferedPaintDC
        else:
            self.dcref = wx.PaintDC

    def createBitmaps(self):
        w, h = 6, self.GetSize()[1]
        b = wx.EmptyBitmap(w,h)
        f = wx.EmptyBitmap(w,h)
        dcb = wx.MemoryDC(b)
        dcf = wx.MemoryDC(f)
        dcb.SetPen(wx.Pen("#000000", width=1))
        dcf.SetPen(wx.Pen("#000000", width=1))
        if self.orient == wx.HORIZONTAL:
            height = 6
            steps = int(w / 10.0 + 0.5)
        else:
            width = 6
            steps = int(h / 10.0 + 0.5)
        bounds = int(steps / 6.0)
        for i in range(steps):
            if i == (steps - 1):
                dcb.SetBrush(wx.Brush("#770000"))
                dcf.SetBrush(wx.Brush("#FF0000"))
            elif i >= (steps - bounds):
                dcb.SetBrush(wx.Brush("#440000"))
                dcf.SetBrush(wx.Brush("#CC0000"))
            elif i >= (steps - (bounds*2)):
                dcb.SetBrush(wx.Brush("#444400"))
                dcf.SetBrush(wx.Brush("#CCCC00"))
            else:
                dcb.SetBrush(wx.Brush("#004400"))
                dcf.SetBrush(wx.Brush("#00CC00"))
            if self.orient == wx.HORIZONTAL:
                dcb.DrawRectangle(i*10, 0, 11, height)
                dcf.DrawRectangle(i*10, 0, 11, height)
            else:
                ii = steps - 1 - i
                dcb.DrawRectangle(0, ii*10, width, 11)
                dcf.DrawRectangle(0, ii*10, width, 11)
        if self.orient == wx.HORIZONTAL:
            dcb.DrawLine(w-1, 0, w-1, height)
            dcf.DrawLine(w-1, 0, w-1, height)
        else:
            dcb.DrawLine(0, 0, width, 0)
            dcf.DrawLine(0, 0, width, 0)
        dcb.SelectObject(wx.NullBitmap)
        dcf.SelectObject(wx.NullBitmap)
        self.backBitmap = b
        self.bitmap = f

    def setRms(self, *args):
        if args[0] < 0:
            return
        if not args:
            self.amplitude = [0]
        else:
            self.amplitude = args
        wx.CallAfter(self.Refresh)

    def setMidiCtl(self, x, propagate=True):
        self.propagate = propagate
        self.midictl = x
        self.Refresh()

    def getMidiCtl(self):
        return self.midictl

    def getMinValue(self):
        return self.minvalue

    def getMaxValue(self):
        return self.maxvalue

    def Enable(self):
        self._enable = True
        self.Refresh()

    def Disable(self):
        self._enable = False
        self.Refresh()

    def setSliderHeight(self, height):
        self.sliderHeight = height
        self.Refresh()

    def setSliderWidth(self, width):
        self.sliderWidth = width

    def getInit(self):
        return self.init

    def SetRange(self, minvalue, maxvalue):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def getRange(self):
        return [self.minvalue, self.maxvalue]

    def scale(self):
        if self.orient == wx.VERTICAL:
            h = self.GetSize()[1]
            inter = tFromValue(h-self.pos, self.knobHalfSize, self.GetSize()[1]-self.knobHalfSize)
        else:
            inter = tFromValue(self.pos, self.knobHalfSize, self.GetSize()[0]-self.knobHalfSize)
        if not self.integer:
            return interpFloat(inter, self.minvalue, self.maxvalue)
        elif self.powoftwo:
            return powOfTwo(int(interpFloat(inter, self.minvalue, self.maxvalue)))
        else:
            return int(interpFloat(inter, self.minvalue, self.maxvalue))

    def SetValue(self, value, propagate=True):
        self.propagate = propagate
        if self.HasCapture():
            self.ReleaseMouse()
        if self.powoftwo:
            value = powOfTwoToInt(value)
        value = clamp(value, self.minvalue, self.maxvalue)
        if self.log:
            t = toLog(value, self.minvalue, self.maxvalue)
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        else:
            t = tFromValue(value, self.minvalue, self.maxvalue)
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        if self.integer:
            self.value = int(self.value)
        if self.powoftwo:
            self.value = powOfTwo(self.value)
        self.clampPos()
        self.selected = False
        self.Refresh()

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
        self.Refresh()

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
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']:
                self.new += char
            elif event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
                self.SetValue(eval(self.new))
                self.new = ''
                self.selected = False
            self.Refresh()
        event.Skip()

    def MouseDown(self, evt):
        if evt.ShiftDown():
            self.DoubleClick(evt)
            return
        if self._enable:
            size = self.GetSize()
            if self.orient == wx.VERTICAL:
                self.pos = clamp(evt.GetPosition()[1], self.knobHalfSize, size[1]-self.knobHalfSize)
            else:
                self.pos = clamp(evt.GetPosition()[0], self.knobHalfSize, size[0]-self.knobHalfSize)
            self.value = self.scale()
            self.CaptureMouse()
            self.selected = False
            self.Refresh()
        evt.Skip()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def DoubleClick(self, event):
        if self._enable:
            w, h = self.GetSize()
            pos = event.GetPosition()
            if self.orient == wx.VERTICAL:
                if wx.Rect(0, self.pos-self.knobHalfSize, w, self.knobSize).Contains(pos):
                    self.selected = True
            else:
                if wx.Rect(self.pos-self.knobHalfSize, 0, self.knobSize, h).Contains(pos):
                    self.selected = True
            self.Refresh()
        event.Skip()

    def MouseMotion(self, evt):
        if self._enable:
            size = self.GetSize()
            if self.HasCapture():
                if self.orient == wx.VERTICAL:
                    self.pos = clamp(evt.GetPosition()[1], self.knobHalfSize, size[1]-self.knobHalfSize)
                else:
                    self.pos = clamp(evt.GetPosition()[0], self.knobHalfSize, size[0]-self.knobHalfSize)
                self.value = self.scale()
                self.selected = False
                self.Refresh()

    def OnResize(self, evt):
        self.clampPos()
        self.Refresh()

    def clampPos(self):
        size = self.GetSize()
        if self.powoftwo:
            val = powOfTwoToInt(self.value)
        else:
            val = self.value
        if self.orient == wx.VERTICAL:
            self.pos = tFromValue(val, self.minvalue, self.maxvalue) * (size[1] - self.knobSize) + self.knobHalfSize
            self.pos = clamp(size[1]-self.pos, self.knobHalfSize, size[1]-self.knobHalfSize)
        else:
            self.pos = tFromValue(val, self.minvalue, self.maxvalue) * (size[0] - self.knobSize) + self.knobHalfSize
            self.pos = clamp(self.pos, self.knobHalfSize, size[0]-self.knobHalfSize)

    def setBackgroundColour(self, colour):
        self.backgroundColour = colour
        self.SetBackgroundColour(self.backgroundColour)
        self.Refresh()

    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = self.dcref(self)
        gc = wx.GraphicsContext_Create(dc)

        dc.SetBackground(wx.Brush(self.backgroundColour, wx.SOLID))
        dc.Clear()

        # Draw meter
        width = 6
        db = math.log10(self.amplitude[0]+0.00001) * 0.2 + 1.
        height = int(db*h)
        dc.DrawBitmap(self.backBitmap, 9, 0)
        if height > 0:
            dc.SetClippingRegion(9, h-height, width, height)
            dc.DrawBitmap(self.bitmap, 9, 0)
            dc.DestroyClippingRegion()

        # Draw knob
        if self._enable: knobColour = '#888888'
        else: knobColour = "#DDDDDD"
        if self.orient == wx.VERTICAL:
            rec = wx.Rect(0, self.pos-self.knobHalfSize, w, self.knobSize-1)
            if self.selected:
                brush = wx.Brush(wx.Colour(64, 64, 64, 128))
            else:
                brush = wx.Brush(wx.Colour(64, 64, 64, 192))
            gc.SetBrush(brush)
            gc.DrawRoundedRectangle(rec[0], rec[1], rec[2], rec[3], 3)
        else:
            rec = wx.Rect(self.pos-self.knobHalfSize, 0, self.knobSize-1, h)
            if self.selected:
                brush = wx.Brush('#333333', wx.SOLID)
            else:
                brush = gc.CreateLinearGradientBrush(self.pos-self.knobHalfSize, 0, self.pos+self.knobHalfSize, 0, "#323854", knobColour)
            gc.SetBrush(brush)
            gc.DrawRoundedRectangle(rec[0], rec[1], rec[2], rec[3], 3)

        if sys.platform in ['win32', 'linux2']:
            dc.SetFont(wx.Font(7, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        else:
            dc.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        # Draw text
        if self.selected and self.new:
            val = self.new
        else:
            if self.integer:
                val = '%d' % self.GetValue()
            elif abs(self.GetValue()) >= 1000:
                val = '%.0f' % self.GetValue()
            elif abs(self.GetValue()) >= 100:
                val = '%.0f' % self.GetValue()
            elif abs(self.GetValue()) >= 10:
                val = '%.0f' % self.GetValue()
            elif abs(self.GetValue()) < 10:
                val = '%.1f' % self.GetValue()
        if sys.platform == 'linux2':
            width = len(val) * (dc.GetCharWidth() - 3)
        else:
            width = len(val) * dc.GetCharWidth()
        dc.SetTextForeground('#FFFFFF')
        dc.DrawLabel(val, rec, wx.ALIGN_CENTER)

        # Send value
        if self.outFunction and self.propagate:
            self.outFunction(self.GetValue())
        self.propagate = True

        evt.Skip()

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
                offX = pos[0] - self.clickPos[0]
                off = offY + offX
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
       
class TransportButtons(wx.Panel):
    def __init__(self, parent, playCallback=None, recordCallback=None):
        super(TransportButtons, self).__init__(parent)

        self.playmode = self.recordmode = 0
        self.playCallback = playCallback
        self.recordCallback = recordCallback

        self.playIcon = wx.Bitmap(ICON_PLAY, wx.BITMAP_TYPE_PNG)
        self.playPressedIcon = wx.Bitmap(ICON_PLAY_PRESSED, wx.BITMAP_TYPE_PNG)
        self.recordIcon = wx.Bitmap(ICON_RECORD, wx.BITMAP_TYPE_PNG)
        self.recordPressedIcon = wx.Bitmap(ICON_RECORD_PRESSED, wx.BITMAP_TYPE_PNG)
        
        self.play = wx.BitmapButton(self, wx.ID_ANY, self.playIcon)
        self.play.Bind(wx.EVT_BUTTON, self.onPlay)

        self.record = wx.BitmapButton(self, wx.ID_ANY, self.recordIcon)
        self.record.Bind(wx.EVT_BUTTON, self.onRecord)
        
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.play, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        box.Add(self.record, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        self.SetSizer(box)

    def onPlay(self, evt):
        self.playmode = (self.playmode + 1) % 2
        if self.playmode == 1:
            self.play.SetBitmapLabel(self.playPressedIcon)
            self.record.Disable()
        else:
            self.play.SetBitmapLabel(self.playIcon)
            self.record.SetBitmapLabel(self.recordIcon)
            self.record.Enable()
            self.recordmode = 0
        if self.playCallback is not None:
            self.playCallback(self.playmode)

    def onRecord(self, evt):
        self.recordmode = self.playmode = (self.recordmode + 1) % 2
        if self.recordmode == 1:
            self.record.SetBitmapLabel(self.recordPressedIcon)
            self.play.SetBitmapLabel(self.playPressedIcon)
        else:
            self.record.SetBitmapLabel(self.recordIcon)
            self.play.SetBitmapLabel(self.playIcon)
        if self.recordCallback is not None:
            self.recordCallback(self.recordmode)

if __name__ == "__main__":
    from pyo64 import *
    s = Server().boot()
    class TestFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None)
            panel = wx.Panel(self)
            panel.SetBackgroundColour(BACKGROUND_COLOUR)
            #tr = TransportButtons(panel)
            #knob = QLiveControlKnob(panel, 20, 20000, pos=(20,20), label="Freq")
            #knob.setEnable(True)
            self.Show()
    app = wx.App()
    f = TestFrame()
    app.MainLoop()