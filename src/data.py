from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.entity import Player

from typing import TypedDict
from enum import Enum, IntFlag


RESOLUTION = (1280, 720)
MAZE_X = 13
MAZE_Y = 13
EDGE_THICK = 3
PAD = 15

CELL_COLOR = (100, 0, 255)
PACMAN_COLOR = (255, 255, 0)
GUM_COLOR = (120, 255, 0)
SUPERGUM_COLOR = (120, 255, 0)

FRUIT_TIME = 10
SUPERGUM_TIME = 12
LEVEL_TIME = 900

FRUIT_POINTS = 300
GHOST_POINTS = 200
SUPERGUM_POINTS = 50
GUM_POINTS = 10
STRATEGIES = ("follow", "random")


class Dir(IntFlag):
    N = 1
    E = 2
    S = 4
    W = 8


class GameState(Enum):

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


class LevelData(TypedDict):
    max_gums: int
    time: int
    strategies: dict[str, tuple[str, ...]]


class LevelConfig(TypedDict):

    player: Player
    # enemies: list[Enemy]
    # entities: list[Entity]
    data: LevelData
    game_state: GameState
    # status: GameStatus
    # super_gums: list[SuperGum]


LEVELS_DATA = {
    1: LevelData(max_gums=50, time=300, strategies={
        "red": ("follow", "follow", "random", "follow", "eight_cell"),
        "pink": ("anticipate", "random", "anticipate", "anticipate", "follow"),
        "cyan": ("eight_cell", "mirror", "eight_cell", "anticipate",
                 "eight_cell"),
        "orange": ("mirror", "mirror", "follow", "anticipate", "mirror")}),
    2: LevelData(max_gums=65, time=280, strategies={"red": ("follow",),
                                                    "pink": ("anticipate",),
                                                    "cyan": ("eight_cell",),
                                                    "orange": ("mirror",)}),
    3: LevelData(max_gums=80, time=260, strategies={"red": ("follow",),
                                                    "pink": ("anticipate",),
                                                    "cyan": ("eight_cell",),
                                                    "orange": ("mirror",)}),
    4: LevelData(max_gums=95, time=240, strategies={"red": ("follow",),
                                                    "pink": ("anticipate",),
                                                    "cyan": ("eight_cell",),
                                                    "orange": ("mirror",)}),
    5: LevelData(max_gums=110, time=220, strategies={"red": ("follow",),
                                                     "pink": ("anticipate",),
                                                     "cyan": ("eight_cell",),
                                                     "orange": ("mirror",)}),
    6: LevelData(max_gums=125, time=200, strategies={"red": ("follow",),
                                                     "pink": ("anticipate",),
                                                     "cyan": ("eight_cell",),
                                                     "orange": ("mirror",)}),
    7: LevelData(max_gums=140, time=180, strategies={"red": ("follow",),
                                                     "pink": ("anticipate",),
                                                     "cyan": ("eight_cell",),
                                                     "orange": ("mirror",)}),
    8: LevelData(max_gums=155, time= 160,  strategies={"red": ("follow",),
                                                       "pink": ("anticipate",),
                                                       "cyan": ("eight_cell",),
                                                       "orange": ("mirror",)}),
    9: LevelData(max_gums=160, time=140,  strategies={"red": ("follow",),
                                                      "pink": ("anticipate",),
                                                      "cyan": ("eight_cell",),
                                                      "orange": ("mirror",)}),
    10: LevelData(max_gums=164, time=120, strategies={"red": ("follow",),
                                                      "pink": ("anticipate",),
                                                      "cyan": ("eight_cell",),
                                                      "orange": ("mirror",)}),
}
