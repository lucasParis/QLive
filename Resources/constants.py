import os, sys, unicodedata, copy
from types import UnicodeType
from pyolib._wxwidgets import BACKGROUND_COLOUR

reload(sys)
sys.setdefaultencoding("utf-8")

QLIVE_MAGIC_LINE = "### QLIVE PROJECT FILE ###\n"
APP_NAME = "QLive"
APP_VERSION = "0.1.0"
APP_COPYRIGHT = '???,  2015'
FILE_EXTENSION = "qlp"

DEFAULT_ENCODING = sys.getdefaultencoding()
SYSTEM_ENCODING = sys.getfilesystemencoding()

PLATFORM = sys.platform

if '/%s.app' % APP_NAME in os.getcwd():
    RESOURCES_PATH = os.getcwd()
else:
    RESOURCES_PATH = os.path.join(os.getcwd(), 'Resources')

if not os.path.isdir(RESOURCES_PATH) and PLATFORM == "win32":
    RESOURCES_PATH = os.path.join(os.getenv("ProgramFiles"), "QLive", "Resources")

TEMP_PATH = os.path.join(os.path.expanduser('~'), '.qlive')
if not os.path.isdir(TEMP_PATH):
    os.mkdir(TEMP_PATH)

OPEN_RECENT_PATH = os.path.join(TEMP_PATH, "open_recents.txt")
if not os.path.isfile(OPEN_RECENT_PATH):
    with open(OPEN_RECENT_PATH, "w") as f:
        pass

PREFERENCES_PATH = os.path.join(TEMP_PATH, "qlive-prefs.py")
if not os.path.isfile(PREFERENCES_PATH):
    with open(PREFERENCES_PATH, "w") as f:
        f.write("qlive_prefs = {}")

qlive_prefs = {}
with open(PREFERENCES_PATH, "r") as f:
    text = f.read()
exec text in locals()
PREFERENCES = copy.deepcopy(qlive_prefs)

SOUNDS_PATH = os.path.join(RESOURCES_PATH, "sounds")
NEW_FILE_PATH = os.path.join(RESOURCES_PATH, "qlive_new_file.qlp")

DEBUG = True

NUM_CHNLS = 2
NUM_INPUTS = 4
NUM_OUTPUTS = 4

BOX_MENU_ITEM_FIRST_ID = 1000
NEW_TRACK_ID = 2000
DELETE_TRACK_ID = 2001
LINK_STEREO_ID = 3000

# Audio drivers
if PLATFORM == 'darwin' and '/%s.app' % APP_NAME in os.getcwd():
    AUDIO_DRIVERS = ['portaudio']
elif PLATFORM == 'darwin':
    AUDIO_DRIVERS = ['coreaudio', 'portaudio', 'jack']
elif PLATFORM == 'win32':
    AUDIO_DRIVERS = ['portaudio']
else:
    AUDIO_DRIVERS = ['portaudio', 'jack']

# MIDI drivers
MIDI_DRIVERS = ['portmidi']

# Audio settings
SAMPLE_RATES = ['22050','44100','48000', '88200', '96000']
BUFFER_SIZES = ['64','128','256','512','1024','2048','4096','8192','16384']
ALLOWED_EXTENSIONS = ["wav","wave","aif","aiff","aifc","au","","sd2","flac","caf","ogg"]
EXPORT_FORMATS = ['WAV', 'AIFF', 'AU', 'RAW', 'SD2', 'FLAC', 'CAF', 'OGG']
EXPORT_TYPES = ['16 int', '24 int', '32 int', '32 float', '64 float']
RECORD_EXTENSIONS = [".wav",".aif",".au","",".sd2",".flac",".caf",".ogg"]
AUDIO_FILE_WILDCARD =  "All files|*.*|" \
                       "Wave file|*.wave;*.WAV;*.WAVE;*.Wav;*.Wave;*.wav|" \
                       "AIFF file|*.aif;*.aiff;*.aifc;*.AIF;*.AIFF;*.Aif;*.Aiff|" \
                       "Flac file|*.flac;*.FLAC;*.Flac;|" \
                       "OGG file|*.ogg;*.OGG;*.Ogg;|" \
                       "SD2 file|*.sd2;*.SD2;*.Sd2;|" \
                       "AU file|*.au;*.AU;*.Au;|" \
                       "CAF file|*.caf;*.CAF;*.Caf"

# Fonts
FONT_FACE = 'Trebuchet MS'
if sys.platform in ['linux2', 'win32']:
    CONTROLSLIDER_FONT = 7
else:
    CONTROLSLIDER_FONT = 10

# Colours
BACKGROUND_COLOUR = BACKGROUND_COLOUR
MIDILEARN_COLOUR = "#FF2299"
CUEBUTTON_UNSELECTED_COLOUR = "#DDDDDD"
CUEBUTTON_SELECTED_COLOUR = "#4444DD"
CONTROLSLIDER_KNOB_COLOUR = '#DDDDDD'
CONTROLSLIDER_DISABLE_KNOB_COLOUR = '#ABABAB'
CONTROLSLIDER_BACK_COLOUR = '#BBB9BC'
CONTROLSLIDER_DISABLE_BACK_COLOUR = '#99A7AA'
CONTROLSLIDER_SELECTED_COLOUR = '#EAEAEA'
CONTROLSLIDER_TEXT_COLOUR = '#000000'
TRACKS_BACKGROUND_COLOUR = "#444444"
FXBOX_OUTLINE_COLOUR = "#222222"
FXBOX_ENABLE_BACKGROUND_COLOUR = "#EEEEEE"
FXBOX_DISABLE_BACKGROUND_COLOUR = "#CCCCCC"
FXBOX_FOREGROUND_COLOUR = "#000000"
