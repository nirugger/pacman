from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.level.cell import Cell

from src.data import MAZE_X, MAZE_Y, Dir, PACMAN_COLOR
from src.entities.strategy import Strategy

from abc import ABC, abstractmethod
import pygame as pg

PLAYER_SPEED = 100.0
RED_SPEED = 20000000
CYAN_SPEED = 30000000
PINK_SPEED = 20000000
ORANGE_SPEED = 100000000


class Character(ABC):
    def __init__(self):
        self.home: tuple[int, int]
        self.pos: tuple[int, int]
        self.target: tuple[int, int]
        self.movement: dict[str, int]
        self.speed: int

        self.rect: pg.Rect

        self.center: pg.math.Vector2
        self.target_center: pg.math.Vector2
        self.home_center: pg.math.Vector2

    def set_rect(self, graph: dict[tuple[int, int], 'Cell']) -> None:
        self.rect = graph[(self.pos[0], self.pos[1])].rect.copy()

    @abstractmethod
    def update_movement(self, graph: dict[tuple[int, int], Cell]) -> None:
        ...
    #
    # @abstractmethod
    # def update(self, graph: dict[tuple[int, int], Cell]) -> None:
    #     ...

    @abstractmethod
    def set_target_on_strategy(
        self,
        end: tuple[int, int],
        graph: dict[tuple[int, int], Cell],
        player: Player
         ) -> None:
        ...

    @abstractmethod
    def reset_positions(self, graph: dict[tuple[int, int], Cell]) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pg.Surface) -> None:
        ...


class Player(Character):
    def __init__(self) -> None:
        self.home = (MAZE_X // 2, MAZE_Y // 2)
        self.pos = self.home
        self.target = self.home
        self.last_valid_pos = self.home
        self.movement = {'x': 0, 'y': 0, 'nx': 0, 'ny': 0}
        self.speed = PLAYER_SPEED
        self.last_valid_module = 0
        self.lives: int = 3
        self.score: int = 0
        self.cheat: bool = False

    def set_target_on_strategy(
            self,
            end: tuple[int, int],
            graph: dict[tuple[int, int], Cell]
            ) -> None:
        return

    def update_movement(
            self,
            graph: dict[tuple[int, int], Cell]
            ) -> None:

        if self.movement['nx'] == 1:
            if graph[self.pos].value & Dir.E == 0 or self.cheat:
                self.movement['x'] = 1
                self.movement['y'] = 0
                self.movement['nx'] = 0
                self.movement['ny'] = 0
        if self.movement['nx'] == -1:
            if graph[self.pos].value & Dir.W == 0 or self.cheat:
                self.movement['x'] = -1
                self.movement['y'] = 0
                self.movement['nx'] = 0
                self.movement['ny'] = 0
        if self.movement['ny'] == -1:
            if graph[self.pos].value & Dir.N == 0 or self.cheat:
                self.movement['x'] = 0
                self.movement['y'] = -1
                self.movement['nx'] = 0
                self.movement['ny'] = 0
        if self.movement['ny'] == 1:
            if graph[self.pos].value & Dir.S == 0 or self.cheat:
                self.movement['x'] = 0
                self.movement['y'] = 1
                self.movement['nx'] = 0
                self.movement['ny'] = 0
        a, b = self.pos
        if self.movement['x'] == 1:
            if (graph[self.pos].value & Dir.E == 0
                    or (self.cheat and self.pos[0] != MAZE_X - 1)):
                self.target = (a + 1, b)
            else:
                self.target = self.pos
                self.movement['x'] = 0

        if self.movement['x'] == -1:
            if (graph[self.pos].value & Dir.W == 0
                    or (self.cheat and self.pos[0] != 0)):
                self.target = (a - 1, b)
            else:
                self.target = self.pos
                self.movement['x'] = 0

        if self.movement['y'] == -1:
            if (graph[self.pos].value & Dir.N == 0
                    or (self.cheat and self.pos[1] != 0)):
                self.target = (a, b - 1)
            else:
                self.target = self.pos
                self.movement['y'] = 0

        if self.movement['y'] == 1:
            if (graph[self.pos].value & Dir.S == 0
                    or (self.cheat and self.pos[1] != MAZE_Y - 1)):
                self.target = (a, b + 1)
            else:
                self.target = self.pos
                self.movement['y'] = 0

        if graph[self.pos].value != 15:
            self.last_valid_pos = self.pos

    def reset_positions(self, graph: dict[tuple[int, int], Cell]):
        self.pos = self.home
        self.movement = {'x': 0, 'y': 0, 'nx': 0, 'ny': 0}
        self.target = self.home
        self.rect.center = graph[self.home].rect.center
        self.center = self.rect.center
        self.last_valid_module = 0

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.circle(surface, PACMAN_COLOR, (int(self.center.x), int(self.center.y)), 13)


class Enemy(Character):
    def __init__(
            self,
            color: str
            ) -> None:
        self.color = color
        self.movement = {'x': 0, 'y': 0}
        self.strategy: str = ''

    def set_target_on_strategy(
            self,
            end: tuple[int, int],
            graph: dict[tuple[int, int], Cell],
            player: Player
            ) -> None:
        match self.strategy:
            case "follow":
                self.target = Strategy.follow(self.pos, end, graph)
            case "random":
                self.target = Strategy.random(self.pos, graph)
            case "anticipate":
                self.target = Strategy.anticipate(self.pos, graph, player)
            case "eight_cell":
                self.target = Strategy.eight_cell(self.pos, graph, end,
                                                  self.home)

    def update_movement(
            self,
            graph: dict[tuple[int, int], Cell],
            ) -> None:

        x, y = self.pos
        nx, ny = self.target
        if nx < x:
            self.movement['x'] = -1
            self.movement['y'] = 0
        if nx > x:
            self.movement['x'] = 1
            self.movement['y'] = 0
        if ny < y:
            self.movement['x'] = 0
            self.movement['y'] = -1
        if ny > y:
            self.movement['x'] = 0
            self.movement['y'] = 1
        if nx == x and ny == y:
            self.movement['x'] = 0
            self.movement['y'] = 0

    def reset_positions(self, graph: dict[tuple[int, int], Cell]):
        self.pos = self.home
        self.target = self.home
        self.movement = {'x': 0, 'y': 0}
        self.rect.center = graph[self.home].rect.center
        self.last_valid_module = 0

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.circle(surface, self.color, self.rect.center, 13)


class Red(Enemy):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.home = (0, MAZE_Y - 1)
        self.pos = self.home
        self.target = self.pos
        self.strategy = "follow"
        self.speed = RED_SPEED
        self.last_valid_module = 0


class Pink(Enemy):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.home = (0, 0)
        self.pos = self.home
        self.target = self.pos
        self.strategy = "anticipate"
        self.speed = PINK_SPEED
        self.last_valid_module = 0


class Cyan(Enemy):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.home = (MAZE_X - 1, 0)
        self.pos = self.home
        self.target = self.pos
        self.strategy = "eight_cell"
        self.speed = CYAN_SPEED
        self.last_valid_module = 0


class Orange(Enemy):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.home = (MAZE_X - 1, MAZE_Y - 1)
        self.pos = self.home
        self.target = self.pos
        self.strategy = "random"
        self.speed = ORANGE_SPEED
        self.last_valid_module = 0
