from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.level.cell import Cell


from abc import ABC, abstractmethod

import pygame as pg


class GameObject(ABC):
    """Define the common attributes for all game objects"""
    def __init__(self, position: list[int], width: int,
                 height: int) -> None:
        if not 0 <= position[0] < width:
            raise ValueError("Each game object must fit in the maze")
        if not 0 <= position[1] < height:
            raise ValueError("Each game object must fit in the maze")
        self.pos = position


# class Prop(GameObject):
#     def __init__(self, position: list[int], width: int, height: int,
#                  color: pg.Color = pg.Color('white')):
#         super().__init__(position, width, height)


# class PacGum(Prop):
#     def __init__(self, position: list[int], width: int, height: int) -> None:
#         super().__init__(position, width, height)


# class SuperGum(Prop):
#     def __init__(self, position: list[int], width: int, height: int) -> None:
#         super().__init__(position, width, height)


class Character(GameObject):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)
        self.rect: pg.Rect

    def set_rect(self, graph: dict[tuple[int, int], 'Cell']) -> None:
        self.rect = graph[(self.pos[0], self.pos[1])].rect.copy()

    def move(self, dt: int) -> None:
        pass


class Player(Character):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)
        self.lives = 3
        self.score = 0
        self.moving: dict[str, int] = {'x_now': 0, 'y_now': 0, 'x_next': 0, 'y_next': 0}


class Enemy(Character):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)


class Red(Enemy):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)


class Pink(Enemy):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)


class Cyan(Enemy):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)


class Orange(Enemy):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)
