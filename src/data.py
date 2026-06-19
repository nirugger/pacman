from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.entity import Player, Enemy, Character

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
    speed: int
    max_gums: int


class LevelConfig(TypedDict):

    player: Player
    enemies: list[Enemy]
    entities: list[Character]
    data: LevelData
    game_state: GameState
    # status: GameStatus
    # super_gums: list[SuperGum]


LEVELS_DATA = {
    1: LevelData(speed=1, max_gums=50),
    2: LevelData(speed=1, max_gums=65),
    3: LevelData(speed=1, max_gums=80),
    }
