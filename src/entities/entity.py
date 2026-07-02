"""Define all the characters of the game."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.level.cell import Cell

from src.data import MAZE_X, MAZE_Y, Dir, EDGE_THICK
from src.entities.strategy import Strategy

from abc import ABC, abstractmethod
import pygame as pg


# PLAYER_SPEED = 120 + 80
# RED_SPEED = 100 + 80
# CYAN_SPEED = 81 + 80
# PINK_SPEED = 100 + 80
# ORANGE_SPEED = 90 + 80


class Entity(ABC):
    """Abstract class for all the characters of the game."""

    def __init__(self, name: str) -> None:
        """Initialize the entity with a name and set up its attributes."""
        self.name: str = name
        self.home: tuple[int, int]
        self.pos: tuple[int, int]
        self.target: tuple[int, int]
        self.movement: dict[str, int]
        self.speed: int
        self.speed_mult: float
        self.color: str | tuple[int, int, int]

        self.rect: pg.Rect

        self.center: pg.math.Vector2
        self.target_center: pg.math.Vector2
        self.home_center: pg.math.Vector2

    def set_rect(self, graph: dict[tuple[int, int], 'Cell']) -> None:
        """Set the rectangle of the entity.

        Such that rectangle will be used for rendering the entity, and it is
        based on the position in the maze: more precisely, is it a copy of the
        rectangle of the cell in the maze corresponding to the entity's
        position.

        Args:
            graph (dict[tuple[int, int], Cell]): The maze graph where each cell
            is represented by its coordinates and a Cell object.
        """
        self.rect = graph[(self.pos[0], self.pos[1])].rect.copy()

    # def set_speed(self)

    @abstractmethod
    def update_movement(self, graph: dict[tuple[int, int], Cell]) -> None:
        """Update the movement of the entity."""
        ...

    @abstractmethod
    def set_target_on_strategy(self,
                               end: tuple[int, int],
                               graph: dict[tuple[int, int], Cell],
                               player: Player,
                               red_pos: tuple[int, int],
                               scatter: bool
                               ) -> None:
        """Define the next cell the entity will move to.

        Args:
            end (tuple[int, int]): The target position for the entity.
            graph (dict[tuple[int, int], Cell]): The maze graph where each cell
            is represented by its coordinates and a Cell object.
            player (Player): The player object, used for certain strategies.
            red_pos (tuple[int, int]): The position of the red enemy, used for
            certain strategies.
            scatter (bool): A flag indicating whether the entity should scatter
            or not, affecting its strategy.
        """
        ...

    @abstractmethod
    def reset_positions(self, graph: dict[tuple[int, int], Cell]) -> None:
        """Set the entity's position back to its home position.

        Args:
            graph (dict[tuple[int, int], Cell]): The maze graph where each cell
            is represented by its coordinates and a Cell object.
        """
        ...

    @abstractmethod
    def draw(self, surface: pg.Surface, radius: int) -> None:
        """Draw the entity on the given surface.

        Args:
            surface (pg.Surface): The surface on which to draw the entity.
            radius (int): The radius of the circle representing the entity.
        """
        ...


class Player(Entity):
    """Class representing the player character in the game."""

    def __init__(self, name: str) -> None:
        """Initialize the player with a name and set up its attributes."""
        self.name = name
        self.home = (MAZE_X // 2, MAZE_Y // 2)
        self.pos = self.home
        self.target = self.home
        self.last_valid_pos = self.home
        self.movement = {'x': 0, 'y': 0, 'nx': 0, 'ny': 0}
        self.speed: int
        self.lives: int = 3
        self.score: int = 0
        self.cheat: bool = False
        self.has_been_cheating: bool = False

    def set_target_on_strategy(
            self,
            end: tuple[int, int],
            graph: dict[tuple[int, int], Cell],
            player: Player,
            red_pos: tuple[int, int],
            scatter: bool
            ) -> None:
        """Do nothing, as the player does not have a strategy for movement.

        Args:
            end (tuple[int, int]): The target position for the entity.
            graph (dict[tuple[int, int], Cell]): The maze graph where each cell
            is represented by its coordinates and a Cell object.
            player (Player): The player object, used for certain strategies.
            red_pos (tuple[int, int]): The position of the red enemy, used for
            certain strategies.
            scatter (bool): A flag indicating whether the entity should scatter
            or not, affecting its strategy.
        """
        return

    def update_movement(
            self,
            graph: dict[tuple[int, int], Cell]
            ) -> None:
        """Update the player's movement.

        Check the next intended direction and, when such direction is
        available, update the current movement accordingly. Then check the
        current movement and set the player's target accordingly. Eventually,
        save the player's last valid position to avoid crashes in cheating
        mode.
        Args:
            graph (dict[tuple[int, int], Cell]): The maze graph where each cell
            is represented by its coordinates and a Cell object.
        """
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
        """Reset the player's position and movement.

        Args:
            graph (dict[tuple[int, int], Cell]): The maze graph where each
            cell is represented by its coordinates and a Cell object.
        """
        self.pos = self.home
        self.target = self.home
        # self.rect.center = graph[self.home].rect.center
        self.center = graph[self.home].center.copy()
        self.movement = {'x': 0, 'y': 0, 'nx': 0, 'ny': 0}

    def draw(self, surface: pg.Surface, radius: int) -> None:
        """Draw the player on the given surface.

        Args:
            surface (pg.Surface): The surface on which to draw the player.
            radius (int): The radius of the circle representing the player.
        """
        pg.draw.circle(surface, self.color,
                       (int(self.center.x) + EDGE_THICK,
                        int(self.center.y) + EDGE_THICK),
                       radius)


class Enemy(Entity):
    """Class representing an enemy character in the game."""

    def __init__(
            self,
            name: str,
            color: str | tuple[int, int, int],
            strategy: tuple[str, ...]
            ) -> None:
        """Initialize the enemy with a name, color, and strategy.

        Args:
            name (str): The name of the enemy.
            color (str | tuple[int, int, int]): The color of the enemy, either
            as a string or an RGB tuple.
            strategy (tuple[str, ...]): A tuple of strategies that the enemy
            will follow during the game.
        """
        self.name = name
        self.color = color
        self.movement = {'x': 0, 'y': 0}
        self.strategy = strategy
        # self.strategy: str = ''
        self.turn: int = 0
        self.frightened: float = 0.0
        self.going_home = False
        self.waiting = False
        self.last_wait = 0.0

    def _check_wait(self) -> None:
        if time.time() - self.last_wait > 5.0:
            self.waiting = False

    def set_target_on_strategy(
            self,
            end: tuple[int, int],
            graph: dict[tuple[int, int], Cell],
            player: Player,
            red_pos: tuple[int, int],
            scatter: bool
            ) -> None:
        """Set the next cell the enemy will move to.

        Args:
            end (tuple[int, int]): The target position for the enemy.
            graph (dict[tuple[int, int], Cell]): The maze graph where each cell
            is represented by its coordinates and a Cell object.
            player (Player): The player object, used for certain strategies.
            red_pos (tuple[int, int]): The position of the red enemy, used for
            certain strategies.
            scatter (bool): A flag indicating whether the enemy should scatter
            or not, affecting its strategy.
        """
        self._check_wait()
        if self.waiting:
            return
        if self.going_home:
            self.target = Strategy.follow(self.pos, self.home, graph)
            if self.pos == self.home:
                self.last_wait = time.time()
                self.going_home = False
                self.waiting = True
            return
        if self.frightened:
            strat = "random"
        elif scatter:
            strat = "scatter"
        elif self.waiting:
            self.target = Strategy.follow(self.pos, self.home, graph)
            return
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
        if self.target == self.pos:
            self.target = Strategy.random(self.pos, graph)

    def update_movement(
            self,
            graph: dict[tuple[int, int], Cell],
            ) -> None:
        """Update the enemy's movement based on its target.

        Args:
            graph (dict[tuple[int, int], Cell]): The maze graph where each cell
            is represented by its coordinates and a Cell object.
        """
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
        """Reset the enemy's position to its home position.

        Args:
            graph (dict[tuple[int, int], Cell]): The maze graph where each cell
            is represented by its coordinates and a Cell object.
        """
        self.pos = self.home
        self.target = self.home
        self.movement = {'x': 0, 'y': 0}
        self.rect.center = graph[self.home].rect.center
        self.center = graph[self.home].center.copy()
        self.frightened: float = 0.0

    def draw(self, surface: pg.Surface, radius: int) -> None:
        """Draw the enemy on the given surface.

        Args:
            surface (pg.Surface): The surface on which to draw the enemy.
            radius (int): The radius of the circle representing the enemy.
        """
        if self.frightened:
            if self.frightened >= 3.0:
                pg.draw.circle(surface, 'white',
                               (int(self.center.x) + EDGE_THICK,
                                int(self.center.y) + EDGE_THICK), radius)
                return
            else:
                color = ('white'
                         if self.frightened - int(self.frightened) <= 0.5
                         else self.color)
                pg.draw.circle(surface, color,
                               (int(self.center.x) + EDGE_THICK,
                                int(self.center.y) + EDGE_THICK), radius)
                return

        if self.going_home:
            pg.draw.circle(surface, 'blue',
                           (int(self.center.x) + EDGE_THICK,
                            int(self.center.y) + EDGE_THICK), radius)
            return

        pg.draw.circle(surface, self.color,
                       (int(self.center.x) + EDGE_THICK,
                        int(self.center.y) + EDGE_THICK), radius)


class Red(Enemy):
    """Class representing the red enemy character in the game."""

    def __init__(self, name: str, color: str | tuple[int, int, int],
                 strategy: tuple[str, ...]) -> None:
        """Initialize the red enemy with a name, color, and strategy."""
        super().__init__(name, color, strategy)
        self.home = (0, MAZE_Y - 1)
        self.pos = self.home
        self.target = self.pos
        self.speed: int


class Pink(Enemy):
    """Class representing the pink enemy character in the game."""

    def __init__(self, name: str, color: str | tuple[int, int, int],
                 strategy: tuple[str, ...]) -> None:
        """Initialize the pink enemy with a name, color, and strategy."""
        super().__init__(name, color, strategy)
        self.home = (0, 0)
        self.pos = self.home
        self.target = self.pos
        self.speed: int


class Cyan(Enemy):
    """Class representing the cyan enemy character in the game."""

    def __init__(self, name: str, color: str | tuple[int, int, int],
                 strategy: tuple[str, ...]) -> None:
        """Initialize the cyan enemy with a name, color, and strategy."""
        super().__init__(name, color, strategy)
        self.home = (MAZE_X - 1, 0)
        self.pos = self.home
        self.target = self.pos
        self.speed: int


class Orange(Enemy):
    """Class representing the orange enemy character in the game."""

    def __init__(self, name: str, color: str | tuple[int, int, int],
                 strategy: tuple[str, ...]) -> None:
        """Initialize the orange enemy with a name, color, and strategy."""
        super().__init__(name, color, strategy)
        self.home = (MAZE_X - 1, MAZE_Y - 1)
        self.pos = self.home
        self.target = self.pos
        self.speed: int
