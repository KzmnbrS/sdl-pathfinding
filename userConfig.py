from sdl2 import *


RGBA = SDL_Color

WINDOW = {
    'TITLE': b'BEST PROGRAM EU',
    'WIDTH': 1280,
    'HEIGHT': 720,
    'BACKGROUND_COLOR': RGBA(241, 240, 236)
}

CELL = {
    'KEYS': {
        'WALL': SDLK_w,
        'REGULAR': SDLK_r,
        'START': SDLK_s,
        'FINISH': SDLK_f,
        'PATH': SDLK_p
    },

    'COLORS': {
        'WALL': RGBA(80, 62, 44),
        'REGULAR': RGBA(241, 240, 236),
        'START': RGBA(85, 208, 235),
        'FINISH': RGBA(219, 152, 52),
        'PATH': RGBA(60, 76, 231)
    },

    'SIZE': {
        'X': 32,
        'Y': 30
    }
}


