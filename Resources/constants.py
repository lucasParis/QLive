import os, sys, unicodedata
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

SOUNDS_PATH = os.path.join(RESOURCES_PATH, "sounds")

DEBUG = True

NUM_INPUTS = 4
NUM_OUTPUTS = 4

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
BIT_DEPTHS= {'16 bits int': 0, '24 bits int': 1, '32 bits int': 2, '32 bits float': 3}
BUFFER_SIZES = ['64','128','256','512','1024','2048','4096','8192','16384']
AUDIO_FILE_FORMATS = {'wav': 0, 'aif': 1, 'au': 2, 'sd2': 4, 'flac': 5, 'caf': 6, 'ogg': 7}
AUDIO_FILE_WILDCARD =  "All files|*.*|" \
                       "Wave file|*.wave;*.WAV;*.WAVE;*.Wav;*.Wave;*.wav|" \
                       "AIFF file|*.aif;*.aiff;*.aifc;*.AIF;*.AIFF;*.Aif;*.Aiff|" \
                       "Flac file|*.flac;*.FLAC;*.Flac;|" \
                       "OGG file|*.ogg;*.OGG;*.Ogg;|" \
                       "SD2 file|*.sd2;*.SD2;*.Sd2;|" \
                       "AU file|*.au;*.AU;*.Au;|" \
                       "CAF file|*.caf;*.CAF;*.Caf"

# Colours
BACKGROUND_COLOUR = BACKGROUND_COLOUR
MIDILEARN_COLOUR = "#FF2299"
