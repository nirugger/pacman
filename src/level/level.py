from mazegenerator import MazeGenerator
from src.level.cell import Cell
from src.data import (PAD, GUM_COLOR, SUPERGUM_COLOR, MAZE_X, MAZE_Y,
                      LevelConfig, SUPERGUM_POINTS, GUM_POINTS, GameState,
                      SUPERGUM_TIME, LEVEL_TIME, GHOST_POINTS)

import pygame as pg
import time
import random
import sys


class Level:
    def __init__(
            self,
            surface: pg.Surface,
            level_config: LevelConfig,
            level_id: int = 1,
            ) -> None:

        self.surface = surface
        self.level_id = level_id
        self.seed = 42 if level_id == 1 else random.randint(1, 100)
        self.level_config = level_config
        self.player = self.level_config['player']
        self.speed = self.level_config['data']['speed']
        self.maze = MazeGenerator(size=(MAZE_X, MAZE_Y), seed=self.seed)
        self.graph: dict[tuple[int, int], Cell] = self._build_graph()
        self.layout: pg.Surface = self._build_layout()
        self.playable_surface: pg.Surface
        self.ghost_points = GHOST_POINTS

        self.paused = False
        self.total_collected = 0
        self.starting_time = time.time()
        self.last_supergum = 0

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

        for c in self.graph.values():
            c.rect = c.draw(level_surface, edge)
            c.center = pg.math.Vector2(c.rect.center)
            if c.sg:
                self.draw_super_gums(level_surface, (c.i, c.j))
            elif c.g:
                self.draw_gum(level_surface, (c.i, c.j))

        self.playable_surface = level_surface.copy()
        return level_surface

    def run(self) -> LevelConfig:
        # self.player.set_rect(self.graph)
        for e in self.level_config['entities']:
            e.set_rect(self.graph)
            e.center = pg.math.Vector2(e.rect.center)
            e.target_center = pg.math.Vector2(e.rect.center)
            e.home_center = pg.math.Vector2(e.rect.center)
        self._reset_positions()
        clock = pg.time.Clock()
        self.starting_time = time.time()
        self.surface.fill((15, 20, 25))
        # for e in self.level_config['entities']:
        #     if e is self.player:
        #         e.update_movement(self.graph)
        #     else:
        #         e.set_target_on_strategy(
        #             self.player.last_valid_pos, self.graph, self.player
        #         )
        #         e.update_movement(self.graph)


        while True:
            dt = clock.tick(60) / 1000
            self.playable_surface = self.layout.copy()
            if self.paused:
                self.speed = 0
            else:
                self.speed = self.level_config['data']['speed']
            if self.level_config['game_state'] is GameState.WIN:
                return self.level_config
            if self.level_config['game_state'] is GameState.LOSE:
                return self.level_config

            # if self._handle_events() == "menu":
            #     return self.level_config
            # print(self.player.center.x, self.player.center.y)
            self._handle_events()
            self._handle_time()
            # self._handle_movement()
            self._handle_vector_movement(dt)
            self._handle_collectibles()
            self._draw_frame()
            self._handle_collisions()

    def _handle_time(self) -> None:
        if time.time() - self.starting_time >= LEVEL_TIME:
            self.level_config['game_state'] = GameState.LOSE
        if time.time() - self.starting_time - self.last_supergum >= SUPERGUM_TIME:
            self.ghost_points = GHOST_POINTS
            for e in self.level_config['enemies']:
                e.frightened = False


    def _handle_collisions(self) -> None:

        for e in self.level_config['enemies']:
            if e.rect.collidepoint(self.player.rect.center) and e.going_home is False:
                if e.frightened:
                    e.going_home = True
                    e.frightened = False
                    self.player.score += self.ghost_points
                    self.ghost_points += GHOST_POINTS
                    # e.reset_positions(self.graph)
                else:
                    if self.player.cheat:
                        return


                    self.player.lives -= 1
                    if self.player.lives == 0:
                        self.level_config['game_state'] = GameState.LOSE
                    for ent in self.level_config['entities']:
                        ent.reset_positions(self.graph)

    def _handle_collectibles(self) -> None:
        if self.graph[self.player.pos].sg:
            self.graph[self.player.pos].sg = False
            self.player.score += SUPERGUM_POINTS
            self.layout = self._build_layout()
            self.last_supergum = time.time() - self.starting_time
            for e in self.level_config['enemies']:
                if e.going_home is False:
                    e.frightened = True
            self.total_collected += 1
        if self.graph[self.player.pos].g:
            self.graph[self.player.pos].g = False
            self.player.score += GUM_POINTS
            self.layout = self._build_layout()
            self.total_collected += 1
        if self.total_collected == self.level_config['data']['max_gums'] + 4:
            self.level_config['game_state'] = GameState.WIN

    def _handle_vector_movement(self, dt: float) -> None:

        for e in self.level_config['entities']:
            mov = self.graph[e.target].center - e.center
            dist = mov.length()
            if int(dist) == 0:
                e.pos = e.target
                e.center = self.graph[e.pos].center.copy()
                e.rect.center = (round(e.center.x), round(e.center.y))

                if e is self.player:
                    e.update_movement(self.graph)
                else:
                    e.set_target_on_strategy(
                        self.player.last_valid_pos, self.graph, self.player, self.level_config['enemies'][0].pos
                    )
                    e.update_movement(self.graph)
            else:
                movement = mov.normalize() * e.speed * dt
                e.center += movement * self.speed
                e.rect.center = (round(e.center.x), round(e.center.y))


    # def _handle_movement(self) -> None:

    #     now = (time.time_ns() - self.starting_time)
    #     for e in self.level_config['entities']:
    #         if ((abs(e.rect.x - self.graph[e.pos].rect.x) >= self.edge
    #            or abs(e.rect.x - self.graph[e.target].rect.x) <= self.speed)
    #            and (abs(e.rect.y - self.graph[e.pos].rect.y) >= self.edge
    #            or abs(e.rect.y - self.graph[e.target].rect.y) <= self.speed)):

    #             e.pos = e.target
    #             e.rect.x = self.graph[e.target].rect.x
    #             e.rect.y = self.graph[e.target].rect.y

    #             if e is self.player:
    #                 e.update_movement(self.graph)
    #             else:
    #                 e.set_target_on_strategy(
    #                     self.player.last_valid_pos, self.graph, self.player
    #                     )
    #                 e.update_movement(self.graph)

    #         module = (now - self.starting_time) >= (e.speed)
    #         if now - e.last_valid_module >= e.speed:
    #             e.last_valid_module = now
    #             # e.last_valid_module = module
    #             e.rect.x += e.movement['x'] * self.speed
    #             e.rect.y += e.movement['y'] * self.speed
    #     if now - self.starting_time >= 10000000:
    #         self.starting_time = now

    def _handle_events(self) -> None:
        """Handle keyboard and window events for the renderer."""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

                if event.key == pg.K_ESCAPE:
                    pass

                if event.key == pg.K_RIGHT:
                    self.paused = False
                    self.player.movement['nx'] = 1
                    self.player.movement['ny'] = 0

                if event.key == pg.K_LEFT:
                    self.paused = False
                    self.player.movement['nx'] = -1
                    self.player.movement['ny'] = 0

                if event.key == pg.K_UP:
                    self.paused = False
                    self.player.movement['nx'] = 0
                    self.player.movement['ny'] = -1

                if event.key == pg.K_DOWN:
                    self.paused = False
                    self.player.movement['nx'] = 0
                    self.player.movement['ny'] = 1

                if event.key == pg.K_c:
                    self.player.cheat = not self.player.cheat

                if event.key == pg.K_n and self.player.cheat:
                    self.level_config['game_state'] = GameState.WIN

                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        return

    def _reset_positions(self) -> None:
        self.player.reset_positions(self.graph)

        for e in self.level_config['enemies']:
            e.reset_positions(self.graph)

    def _draw_frame(self) -> None:
        for e in self.level_config['entities']:
            e.draw(self.playable_surface)

        self.surface.blit(self.playable_surface, (PAD, PAD))
        pg.display.flip()

    def draw_super_gums(
            self,
            surface: pg.Surface,
            coord: tuple[int, int]
            ) -> None:

        pg.draw.circle(
            surface, SUPERGUM_COLOR,
            self.graph[(coord[0], coord[1])].rect.center,
            radius=10, width=4
        )

    def draw_gum(
            self,
            surface: pg.Surface,
            coord: tuple[int, int]
            # app: App
            ) -> None:

        pg.draw.circle(
            surface, GUM_COLOR,
            self.graph[(coord[0], coord[1])].rect.center,
            radius=5,
        )
