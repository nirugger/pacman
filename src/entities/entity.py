from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.level.cell import Cell

from src.data import MAZE_X, MAZE_Y, Dir, PACMAN_COLOR
from src.entities.strategy import Strategy

from abc import ABC, abstractmethod
import pygame as pg

PLAYER_SPEED = 120.0
RED_SPEED = 115.0
CYAN_SPEED = 100.0
PINK_SPEED = 110.0
ORANGE_SPEED = 105.0


class Entity(ABC):
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

    @abstractmethod
    def set_target_on_strategy(self,
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


class Player(Entity):
    def __init__(self) -> None:
        self.home = (MAZE_X // 2, MAZE_Y // 2)
        self.pos = self.home
        self.target = self.home
        self.last_valid_pos = self.home
        self.movement = {'x': 0, 'y': 0, 'nx': 0, 'ny': 0}
        self.speed = PLAYER_SPEED
        self.lives: int = 99
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

    def reset_positions(self, graph: dict[tuple[int, int], Cell]) -> None:
        self.pos = self.home
        self.target = self.home
        # self.rect.center = graph[self.home].rect.center
        self.center = graph[self.home].center.copy()
        self.movement = {'x': 0, 'y': 0, 'nx': 0, 'ny': 0}

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.circle(surface, PACMAN_COLOR,
                       (int(self.center.x), int(self.center.y)), 13)


class Enemy(Entity):
    def __init__(
            self,
            color: str,
            strategy: tuple[str, ...]
            ) -> None:
        self.color = color
        self.movement = {'x': 0, 'y': 0}
        self.strategy = strategy
        # self.strategy: str = ''
        self.turn: int = 0
        self.frightened = False
        self.going_home = False

    def set_target_on_strategy(
            self,
            end: tuple[int, int],
            graph: dict[tuple[int, int], Cell],
            player: Player,
            red_pos: tuple[int, int],
            scatter: bool
            ) -> None:
        if self.going_home:
            self.target = Strategy.follow(self.pos, self.home, graph)
            if self.pos == self.home:
                self.going_home = False
            return
        if self.frightened:
            strat = "random"
        elif scatter:
            strat = "scatter"
        else:
            strat = self.strategy[self.turn % len(self.strategy)]
        match strat:
            case "follow":
                self.target = Strategy.follow(self.pos, end, graph)
            case "random":
                self.target = Strategy.random(self.pos, graph)
            case "anticipate":
                self.target = Strategy.anticipate(self.pos, graph, player)
            case "eight_cell":
                self.target = Strategy.eight_cell(self.pos, graph, end,
                                                  self.home)
            case "mirror":
                self.target = Strategy.mirror(self.pos, red_pos, player.pos,
                                              graph, player.last_valid_pos)
            case "scatter":
                self.target = Strategy.scatter(self.pos, self.home, graph)

    def update_movement(
            self,
            graph: dict[tuple[int, int], Cell],
            ) -> None:
        self.turn += 1
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

    def reset_positions(self, graph: dict[tuple[int, int], Cell]) -> None:
        self.pos = self.home
        self.target = self.home
        self.movement = {'x': 0, 'y': 0}
        self.rect.center = graph[self.home].rect.center
        self.center = graph[self.home].center.copy()
        self.frightened = False

    def draw(self, surface: pg.Surface) -> None:
        # pg.draw.circle(surface, self.color, self.rect.center, 13)
        if self.frightened:
            pg.draw.circle(surface, 'white',
                           (int(self.center.x), int(self.center.y)), 13)
            return
        if self.going_home:
            pg.draw.circle(surface, 'blue',
                           (int(self.center.x), int(self.center.y)), 13)
            return
        pg.draw.circle(surface, self.color,
                       (int(self.center.x), int(self.center.y)), 13)


class Red(Enemy):
    def __init__(self, color: str, strategy: tuple[str, ...]) -> None:
        super().__init__(color, strategy)
        self.home = (0, MAZE_Y - 1)
        self.pos = self.home
        self.target = self.pos
        self.speed = RED_SPEED


class Pink(Enemy):
    def __init__(self, color: str, strategy: tuple[str, ...]) -> None:
        super().__init__(color, strategy)
        self.home = (0, 0)
        self.pos = self.home
        self.target = self.pos
        self.speed = PINK_SPEED


class Cyan(Enemy):
    def __init__(self, color: str, strategy: tuple[str, ...]) -> None:
        super().__init__(color, strategy)
        self.home = (MAZE_X - 1, 0)
        self.pos = self.home
        self.target = self.pos
        self.speed = CYAN_SPEED


class Orange(Enemy):
    def __init__(self, color: str, strategy: tuple[str, ...]) -> None:
        super().__init__(color, strategy)
        self.home = (MAZE_X - 1, MAZE_Y - 1)
        self.pos = self.home
        self.target = self.pos
        self.speed = ORANGE_SPEED
