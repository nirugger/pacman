from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.entity import Player

from typing import TypedDict
from enum import Enum, IntFlag


RESOLUTION = (1280, 720)
MAZE_X = 15
MAZE_Y = 15
EDGE_THICK = 3
PAD = 50

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
    NEW_GAME = 1
    WIN = 2
    LOSE = 3
    IN_GAME = 4


class LevelData(TypedDict):
    max_gums: int
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
    1: LevelData(max_gums=50, strategies={
        "red": ("follow", "follow", "random", "follow", "eight_cell"),
        "pink": ("anticipate", "random", "anticipate", "anticipate", "follow"),
        "cyan": ("eight_cell", "mirror", "eight_cell", "anticipate",
                 "eight_cell"),
        "orange": ("mirror", "mirror", "follow", "anticipate", "mirror")}),
    2: LevelData(max_gums=65, strategies={"red": ("follow",),
                                          "pink": ("anticipate",),
                                          "cyan": ("eight_cell",),
                                          "orange": ("mirror",)}),
    3: LevelData(max_gums=80, strategies={"red": ("follow",),
                                          "pink": ("anticipate",),
                                          "cyan": ("eight_cell",),
                                          "orange": ("mirror",)}),
}
