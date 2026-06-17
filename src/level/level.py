from enum import IntFlag
import pygame as pg
import sys

import random

from mazegenerator import MazeGenerator
from src.level.cell import Cell
from src.data import (PACMAN_COLOR, PAD, SUPERGUM_COLOR, MAZE_X, MAZE_Y,
                      LevelConfig, SUPERGUM_POINTS, GUM_POINTS, GameState, Dir)
from src.entities.entity import Enemy


class Level:
    def __init__(
            self,
            surface: pg.Surface,
            level_config: LevelConfig,
            level_id: int = 1,
            ) -> None:

        self.level_id = level_id
        self.seed = 42 if level_id == 1 else random.randint(1, 100)
        self.level_config = level_config
        self.maze = MazeGenerator(size=(MAZE_X, MAZE_Y), seed=self.seed)
        self._graph: dict[tuple[int, int], Cell] = self._build_graph()
        self.surface = surface
        self.player = self.level_config['player']
        self.paused = False
        self.playable_surface: pg.Surface
        self.layout: pg.Surface = self._build_layout()
        self.speed = self.level_config['data']['speed']
        self.total_collected = 0

    def _build_graph(self) -> dict[tuple[int, int], Cell]:
        max_gums = self.level_config['data']['max_gums']
        graph: dict[tuple[int, int], Cell] = {}
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[0])):
                graph[(j, i)] = Cell((j, i), self.maze.maze[i][j])
                if i == 0 and j == 0:
                    graph[(j, i)].sg = True
                elif i == len(self.maze.maze) - 1 and j == 0:
                    graph[(j, i)].sg = True
                elif i == 0 and j == len(self.maze.maze[0]) - 1:
                    graph[(j, i)].sg = True
                elif (i == len(self.maze.maze) - 1
                        and j == len(self.maze.maze[0]) - 1):
                    graph[(j, i)].sg = True
        counter = 0
        candidates = [
            c for c in graph.values()
            if c.sg is False and c.value != 15
            and (c.j, c.i) != (MAZE_Y // 2, MAZE_X // 2)
            ]
        while counter < max_gums:
            c = random.choice(candidates)
            candidates.remove(c)
            c.g = True
            counter += 1

        return graph

    def _build_layout(self) -> pg.Surface:
        screen_w = self.surface.get_width()
        screen_h = self.surface.get_height()
        edge = min(
            (screen_h - 2 * PAD) // len(self.maze.maze),
            (screen_w - 2 * PAD) // len(self.maze.maze[0])
        )
        surface_sizes = (edge * len(self.maze.maze[0]) + 1,
                         edge * len(self.maze.maze) + 1)
        self.edge = edge

        level_surface = pg.Surface(surface_sizes)
        level_surface.fill((15, 20, 25))

        for c in self._graph.values():
            c.rect = c.render(level_surface, edge)
            if c.sg:
                self.draw_super_gums(level_surface, (c.i, c.j))
            elif c.g:
                self.draw_gum(level_surface, (c.i, c.j))

        self.playable_surface = level_surface.copy()
        return level_surface

    def run(self) -> LevelConfig:
        self.player.set_rect(self._graph)
        for e in self.level_config['enemies']:
            e.set_rect(self._graph)
        clock = pg.time.Clock()
        self.surface.fill((15, 20, 25))

        while True:
            clock.tick(60)
            # import time
            # time.sleep(1.0)
            self.playable_surface = self.layout.copy()
            # if self.handle_events() == "menu":
            #     return self.level_config
            if self.paused:
                self.speed = 0
            else:
                self.speed = self.level_config['data']['speed']
            if self.level_config['game_state'] is GameState.WIN:
                return self.level_config

            self.handle_events()
            self.handle_movement()
            self.handle_collectibles()
            self.draw_pacman()
            for e in self.level_config['enemies']:
                self.draw_ghost(e)
            self.surface.blit(self.playable_surface, (PAD, PAD))
            pg.display.flip()

    def handle_collectibles(self) -> None:
        if self._graph[self.player.pos].sg:
            self._graph[self.player.pos].sg = False
            self.player.score += SUPERGUM_POINTS
            self.layout = self._build_layout()
            self.total_collected += 1
        if self._graph[self.player.pos].g:
            self._graph[self.player.pos].g = False
            self.player.score += GUM_POINTS
            self.layout = self._build_layout()
            self.total_collected += 1
        if self.total_collected == self.level_config['data']['max_gums'] + 4:
            self.level_config['game_state'] = GameState.WIN

    def handle_movement(self) -> None:

        if ((abs(self.player.rect.x - self._graph[self.player.pos].rect.x)
           >= self.edge
           or abs(self.player.rect.x - self._graph[self.player.target].rect.x)
           <= self.speed)
           and (abs(self.player.rect.y - self._graph[self.player.pos].rect.y)
           >= self.edge
           or abs(self.player.rect.y - self._graph[self.player.target].rect.y)
           <= self.speed)):


            # for e in self.level_config['enemies']:
            #     if e.strategy != "random":
            #         e.move(self._graph, self.player.pos)

            self.player.pos = self.player.target

            self.player.rect.x = self._graph[self.player.target].rect.x
            self.player.rect.y = self._graph[self.player.target].rect.y

            if self.player.moving['x_next'] == 1:
                if self._graph[self.player.pos].value & Dir.E == 0:
                    self.player.moving['x_now'] = 1
                    self.player.moving['y_now'] = 0
                    self.player.moving['x_next'] = 0
                    self.player.moving['y_next'] = 0
            if self.player.moving['x_next'] == -1:
                if self._graph[self.player.pos].value & Dir.W == 0:
                    self.player.moving['x_now'] = -1
                    self.player.moving['y_now'] = 0
                    self.player.moving['x_next'] = 0
                    self.player.moving['y_next'] = 0
            if self.player.moving['y_next'] == -1:
                if self._graph[self.player.pos].value & Dir.N == 0:
                    self.player.moving['x_now'] = 0
                    self.player.moving['y_now'] = -1
                    self.player.moving['x_next'] = 0
                    self.player.moving['y_next'] = 0
            if self.player.moving['y_next'] == 1:
                if self._graph[self.player.pos].value & Dir.S == 0:
                    self.player.moving['x_now'] = 0
                    self.player.moving['y_now'] = 1
                    self.player.moving['x_next'] = 0
                    self.player.moving['y_next'] = 0
            a, b = self.player.pos
            if self.player.moving['x_now'] == 1:
                if self._graph[self.player.pos].value & Dir.E == 0:
                    self.player.target = (a + 1, b)
                else:
                    self.player.target = self.player.pos
                    self.player.moving['x_now'] = 0

            if self.player.moving['x_now'] == -1:
                if self._graph[self.player.pos].value & Dir.W == 0:
                    self.player.target = (a - 1, b)
                else:
                    self.player.target = self.player.pos
                    self.player.moving['x_now'] = 0

            if self.player.moving['y_now'] == -1:
                if self._graph[self.player.pos].value & Dir.N == 0:
                    self.player.target = (a, b - 1)
                else:
                    self.player.target = self.player.pos
                    self.player.moving['y_now'] = 0

            if self.player.moving['y_now'] == 1:
                if self._graph[self.player.pos].value & Dir.S == 0:
                    self.player.target = (a, b + 1)
                else:
                    self.player.target = self.player.pos
                    self.player.moving['y_now'] = 0

        self.player.rect.x += self.player.moving['x_now'] * self.speed
        self.player.rect.y += self.player.moving['y_now'] * self.speed

        for e in self.level_config['enemies']:
            if ((abs(e.rect.x - self._graph[e.pos].rect.x)
                >= self.edge
                or abs(e.rect.x - self._graph[e.target].rect.x)
                <= self.speed)
                and (abs(e.rect.y - self._graph[e.pos].rect.y)
                >= self.edge
                or abs(e.rect.y - self._graph[e.target].rect.y)
                <= self.speed)):

                e.rect.x = self._graph[e.target].rect.x
                e.rect.y = self._graph[e.target].rect.y

                e.pos = e.target
                e.move(self._graph, self.player.pos)




        # for e in self.level_config['enemies']:

        for e in self.level_config['enemies']:
            e.rect.x += e.moving['x'] * self.speed
            e.rect.y += e.moving['y'] * self.speed


    def handle_events(self) -> None:
        """Handle keyboard and window events for the renderer."""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

                if event.key == pg.K_ESCAPE:
                    pass

                if event.key == pg.K_RIGHT:
                    self.paused = False
                    self.player.moving['x_next'] = 1
                    self.player.moving['y_next'] = 0

                if event.key == pg.K_LEFT:
                    self.paused = False
                    self.player.moving['x_next'] = -1
                    self.player.moving['y_next'] = 0

                if event.key == pg.K_UP:
                    self.paused = False
                    self.player.moving['x_next'] = 0
                    self.player.moving['y_next'] = -1

                if event.key == pg.K_DOWN:
                    self.paused = False
                    self.player.moving['x_next'] = 0
                    self.player.moving['y_next'] = 1

                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        return

    def draw_ghost(self, ghost: Enemy) -> None:
        pg.draw.circle(self.playable_surface, ghost.color, ghost.rect.center, 10)


    def draw_pacman(self) -> None:

        pg.draw.circle(self.playable_surface, PACMAN_COLOR,
                       self.player.rect.center,
                       15)
        # self.playable_surface.blit(surface, self.player.rect.center)

    def draw_super_gums(
            self,
            surface: pg.Surface,
            coord: tuple[int, int]
            ) -> None:

        pg.draw.circle(
            surface, SUPERGUM_COLOR,
            self._graph[(coord[0], coord[1])].rect.center,
            radius=10, width=4
        )

    def draw_gum(
            self,
            surface: pg.Surface,
            coord: tuple[int, int]
            # app: App
            ) -> None:

        pg.draw.circle(
            surface, SUPERGUM_COLOR,
            self._graph[(coord[0], coord[1])].rect.center,
            radius=5, width=1
        )
