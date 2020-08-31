from maze import *
from config import *
from extraSDL import *
from userConfig import CELL


def finite_interval(start: int, finish: int, step: int = 1) -> range:
    return range(start, finish + 1, step)


# SECTION: Various crutches

def cell_index_for_position(x, y) -> (int, int):
    """Returns cell's index calculated on passed position.
    All calculations based on application window coordinate system."""
    i = j = 0

    y_start = 0
    for index, y_end in enumerate(finite_interval(CELL_HEIGHT, WIN_HEIGHT, CELL_HEIGHT)):
        if y in finite_interval(y_start, y_end):
            i = index

        y_start = y_end + 1

    x_start = 0
    for index, x_end in enumerate(finite_interval(CELL_WIDTH, WIN_WIDTH, CELL_WIDTH)):
        if x in finite_interval(x_start, x_end):
            j = index

        x_start = x_end + 1

    return i, j


def fetch_mouse_position() -> (int, int):
    """Returns mouse coordinates relative to the application window."""
    x = c_int()
    y = c_int()
    SDL_GetMouseState(x, y)

    # c_int -> int
    x, y = x.value, y.value

    return x, y


def draw_cell(cell, color: SDL_Color):
    cell_rect = SDL_Rect(cell.j * CELL_WIDTH, cell.i * CELL_HEIGHT,
                         CELL_WIDTH, CELL_HEIGHT)

    cell_surface = SDL_CreateRGBSurface(SUPPRESS_DEPRECATED_FLAGS,
                                        cell_rect.w, cell_rect.h,
                                        TRUE_COLOR_PLUS_ALPHA,
                                        R_MASK, G_MASK, B_MASK, A_MASK)
    SDL_FillRect(cell_surface,
                 SDL_Rect(0, 0, cell_rect.w, cell_rect.h),
                 SDL_MapRGB(screen_info.format,
                            color.r, color.g, color.b))

    SDL_BlitSurface(cell_surface, None, screen_ptr, cell_rect)
    SDL_FreeSurface(cell_surface)

    SDL_UpdateWindowSurface(window.handle)


def reset_background():
    SDL_BlitSurface(background, None, screen_ptr, None)
    SDL_UpdateWindowSurface(window.handle)


# SECTION: Event handlers

kind_name_to_val = {
    'REGULAR': REGULAR,
    'WALL': WALL,
    'START': START,
    'FINISH': FINISH
}

prev_path = None


def handle_keydown(key):
    if key == PATH_KEY:
        global prev_path

        if prev_path:
            for cell in prev_path:
                # We have to assure that each cell from the previous path
                # has PATH kind before resetting it to REGULAR.
                if maze.cell_for_index(cell.i, cell.j).kind == PATH:
                    maze.set(cell, REGULAR)
                    draw_cell(cell, REGULAR_COLOR)

        if maze.start and maze.finish:
            path = maze.bfs_path(maze.start, maze.finish)

            if path:
                prev_path = path

                for cell in path:
                    maze.set(cell, PATH)
                    draw_cell(cell, PATH_COLOR)

    elif key in PLOTTING_KEYS:
        kind = None
        for action, button in CELL['KEYS'].items():
            if key == button:
                kind = action

        x, y = fetch_mouse_position()
        i, j = cell_index_for_position(x, y)

        mouseovered_cell = maze.cell_for_index(i, j)

        # Redrawing old start / finish with REGULAR color
        if kind == 'START':
            if maze.start:
                draw_cell(maze.start, REGULAR_COLOR)
            maze.start = mouseovered_cell

        elif kind == 'FINISH':
            if maze.finish:
                draw_cell(maze.finish, REGULAR_COLOR)
            maze.finish = mouseovered_cell

        maze.set(mouseovered_cell, kind_name_to_val[kind])
        draw_cell(mouseovered_cell, CELL['COLORS'][kind])


# SECTION: Entry point. Event loop.

with SDL(SDL_INIT_VIDEO):
    window = Window(WIN_TITLE,
                    SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                    WIN_WIDTH, WIN_HEIGHT,
                    SDL_WINDOW_ALLOW_HIGHDPI | SDL_WINDOW_SHOWN)

    screen_ptr = SDL_GetWindowSurface(window.handle)
    # screen_ptr - C struct pointer. We can
    # access its data via contents attribute
    screen_info = screen_ptr.contents

    background = SDL_CreateRGBSurface(SUPPRESS_DEPRECATED_FLAGS,
                                      screen_info.w, screen_info.h,
                                      TRUE_COLOR_PLUS_ALPHA,
                                      R_MASK, G_MASK, B_MASK, A_MASK)
    SDL_FillRect(background,
                 SDL_Rect(0, 0, screen_info.w, screen_info.h),
                 SDL_MapRGB(screen_info.format,
                            WIN_BG.r, WIN_BG.g, WIN_BG.b))

    reset_background()

    maze = Maze(i_size=WIN_HEIGHT // CELL_HEIGHT,
                j_size=WIN_WIDTH // CELL_WIDTH)

    running = True
    while running:
        e = SDL_Event()
        SDL_PollEvent(e)

        if e.type == SDL_QUIT:
            running = False
        if e.type == SDL_KEYDOWN:
            handle_keydown(e.key.keysym.sym)

    SDL_FreeSurface(background)
