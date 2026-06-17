from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.entity import Player, Enemy


from typing import TypedDict
from enum import Enum, IntFlag


CELL_COLOR = (255, 0, 0)
PAD = 50
SUPERGUM_POINTS = 50
GUM_POINTS = 10
PACMAN_COLOR = (255, 255, 0)
PLAYER_SPEED = 10
GUM_COLOR = (0, 0, 255)
SUPERGUM_COLOR = (255, 255, 0)
RESOLUTION = (1280, 720)
MAZE_X = 15
MAZE_Y = 15


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
    data: LevelData
    game_state: GameState
    # status: GameStatus
    # super_gums: list[SuperGum]


LEVELS_DATA = {
    1: LevelData(speed=5, max_gums=0),
    2: LevelData(speed=4, max_gums=100),
    3: LevelData(speed=5, max_gums=150),
    }
