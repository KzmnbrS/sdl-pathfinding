from userConfig import *


# MARK: Window

WIN_TITLE = WINDOW['TITLE']
WIN_WIDTH = WINDOW['WIDTH']
WIN_HEIGHT = WINDOW['HEIGHT']
WIN_BG = WINDOW['BACKGROUND_COLOR']

# MARK: Color definition

# SDL interprets each pixel as a 32-bit number, so our masks must depend
# on the endianness (byte order) of the machine

big_endian = (SDL_BYTEORDER == SDL_BIG_ENDIAN)
R_MASK = 0xff000000 if big_endian else 0x000000ff
G_MASK = 0x00ff0000 if big_endian else 0x0000ff00
B_MASK = 0x0000ff00 if big_endian else 0x00ff0000
A_MASK = 0x000000ff if big_endian else 0xff000000

SUPPRESS_DEPRECATED_FLAGS = 0   # SDL_CreateRGBSurface(flags, ...)
TRUE_COLOR_PLUS_ALPHA = 32      # 24 bits for color definition and 8 for alpha channel

# MARK: CELL

RESET_KEY = CELL['KEYS']['REGULAR']
WALL_KEY = CELL['KEYS']['WALL']
START_KEY = CELL['KEYS']['START']
FINISH_KEY = CELL['KEYS']['FINISH']
PATH_KEY = CELL['KEYS']['PATH']

PLOTTING_KEYS = (RESET_KEY, WALL_KEY,
                 START_KEY, FINISH_KEY)

CELL_WIDTH = CELL['SIZE']['X']
CELL_HEIGHT = CELL['SIZE']['Y']

REGULAR_COLOR = CELL['COLORS']['REGULAR']
WALL_COLOR = CELL['COLORS']['WALL']
START_COLOR = CELL['COLORS']['START']
FINISH_COLOR = CELL['COLORS']['FINISH']
PATH_COLOR = CELL['COLORS']['PATH']

