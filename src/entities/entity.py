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


class Prop(GameObject):
    def __init__(self, position: list[int], width: int, height: int,
                 color: pg.Color = pg.Color('white')):
        super().__init__(position, width, height)


class PacGum(Prop):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)


class SuperGum(Prop):
    def __init__(self, position: list[int], width: int, height: int) -> None:
        super().__init__(position, width, height)


class Character(GameObject):
    def __init__(self, position: list[int], width: int, height: int, graph: dict[tuple[int, int], pg.Rect]) -> None:
        super().__init__(position, width, height)
        self.graph = graph

    def move(self, dt: int) -> None:
        pass


class Player(Character):
    def __init__(self, position: list[int], width: int, height: int, graph: dict[tuple[int, int], pg.Rect]) -> None:
        super().__init__(position, width, height, graph)
        self.lives = 3
        self.score = 0

    def get_player_position(self, graph: dict[tuple[int, int], int]):
        pass


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
