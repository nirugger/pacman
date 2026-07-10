"""Contain utility macros, classes and functions for the game."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.entity import Player

import os
from typing import TypedDict
from enum import Enum, IntFlag
import pygame as pg


def dc_draw_line(x_0: int, y_0: int, x_1: int, y_1: int,
                 surface: pg.Surface,
                 color: str | tuple[int, int, int]) -> None:
    """Draw a line pixel by pixel.
    
    Args:
        x_0 (int): the x coordinate of the starting point.
        y_0 (int): the y coordinate of the starting point.
        x_1 (int): the x coordinate of the end point.
        y_1 (int): the y coordinate of the end point.
        surface (pg.Surface): the surface to draw on.
        color (str | tuple[int, int, int]): the line color.
    """
    dx: int = abs(x_1 - x_0)
    dy: int = -abs(y_1 - y_0)
    err: int = dx + dy
    e2: int
    s_x: int = 1 if x_0 < x_1 else -1
    s_y: int = 1 if y_0 < y_1 else -1
    color_value = pg.Color(color)
    while True:
        surface.set_at((x_0, y_0), color_value)
        if x_0 == x_1 and y_0 == y_1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x_0 += s_x
        if e2 <= dx:
            err += dx
            y_0 += s_y


def dc_fill_square(top_left: tuple[int, int], edge: int, surface: pg.Surface,
                   color: str | tuple[int, int, int]) -> None:
    """Draw a full square.
    
    Args:
        top_left (tuple[int, int]): coordinates of square top left.
        edge (int): the edge of the square.
        surface (pg.Surface): the surface to draw on.
        color (str | tuple[int, int, int]): the color of the square.
    """
    color_value = pg.Color(color)
    for i in range(edge):
        for j in range(edge):
            surface.set_at((top_left[0] + i, top_left[1] + j), color_value)


FONT_DIR = os.path.join('assets/fonts')
FONT = os.path.join(FONT_DIR, 'PressStart2P-Regular.ttf')
RESOLUTION = (1280, 720)
MAZE_X = 21
MAZE_Y = 14
EDGE_THICK = 1
EDGE = 30
PAD = 15
FILENAME = 'config.json'

# PACMAN_R = 21
# GHOST_R = 14
# GUM_R = 2
# SGUM_R = 6
# FRUIT_R = 8


CELL_COLOR = (100, 0, 255)
PACMAN_COLOR = (255, 255, 0)
GUM_COLOR = (120, 255, 0)
SUPERGUM_COLOR = (120, 255, 0)

FRUIT_TIME = 10
SUPERGUM_TIME = 12
LEVEL_TIME = 900
MAX_PACGUMS = MAZE_Y * MAZE_X - 23

FRUIT_POINTS = 30
GHOST_POINTS = 20
SUPERGUM_POINTS = 5
GUM_POINTS = 1

ARROWS = {"left": "\u2190",
          "up": "\u2191",
          "right": "\u2192",
          "down": "\u2193"}


ENT_SPEED = {
    'pacman': 200,
    'red': 190,
    'pink': 175,
    'cyan': 185,
    'orange': 180,
}


class Dir(IntFlag):
    """Set the values of the directions as bit flags for easy manipulation."""

    N = 1
    E = 2
    S = 4
    W = 8


class GameState(Enum):
    """Enumerate the different states of the game."""

    MAIN_MENU = 1
    CONTINUE = 2
    NEW_GAME = 3
    HIGHSCORES = 4
    INSTRUCTIONS = 5
    RECORD = 6
    RECORD_CONFIRM = 7
    RESET_CONFIRM = 9
    IN_GAME = 11
    WIN = 12
    LOSE = 13


class Config(TypedDict):
    """Define the configuration settings for the game."""

    highscore_filename: str
    resolution: dict[str, int]
    seed: int


class LevelData(TypedDict):
    """Define the data structure for a game level."""

    max_gums: int
    time: int
    strategies: dict[str, tuple[str, ...]]
    palette: dict[str, tuple[int, int, int]]
    scatter_duration: float
    chase_duration: float


class LevelConfig(TypedDict):
    """Define the configuration for a game level."""

    player: Player
    data: LevelData
    game_state: GameState
    seed: int
    time: float
    edge: int
    radii: dict[str, int]
    font_mult: float
    speed_mult: float
    death_screen: pg.Surface
    death_screen_size: tuple[int, int]
    # enemies: list[Enemy]
    # entities: list[Entity]
    # status: GameStatus
    # super_gums: list[SuperGum]


PALETTES = {
    1: {"bg": (12, 14, 24), "walls": (110, 170, 255), "pacman": (255, 220, 40),
        "blinky": (255, 70, 70), "pinky": (255, 140, 220),
        "inky": (70, 255, 255), "clyde": (255, 170, 60),
        "pg": (245, 245, 245), "spg": (255, 245, 170),
        "fruit": (120, 255, 110), "text": (230, 230, 255), },

    2: {"bg": (18, 10, 32), "walls": (180, 140, 255), "pacman": (255, 210, 90),
        "blinky": (255, 70, 180), "pinky": (180, 110, 255),
        "inky": (70, 255, 220), "clyde": (120, 220, 255),
        "pg": (240, 240, 255), "spg": (255, 255, 180),
        "fruit": (90, 255, 160), "text": (220, 210, 255), },

    3: {"bg": (6, 24, 38), "walls": (175, 225, 235), "pacman": (255, 214, 64),
        "blinky": (40, 200, 255), "pinky": (120, 255, 220),
        "inky": (100, 170, 255), "clyde": (210, 245, 255),
        "pg": (235, 245, 255), "spg": (255, 250, 190),
        "fruit": (110, 255, 140), "text": (210, 235, 245), },

    4: {"bg": (10, 20, 16), "walls": (160, 255, 215), "pacman": (255, 220, 70),
        "blinky": (70, 255, 120), "pinky": (120, 255, 180),
        "inky": (180, 255, 120), "clyde": (60, 210, 140),
        "pg": (235, 245, 240), "spg": (255, 250, 170),
        "fruit": (255, 120, 120), "text": (220, 255, 235), },

    5: {"bg": (30, 12, 18), "walls": (255, 170, 130), "pacman": (255, 225, 90),
        "blinky": (255, 90, 40), "pinky": (255, 140, 80),
        "inky": (255, 190, 60), "clyde": (255, 120, 120),
        "pg": (255, 245, 240), "spg": (255, 245, 180),
        "fruit": (255, 80, 150), "text": (255, 220, 205), },

    6: {"bg": (15, 18, 28), "walls": (210, 220, 255), "pacman": (255, 230, 99),
        "blinky": (220, 220, 255), "pinky": (170, 190, 255),
        "inky": (120, 170, 255), "clyde": (180, 240, 255),
        "pg": (250, 250, 255), "spg": (255, 255, 190),
        "fruit": (140, 255, 140), "text": (235, 240, 255), },

    7: {"bg": (26, 8, 40), "walls": (255, 120, 255), "pacman": (255, 220, 90),
        "blinky": (255, 40, 180), "pinky": (180, 40, 255),
        "inky": (40, 255, 255), "clyde": (120, 255, 120),
        "pg": (245, 240, 255), "spg": (255, 250, 180),
        "fruit": (255, 255, 120), "text": (255, 210, 255), },

    8: {"bg": (8, 20, 32), "walls": (200, 245, 255), "pacman": (255, 220, 75),
        "blinky": (180, 240, 255), "pinky": (120, 220, 255),
        "inky": (80, 170, 255), "clyde": (220, 255, 255),
        "pg": (245, 255, 255), "spg": (255, 255, 210),
        "fruit": (120, 255, 150), "text": (220, 245, 255), },

    9: {"bg": (12, 28, 18), "walls": (190, 235, 175), "pacman": (255, 220, 70),
        "blinky": (170, 255, 120), "pinky": (120, 220, 80),
        "inky": (220, 255, 120), "clyde": (80, 180, 60),
        "pg": (245, 250, 235), "spg": (255, 250, 170),
        "fruit": (255, 110, 110), "text": (220, 245, 215), },

    10: {"bg": (9, 9, 9), "walls": (210, 210, 210), "pacman": (255, 210, 60),
         "blinky": (255, 215, 120), "pinky": (210, 190, 120),
         "inky": (255, 240, 180), "clyde": (180, 160, 100),
         "pg": (245, 245, 245), "spg": (255, 235, 120),
         "fruit": (150, 255, 140), "text": (235, 235, 235), },
}

LEVELS_DATA = {
    1: LevelData(max_gums=MAX_PACGUMS // 2 + MAX_PACGUMS // 20, time=300,
                 palette=PALETTES[1],
                 strategies={
                    "red": ("follow", "random", "random", "random", "random"),
                    "pink": ("anticipate", "random", "random", "random",
                             "random"),
                    "cyan": ("eight_cell", "random", "random", "random",
                             "random"),
                    "orange": ("mirror", "random", "random", "random",
                               "random")},
                 scatter_duration=10.0,
                 chase_duration=20.0),
    2: LevelData(max_gums=MAX_PACGUMS // 2 + MAX_PACGUMS // 20, time=280,
                 palette=PALETTES[2],
                 strategies={
                    "red": ("follow", "follow", "random", "random", "random"),
                    "pink": ("anticipate", "anticipate", "random", "random",
                             "random"),
                    "cyan": ("eight_cell", "eight_cell", "random", "random",
                             "random"),
                    "orange": ("mirror", "mirror", "random", "random",
                               "random")},
                 scatter_duration=10.0,
                 chase_duration=25.0),
    3: LevelData(max_gums=MAX_PACGUMS // 2 + 2 * MAX_PACGUMS // 20, time=260,
                 palette=PALETTES[3],
                 strategies={
                    "red": ("follow", "follow", "follow", "random", "random"),
                    "pink": ("anticipate", "anticipate", "anticipate",
                             "random", "random"),
                    "cyan": ("eight_cell", "eight_cell", "eight_cell",
                             "random", "random"),
                    "orange": ("mirror", "mirror", "mirror", "random",
                               "random")},
                 scatter_duration=10.0,
                 chase_duration=30.0),
    4: LevelData(max_gums=MAX_PACGUMS // 2 + 3 * MAX_PACGUMS // 20, time=240,
                 palette=PALETTES[4],
                 strategies={
                    "red": ("follow", "follow", "follow", "follow", "random"),
                    "pink": ("anticipate", "anticipate", "anticipate",
                             "anticipate", "random"),
                    "cyan": ("eight_cell", "eight_cell", "eight_cell",
                             "eight_cell", "random"),
                    "orange": ("mirror", "mirror", "mirror", "mirror",
                               "random")},
                 scatter_duration=10.0,
                 chase_duration=35.0),
    5: LevelData(max_gums=MAX_PACGUMS // 2 + 4 * MAX_PACGUMS // 20, time=220,
                 palette=PALETTES[5],
                 strategies={
                    "red": ("follow",),
                    "pink": ("anticipate",),
                    "cyan": ("eight_cell",),
                    "orange": ("mirror",)},
                 scatter_duration=10.0,
                 chase_duration=40.0),
    6: LevelData(max_gums=MAX_PACGUMS // 2 + 5 * MAX_PACGUMS // 20, time=200,
                 palette=PALETTES[6],
                 strategies={
                    "red": ("follow",),
                    "pink": ("anticipate",),
                    "cyan": ("eight_cell",),
                    "orange": ("mirror",)},
                 scatter_duration=10.0,
                 chase_duration=45.0),
    7: LevelData(max_gums=MAX_PACGUMS // 2 + 6 * MAX_PACGUMS // 20, time=180,
                 palette=PALETTES[7],
                 strategies={
                    "red": ("follow",),
                    "pink": ("anticipate",),
                    "cyan": ("eight_cell",),
                    "orange": ("mirror",)},
                 scatter_duration=10.0,
                 chase_duration=50.0),
    8: LevelData(max_gums=MAX_PACGUMS // 2 + 7 * MAX_PACGUMS // 20, time=160,
                 palette=PALETTES[8],
                 strategies={
                    "red": ("follow",),
                    "pink": ("anticipate",),
                    "cyan": ("eight_cell",),
                    "orange": ("mirror",)},
                 scatter_duration=10.0,
                 chase_duration=55.0),
    9: LevelData(max_gums=MAX_PACGUMS // 2 + 8 * MAX_PACGUMS // 20, time=140,
                 palette=PALETTES[9],
                 strategies={
                    "red": ("follow",),
                    "pink": ("anticipate",),
                    "cyan": ("eight_cell",),
                    "orange": ("mirror",)},
                 scatter_duration=10.0,
                 chase_duration=60.0),
    10: LevelData(max_gums=MAX_PACGUMS, time=120, palette=PALETTES[10],
                  strategies={
        "red": ("follow",),
        "pink": ("anticipate",),
        "cyan": ("eight_cell",),
        "orange": ("mirror",)},
                  scatter_duration=10.0,
                  chase_duration=65.0),
}
