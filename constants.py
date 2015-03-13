import sys, unicodedata
from types import UnicodeType

reload(sys)
sys.setdefaultencoding("utf-8")

DEFAULT_ENCODING = sys.getdefaultencoding()
SYSTEM_ENCODING = sys.getfilesystemencoding()

PLATFORM = sys.platform

DEBUG = True

QLIVE_MAGIC_LINE = "### QLIVE PROJECT FILE ###\n"
QLIVE_VERSION = 0.1

NUM_INPUTS = 4
NUM_OUTPUTS = 4

# Colours
MIDILEARN_COLOUR = "#FF2299"
