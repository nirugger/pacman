
from mazegenerator import MazeGenerator
from src.level.cell import Cell
from src.entities.entity import Enemy, Red, Pink, Cyan, Orange
from src.data import (PAD, GUM_COLOR, SUPERGUM_COLOR, MAZE_X, MAZE_Y,
                      LevelConfig, SUPERGUM_POINTS, GUM_POINTS, GameState,
                      SUPERGUM_TIME, EDGE_THICK, GHOST_POINTS, FRUIT_TIME,
                      FRUIT_POINTS, CELL_COLOR, FONT)

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
        self.seed = (level_config['seed']
                     if level_id == 1
                     else random.randint(1, 100))
        self.level_config = level_config
        self.player = self.level_config['player']
        self.enemies = self._build_enemies()
        self.entities = [self.player] + self.enemies
        self.seconds = 0.0
        self.scatter = False
        self.max_time = self.level_config['data']['time']

        self.maze = MazeGenerator(size=(MAZE_X, MAZE_Y), seed=self.seed)
        self.graph: dict[tuple[int, int], Cell] = self._build_graph()
        self.layout: pg.Surface = self._build_layout()
        self.playable_surface: pg.Surface
        self.ghost_points = GHOST_POINTS

        self.new_game = True
        self.paused = False
        self.last_supergum = 0.0
        self.fruit_check = True
        self.last_fruit = 0.0
        self.total_collected = 0
        self.setup_level()

        self.buttons: dict[str, pg.Rect] = {}

    def _build_enemies(self) -> list[Enemy]:
        e: list[Enemy] = []
        for color in ("red", "pink", "cyan", "orange"):
            enemy: Enemy
            match color:
                case "red":
                    enemy = Red(self.level_config['data']['palette']['blinky'],
                                self.level_config['data']['strategies'][color])
                case "pink":
                    enemy = Pink(self.level_config['data']['palette']['pinky'],
                                 self.level_config['data']['strategies'][color])
                case "cyan":
                    enemy = Cyan(self.level_config['data']['palette']['inky'],
                                 self.level_config['data']['strategies'][color])
                case "orange":
                    enemy = Orange(self.level_config['data']['palette']['clyde'],
                                   self.level_config['data']['strategies'][color])
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
        surface_sizes = (self.edge * len(self.maze.maze[0]) + EDGE_THICK,
                         self.edge * len(self.maze.maze) + EDGE_THICK)
        level_surface = pg.Surface(surface_sizes)
        level_surface.fill(self.level_config['data']['palette']['bg'])

        color = self.level_config['data']['palette']['walls']
        for c in self.graph.values():
            c.draw(level_surface, self.edge, color)
            if c.sg:
                self.draw_super_gums(level_surface, (c.i, c.j))
            elif c.g:
                self.draw_gum(level_surface, (c.i, c.j))
            elif c.fruit:
                self.draw_fruit(level_surface, (c.i, c.j))
        return level_surface

    def setup_level(self) -> None:
        self.player.reset_positions(self.graph)
        self.player.color = self.level_config['data']['palette']['pacman']
        for e in self.entities:
            e.set_rect(self.graph)
            e.center = pg.math.Vector2(e.rect.center)
            e.target_center = pg.math.Vector2(e.rect.center)
            e.home_center = pg.math.Vector2(e.rect.center)
        # self.surface.fill((220, 220, 25))
        self.playable_surface = self.layout.copy()

    def run(self) -> LevelConfig:
        # self.surface.fill((220, 220, 25))
        self._draw_frame()
        clock = pg.time.Clock()
        while True:
            self.buttons.clear()
            dt = self._handle_time(clock)
            if self.level_config['game_state'] is GameState.WIN:
                self.level_config['time'] = self.seconds
                return self.level_config
            elif self.level_config['game_state'] is GameState.LOSE:
                self.level_config['time'] = self.seconds
                return self.level_config
            elif self.level_config['game_state'] is GameState.MAIN_MENU:
                self.level_config['time'] = self.seconds
                return self.level_config
            self._handle_vector_movement(dt)
            self._handle_collectibles()
            self._draw_frame()
            self._handle_collisions()
            self._handle_events()

    def _handle_time(self, clock: pg.time.Clock) -> float:

        dt = clock.tick(60) / 1000
        self.seconds += dt * (not self.paused)

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

        return dt

    def _handle_collisions(self) -> None:
        for e in self.enemies:
            if (e.rect.collidepoint(self.player.rect.center)
                    and e.going_home is False):
                if e.frightened:
                    e.going_home = True
                    e.frightened = False
                    self.player.score += self.ghost_points
                    self.ghost_points += GHOST_POINTS
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
        self.playable_surface = self.layout.copy()
        for e in self.entities:
            to_move = self.graph[e.target].center - e.center
            covered = self.graph[e.pos].center - e.center
            to_cover = self.graph[e.pos].center - self.graph[e.target].center
            if covered.length() >= to_cover.length() - 1:
                e.pos = e.target
                e.center = self.graph[e.pos].center.copy()
                e.rect.center = (round(e.center.x), round(e.center.y))

                e.set_target_on_strategy(
                    self.player.last_valid_pos, self.graph,
                    self.player, self.enemies[0].pos, self.scatter
                )
                e.update_movement(self.graph)
            else:
                movement = to_move.normalize() * e.speed * dt
                e.center += movement * (not self.paused)
                e.rect.center = (round(e.center.x), round(e.center.y))

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
                    self.player.has_been_cheating = True
                    self.player.cheat = not self.player.cheat

                if event.key == pg.K_n and self.player.cheat:
                    self.level_config['game_state'] = GameState.WIN

                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:

                if ('continue' in self.buttons and
                        self.buttons['continue'].
                        collidepoint(pg.mouse.get_pos())):
                    self.paused = False

                if ('back_to_menu' in self.buttons and
                        self.buttons['back_to_menu'].
                        collidepoint(pg.mouse.get_pos())):
                    self.level_config['game_state'] = GameState.MAIN_MENU

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        return

    def _show_info(self) -> None:
        width = (self.surface.get_width() - self.playable_surface.get_width()
                 - 2 * PAD)
        height = self.playable_surface.get_height()
        info_surface = pg.Surface((width, height))
        info_surface.fill(self.level_config['data']['palette']['walls'])
        thickness = EDGE_THICK
        internal_rect = pg.Rect(thickness,
                                thickness,
                                width - 2 * thickness,
                                height - 2 * thickness)
        pg.draw.rect(info_surface, self.level_config['data']['palette']['bg'], internal_rect)
        # font = pg.font.SysFont("arial", 32)
        font = pg.font.Font(FONT, 32)
        s = "S" if self.max_time - int(self.seconds) != 1 else ""
        f"YOU MAY DIE IN {self.max_time - int(self.seconds)} SECOND{s}"
        lives = (f"YOU MAY DIE {self.player.lives} MORE TIMES"
                 if self.player.lives > 1 else "LAST LIFE, MAKE IT COUNT")
        f"{lives}"
        f"YOUR SCORE IS WORTH {self.player.score} POINTS"
        "KEYS:"
        "RUN TIME:"
        "PACGUM "
        "GHOST KILLED:"
        for i in range(50, 200, 50):
            if i == 50:
                text = f"TIME: {self.max_time - int(self.seconds)}"
            if i == 100:
                text = f": {self.player.lives}"
            if i == 150:
                text = f"Score: {self.player.score}"
            text_surface = font.render(text, True, "white")
            info_surface.blit(text_surface, (10, i))
        self.surface.blit(info_surface, (self.playable_surface.get_width()
                                         + PAD, PAD))

    def _draw_frame(self) -> None:
        for e in self.entities:
            if e is self.player:
                print(e.color)
            e.draw(self.playable_surface)
        self._show_info()
        self.surface.blit(self.playable_surface, (PAD, PAD))

        if self.paused:
            self.pause_menu()

        pg.display.flip()

    def draw_fruit(
            self,
            surface: pg.Surface,
            coord: tuple[int, int]
            ) -> None:

        color = self.level_config['data']['palette']['fruit']

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

        color = self.level_config['data']['palette']['spg']
        pg.draw.circle(
            surface, color,
            self.graph[(coord[0], coord[1])].rect.center,
            radius=7, width=5
        )

    def draw_gum(
            self,
            surface: pg.Surface,
            coord: tuple[int, int]
            # app: App
            ) -> None:

        color = self.level_config['data']['palette']['pg']
        pg.draw.circle(
            surface, color,
            self.graph[(coord[0], coord[1])].rect.center,
            radius=3,
        )

    def pause_menu(self) -> None:
        font = pg.font.Font(FONT, 42)
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

        text_surface = font.render("BACK TO MENU", True, 'white')
        self.buttons['back_to_menu'] = surface.blit(
            text_surface,
            (surface.get_width() // 2 - text_surface.get_width() // 2,
             surface.get_height() // 2 + font_h))
        self.buttons['back_to_menu'].x += PAD
        self.buttons['back_to_menu'].y += PAD

        self.surface.blit(surface, (PAD, PAD))
