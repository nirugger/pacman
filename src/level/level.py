
from mazegenerator import MazeGenerator
from src.level.cell import Cell
from src.entities.entity import Enemy, Red, Pink, Cyan, Orange
from src.data import (PAD, GUM_COLOR, SUPERGUM_COLOR, MAZE_X, MAZE_Y,
                      LevelConfig, SUPERGUM_POINTS, GUM_POINTS, GameState,
                      SUPERGUM_TIME, LEVEL_TIME, GHOST_POINTS, FRUIT_TIME,
                      FRUIT_POINTS, CELL_COLOR)

import pygame as pg
import random
import sys

SCATTER_RANGE = (10, 20)


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
        self.enemies = self._build_enemies()
        self.entities = [self.player] + self.enemies
        self.seconds = 0.0
        self.scatter = False
        self.max_time = self.level_config['data']['time']

        self.speed = 1
        self.maze = MazeGenerator(size=(MAZE_X, MAZE_Y), seed=self.seed)
        self.graph: dict[tuple[int, int], Cell] = self._build_graph()
        self.layout: pg.Surface = self._build_layout()
        self.playable_surface: pg.Surface
        self.ghost_points = GHOST_POINTS

        self.paused = False
        self.last_supergum = 0.0
        self.fruit_check = True
        self.last_fruit = 0.0
        self.total_collected = 0

        self.buttons: dict[str, pg.Rect] = {}

    def _build_enemies(self) -> list[Enemy]:
        e: list[Enemy] = []
        for color in ("red", "pink", "cyan", "orange"):
            enemy: Enemy
            match color:
                case "red":
                    enemy = Red(color, self.level_config['data']
                                ['strategies'][color])
                case "pink":
                    enemy = Pink(color, self.level_config['data']
                                 ['strategies'][color])
                case "cyan":
                    enemy = Cyan(color, self.level_config['data']
                                 ['strategies'][color])
                case "orange":
                    enemy = Orange(color, self.level_config['data']
                                   ['strategies'][color])
                case _:
                    raise ValueError("Unrecognised color")
            e.append(enemy)
        return e

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

        candidates = [
            c for c in graph.values()
            if c.sg is False and c.value != 15
            and (c.j, c.i) != (MAZE_Y // 2, MAZE_X // 2)
            ]
        for _ in range(max_gums):
            c = random.choice(candidates)
            candidates.remove(c)
            c.g = True

        screen_w = self.surface.get_width()
        screen_h = self.surface.get_height()
        edge = min(
            (screen_h - 2 * PAD) // len(self.maze.maze),
            (screen_w - 2 * PAD) // len(self.maze.maze[0])
        )
        self.edge = edge

        for c in graph.values():
            c.rect = pg.Rect(c.i * self.edge, c.j * self.edge,
                             self.edge, self.edge)
            c.center = pg.math.Vector2(c.rect.center)
        return graph

    def _build_layout(self) -> pg.Surface:

        surface_sizes = (self.edge * len(self.maze.maze[0]) + 1,
                         self.edge * len(self.maze.maze) + 1)
        level_surface = pg.Surface(surface_sizes)
        level_surface.fill((15, 20, 25))

        for c in self.graph.values():
            c.draw(level_surface, self.edge)
            if c.sg:
                self.draw_super_gums(level_surface, (c.i, c.j))
            elif c.g:
                self.draw_gum(level_surface, (c.i, c.j))
            elif c.fruit:
                self.draw_fruit(level_surface, (c.j, c.i))

        # self.playable_surface = level_surface.copy()
        return level_surface

    def setup_level(self) -> None:
        self.player.reset_positions(self.graph)
        for e in self.entities:
            e.set_rect(self.graph)
            e.center = pg.math.Vector2(e.rect.center)
            e.target_center = pg.math.Vector2(e.rect.center)
            e.home_center = pg.math.Vector2(e.rect.center)
        self.surface.fill((220, 220, 25))

    def run(self) -> LevelConfig:
        # self.player.set_rect(self.graph)
        self.setup_level()
        # self.starting_time = time.time()
        # for e in self.entities:
        #     if e is self.player:
        #         e.update_movement(self.graph)
        #     else:
        #         e.set_target_on_strategy(
        #             self.player.last_valid_pos, self.graph, self.player
        #         )
        #         e.update_movement(self.graph)

        clock = pg.time.Clock()
        while True:
            self.buttons.clear()
            dt = clock.tick(60) / 1000
            # if not self.paused:
            self.seconds += dt * self.speed
            self.playable_surface = self.layout.copy()
            if self.paused:
                self.speed = 0
            else:
                self.speed = 1
            if self.level_config['game_state'] is GameState.WIN:
                return self.level_config
            if self.level_config['game_state'] is GameState.LOSE:
                return self.level_config
            # if self._handle_events() == "menu":
            #     return self.level_config
            self._handle_time()
            self._handle_vector_movement(dt)
            self._handle_collectibles()
            self._draw_frame()
            self._handle_collisions()
            self._show_info()
            self._handle_events()

    def _handle_time(self) -> None:

        if self.seconds >= self.max_time:
            self.level_config['game_state'] = GameState.LOSE

        if self.seconds - self.last_supergum >= SUPERGUM_TIME:
            self.ghost_points = GHOST_POINTS
            for e in self.enemies:
                e.frightened = False

        if SCATTER_RANGE[0] <= int(self.seconds) <= SCATTER_RANGE[1]:
            self.scatter = True
        else:
            self.scatter = False

        if self.seconds - self.last_fruit >= FRUIT_TIME:
            self.graph[MAZE_X // 2, MAZE_Y // 2].fruit = False
            self.layout = self._build_layout()

    def _handle_collisions(self) -> None:
        for e in self.enemies:
            if (e.rect.collidepoint(self.player.rect.center)
                    and e.going_home is False):
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
                    for ent in self.entities:
                        ent.reset_positions(self.graph)

    def _handle_collectibles(self) -> None:
        if self.graph[self.player.pos].sg:
            self.graph[self.player.pos].sg = False
            self.player.score += SUPERGUM_POINTS
            self.layout = self._build_layout()
            self.last_supergum = self.seconds
            self.total_collected += 1
            self.fruit_check = True
            for e in self.enemies:
                if e.going_home is False:
                    e.frightened = True
        if self.graph[self.player.pos].g:
            self.graph[self.player.pos].g = False
            self.player.score += GUM_POINTS
            self.layout = self._build_layout()
            self.total_collected += 1
            self.fruit_check = True

        gums = self.level_config['data']['max_gums']
        if ((self.total_collected == gums * 3 // 10 or
                self.total_collected == gums * 7 // 10) and
                self.fruit_check):
            self.graph[(MAZE_X // 2, MAZE_Y // 2)].fruit = True
            self.layout = self._build_layout()
            self.last_fruit = self.seconds
            self.fruit_check = False

        if self.graph[self.player.pos].fruit:
            self.graph[self.player.pos].fruit = False
            self.player.score += FRUIT_POINTS
            self.layout = self._build_layout()
            self.fruit_check = False

        if self.total_collected == self.level_config['data']['max_gums'] + 4:
            self.level_config['game_state'] = GameState.WIN

    def _handle_vector_movement(self, dt: float) -> None:
        for e in self.entities:
            mov = self.graph[e.target].center - e.center
            dist = mov.length()
            if ((self.graph[e.pos].center - e.center).length()
                    >= (self.graph[e.pos].center - self.graph[e.target].center).length()):
                e.pos = e.target
                e.center = self.graph[e.pos].center.copy()
                e.rect.center = (round(e.center.x), round(e.center.y))

                if e is self.player:
                    e.update_movement(self.graph)
                else:
                    e.set_target_on_strategy(
                        self.player.last_valid_pos, self.graph,
                        self.player, self.enemies[0].pos, self.scatter
                    )
                    e.update_movement(self.graph)
            else:
                movement = mov.normalize() * e.speed * dt
                e.center += movement * self.speed
                e.rect.center = (round(e.center.x), round(e.center.y))

    # def _handle_movement(self) -> None:

    #     now = (time.time_ns() - self.starting_time)
    #     for e in self.entities:
    #         if ((abs(e.rect.x - self.graph[e.pos].rect.x) >= self.edge
    #            or abs(e.rect.x - self.graph[e.target].rect.x) <= self.speed)
    #            and (abs(e.rect.y - self.graph[e.pos].rect.y) >= self.edge
    #            or abs(e.rect.y - self.graph[e.target].rect.y) <=
    #  self.speed)):

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
                    if self.paused:
                        pass
                    else:
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

            if event.type == pg.MOUSEBUTTONDOWN:

                if ('continue' in self.buttons and self.buttons['continue'].
                        collidepoint(pg.mouse.get_pos())):
                    self.paused = False

                if ('exit' in self.buttons and self.buttons['exit'].
                        collidepoint(pg.mouse.get_pos())):
                    self.level_config['game_state'] = GameState.LOSE

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        return

    def _show_info(self) -> None:
        width = (self.surface.get_width() - self.playable_surface.get_width()
                 - 2 * PAD)
        height = self.playable_surface.get_height()
        info_surface = pg.Surface((width, height))
        info_surface.fill(CELL_COLOR)
        thickness = 5
        internal_rect = pg.Rect(thickness,
                                thickness,
                                width - 2 * thickness,
                                height - 2 * thickness)
        pg.draw.rect(info_surface, (15, 20, 25), internal_rect)
        font = pg.font.SysFont("arial", 32)
        for i in range(50, 200, 50):
            if i == 50:
                text = f"Time Left: {self.max_time - int(self.seconds)}"
            if i == 100:
                text = f"Lives: {self.player.lives}"
            if i == 150:
                text = f"Score: {self.player.score}"
            text_surface = font.render(text, True, "white")
            info_surface.blit(text_surface, (10, i))
            pg.display.flip()
        self.surface.blit(info_surface, (self.playable_surface.get_width()
                                         + PAD, PAD))

    def _draw_frame(self) -> None:
        for e in self.entities:
            e.draw(self.playable_surface)
        self.surface.blit(self.playable_surface, (PAD, PAD))

        if self.paused:
            self.pause_menu()

        pg.display.flip()

    def draw_fruit(
            self,
            surface: pg.Surface,
            coord: tuple[int, int]
            ) -> None:

        color = (random.randint(0, 255), random.randint(0, 255),
                 random.randint(0, 255))

        pg.draw.circle(
            surface, color,
            self.graph[(coord[0], coord[1])].rect.center,
            radius=8, width=6
        )

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

    def pause_menu(self) -> None:
        font = pg.font.SysFont('arial', 42)
        font_h = font.get_height()

        xy = self.playable_surface.get_size()
        surface = pg.surface.Surface(xy, pg.SRCALPHA)
        surface.fill((15, 20, 25, 200))

        text_surface = font.render("CONTINUE", True, 'white')
        self.buttons['continue'] = surface.blit(text_surface,
                                                (surface.get_width() // 2
                                                 - text_surface.get_width()
                                                 // 2, surface.get_height() //
                                                 2 - font_h))
        self.buttons['continue'].x += PAD
        self.buttons['continue'].y += PAD

        text_surface = font.render("EXIT", True, 'white')
        self.buttons['exit'] = surface.blit(text_surface,
                                            (surface.get_width() // 2 -
                                             text_surface.get_width() // 2,
                                             surface.get_height() // 2 +
                                             font_h))
        self.buttons['exit'].x += PAD
        self.buttons['exit'].y += PAD

        self.surface.blit(surface, (PAD, PAD))
