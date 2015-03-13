import os, sys, unicodedata
from types import UnicodeType

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

# Colours
MIDILEARN_COLOUR = "#FF2299"
