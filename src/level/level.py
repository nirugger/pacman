from enum import IntFlag
import pygame as pg
import sys

import random

from mazegenerator import MazeGenerator
from src.level.cell import Cell
from src.data import (PACMAN_COLOR, PAD, SUPERGUM_COLOR, MAZE_X, MAZE_Y,
                      LevelConfig, SUPERGUM_POINTS, GUM_POINTS)


class Dir(IntFlag):
    N = 1
    E = 2
    S = 4
    W = 8




class Level:
    def __init__(
            self,
            surface: pg.Surface,
            level_config: LevelConfig,
            level_id: int = 1,
            seed: int = 42,
            ) -> None:

        self.level_id = level_id
        self.maze = MazeGenerator(size=(MAZE_X, MAZE_Y), seed=seed)
        self._graph: dict[tuple[int, int], Cell] = self._build_graph()
        self.surface = surface
        self.level_config = level_config
        self.player = self.level_config['player']
        self.paused = False
        self.playable_surface: pg.Surface
        self.layout: pg.Surface = self._build_layout()
        self.speed = self.level_config['speed']

    def _build_graph(self) -> dict[tuple[int, int], Cell]:
        max_gums = 50
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
        candidates = [c for c in graph.values() if c.sg is False and c.value != 15 and (c.j, c.i) != (MAZE_Y // 2, MAZE_X // 2)]
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
        clock = pg.time.Clock()
        self.surface.fill((15, 20, 25))

        while True:
            dt = clock.tick(60)
            self.playable_surface = self.layout.copy()
            # if self.handle_events() == "menu":
            #     return self.level_config
            if self.paused:
                self.speed = 0
            else:
                self.speed = self.level_config['speed']
            self.handle_events(dt)
            self.handle_movement(dt)
            self.handle_collectibles()
            self.draw_pacman()
            self.surface.blit(self.playable_surface, (PAD, PAD))
            pg.display.flip()

    def handle_collectibles(self) -> None:
        if self._graph[self.player.pos].sg:
            self._graph[self.player.pos].sg = False
            self.player.score += SUPERGUM_POINTS
            self.layout = self._build_layout()
        if self._graph[self.player.pos].g:
            self._graph[self.player.pos].g = False
            self.player.score += GUM_POINTS
            self.layout = self._build_layout()

    def handle_movement(self, dt: int) -> None:
        # print(self.player.rect.center)
        # print(self._graph[self.player.target].rect.center)
        # print()

        # if (abs(self.player.rect.center[1] -
        #     self._graph[self.player.target].rect.center[1])
        #     < self.speed and
        #         abs(self.player.rect.center[0] -
        #     self._graph[self.player.target].rect.center[0])
        #     < self.self.speeself.d):

        if ((abs(self.player.rect.x - self._graph[self.player.pos].rect.x)
           >= self.edge
           or abs(self.player.rect.x - self._graph[self.player.pos].rect.x)
           == 0)
           and (abs(self.player.rect.y - self._graph[self.player.pos].rect.y)
           >= self.edge
           or abs(self.player.rect.y - self._graph[self.player.pos].rect.y)
           == 0)):

            self.player.rect.x = self._graph[self.player.target].rect.x
            self.player.rect.y = self._graph[self.player.target].rect.y

            self.player.pos = self.player.target
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
        # print(self.player.rect.center)
        # print(self._graph[self.player.target].rect.center)
        # print(self.edge)

        self.player.rect.y += self.player.moving['y_now'] * self.speed
        self.player.rect.x += self.player.moving['x_now'] * self.speed

    def handle_events(self, dt: int) -> None:
        """Handle keyboard and window events for the renderer."""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

                if event.key == pg.K_ESCAPE:
                    pass
                    # self.app.menu.pause_menu(self.app)

                if event.key == pg.K_RIGHT:
                    self.player.moving['x_next'] = 1
                    self.player.moving['y_next'] = 0

                    # if self._graph[self.player.pos].value & Dir.E == 0:
                    #     self.player.rect.x += self.edge // 1
                    #     self.player.pos = (
                    #         self.player.pos[0] + 1,
                    #         self.player.pos[1]
                    #     )

                    pass

                if event.key == pg.K_LEFT:
                    self.player.moving['x_next'] = -1
                    self.player.moving['y_next'] = 0

                    # if self._graph[self.player.pos].value & Dir.W == 0:
                    #     self.player.rect.x -= self.edge
                    #     self.player.pos = (self.player.pos[0] - 1, self.player.pos[1])
                    # pass

                if event.key == pg.K_UP:
                    self.player.moving['x_next'] = 0
                    self.player.moving['y_next'] = -1

                    # if self._graph[self.player.pos].value & Dir.N == 0:
                    #     self.player.rect.y -= self.edge
                    #     self.player.pos = (self.player.pos[0], self.player.pos[1] - 1)
                    # pass

                if event.key == pg.K_DOWN:
                    self.player.moving['x_next'] = 0
                    self.player.moving['y_next'] = 1
                    #
                    # if self._graph[self.player.pos].value & Dir.S == 0:
                    #     self.player.rect.y += self.edge
                    #     self.player.pos = (self.player.pos[0], self.player.pos[1] + 1)
                    # pass

                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        return

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