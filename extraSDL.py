from sdl2 import *
from sdl2.sdlttf import *


class SDL:

    def __init__(self, sdl_init_flags):
        if SDL_Init(sdl_init_flags) != 0:
            raise RuntimeError('SDL init failed: %s' % SDL_GetError())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def __del__(self):
        SDL_Quit()


class TTF:

    def __init__(self):
        if TTF_Init() != 0:
            raise RuntimeError('TTF init failed: %s' % TTF_GetError())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def __del__(self):
        TTF_Quit()


class Window:

    def __init__(self, title, x, y, w, h, flags):
        self.handle = SDL_CreateWindow(title, x, y, w, h, flags)
        if self.handle is None:
            raise RuntimeError('Window init failed: %s}' % SDL_GetError())

    def __enter__(self):
        return self.handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def __del__(self):
        SDL_DestroyWindow(self.handle)
        self.handle = None
