from typing import TypedDict
from src.entities.entity import Player, Enemy


CELL_COLOR = (255, 0, 0)
LEVEL_SPEED = 2
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


class LevelConfig(TypedDict):

    player: Player
    enemies: list[Enemy]
    speed: int
    # super_gums: list[SuperGum]
