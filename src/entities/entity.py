from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.level.cell import Cell

from src.data import MAZE_X, MAZE_Y
from src.entities.strategies import Strategy

from abc import ABC, abstractmethod

import pygame as pg


# class Prop(GameObject):
#     def __init__(self, pos: tuple[int, int width: int, height: int,
#                  color: pg.Color = pg.Color('white')):
#         super().__init__(width, height)


# class PacGum(Prop):
#     def __init__(self, pos: list[int], width: int, height: int) -> None:
#         super().__init__(width, height)


# class SuperGum(Prop):
#     def __init__(self, pos: list[int], width: int, height: int) -> None:
#         super().__init__(width, height)


class Character(ABC):

    def set_rect(self, graph: dict[tuple[int, int], 'Cell']) -> None:
        self.rect = graph[(self.pos[0], self.pos[1])].rect.copy()

    # @abstractmethod
    def move(self, dt: int) -> None:
        pass


class Player(Character):
    def __init__(self) -> None:
        self.home = (MAZE_X // 2, MAZE_Y // 2)
        self.pos = self.home
        self.target: tuple[int, int] = self.pos
        self.lives = 3
        self.score = 0
        self.moving: dict[str, int] = {'x_now': 0, 'y_now': 0, 'x_next': 0, 'y_next': 0}


class Enemy(Character):
    def __init__(self, color: str) -> None:
        self.color = color
        self.moving: dict[str, int] = {'x': 0, 'y': 0}

    def move(self, graph: dict[tuple[int, int], Cell], end: tuple[int, int]) -> None:
        self.target = Strategy.follow(self.pos, end, graph)
        print(self.target)
        x, y = self.pos
        nx, ny = self.target
        if nx < x:
            self.moving['x'] = -1
            self.moving['y'] = 0
        if nx > x:
            self.moving['x'] = 1
            self.moving['y'] = 0
        if ny < y:
            self.moving['x'] = 0
            self.moving['y'] = -1
        if ny > y:
            self.moving['x'] = 0
            self.moving['y'] = 1
        if nx == x and ny == y:
            self.moving['x'] = 0
            self.moving['y'] = 0


class Red(Enemy):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.home = (0, MAZE_Y - 1)
        self.pos = self.home
        self.target = self.pos


class Pink(Enemy):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.home = (0, 0)
        self.pos = self.home
        self.target = self.pos


class Cyan(Enemy):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.home = (MAZE_X - 1, 0)
        self.pos = self.home
        self.target = self.pos


class Orange(Enemy):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.home = (MAZE_X - 1, MAZE_Y - 1)
        self.pos = self.home
        self.target = self.pos
