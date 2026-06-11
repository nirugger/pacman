
from enum import IntFlag
import pygame as pg
import sys
from mazegenerator import MazeGenerator
from src.level.cell import Cell
from src.data import PACMAN_COLOR, PAD, SUPERGUM_COLOR, MAZE_X, MAZE_Y, LevelConfig, SUPERGUM_POINTS


class Dir(IntFlag):
    N = 1
    E = 2
    S = 4
    W = 8



def draw_gum(
        surface: pg.Surface,
        graph: dict[tuple[int, int], pg.Rect],
        # app: App
        ) -> None:
    pass


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
        self.paused = False
        self.playable_surface: pg.Surface
        self.layout: pg.Surface = self._build_layout()
        self.pause = False

    def _build_graph(self) -> dict[tuple[int, int], Cell]:
        graph: dict[tuple[int, int], Cell] = {}
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[0])):
                graph[(j, i)] = Cell((j, i), self.maze.maze[i][j])
                if i == 0 and j == 0:
                    graph[(j, i)].sg = True
                if i == len(self.maze.maze) - 1 and j == 0:
                    graph[(j, i)].sg = True
                if i == 0 and j == len(self.maze.maze[0]) - 1:
                    graph[(j, i)].sg = True
                if i == len(self.maze.maze) - 1 and j == len(self.maze.maze[0]) - 1:
                    graph[(j, i)].sg = True
        return graph

    def _build_layout(self) -> pg.Surface:
        screen_w = self.surface.get_width()
        screen_h = self.surface.get_height()
        edge = min(
            (screen_h - 2 * PAD) // len(self.maze.maze),
            (screen_w - 2 * PAD) // len(self.maze.maze[0])
        )
        surface_sizes = (edge * len(self.maze.maze[0]) + 1, edge * len(self.maze.maze) + 1)
        self.edge = edge

        level_surface = pg.Surface(surface_sizes)
        level_surface.fill((15, 20, 25))

        for c in self._graph.values():
            c.rect = c.render(level_surface, edge)
            if c.sg is True:
                self.draw_super_gums(level_surface, (c.i, c.j))

        self.playable_surface = level_surface.copy()
        return level_surface

    def draw_pacman(self) -> None:
        # surface = pg.Surface(self.level_config['player'].rect.topleft)
        pg.draw.circle(self.playable_surface, PACMAN_COLOR,
                       self.level_config['player'].rect.center,
                       15)
        # self.layout.blit(surface, self.level_config['player'].rect.center)


    def draw_super_gums(self, surface: pg.Surface, coord: tuple[int, int]) -> None:
        pg.draw.circle(
            surface, SUPERGUM_COLOR,
            self._graph[(coord[0], coord[1])].rect.center,
            radius=10, width=4
        )

    def run(self) -> LevelConfig:
        self.level_config['player'].set_rect(self._graph)
        clock = pg.time.Clock()

        self.surface.fill((15, 20, 25))
        while True:
            dt = clock.tick(60)

            # if self.handle_events() == "menu":
            #     return self.level_config
            self.handle_events()
            self.handle_collectibles()
            self.playable_surface.fill((15, 20, 25))
            self._build_layout()
            self.draw_pacman()
            # self.draw_super_gums()
            self.surface.blit(self.playable_surface, (PAD, PAD))
            # self.surface.blit(self.layout, (PAD, PAD))
            pg.display.flip()


    def handle_collectibles(self) -> None:

        if self._graph[(self.level_config['player'].pos[0],
                        self.level_config['player'].pos[1])].sg:
            self._graph[(self.level_config['player'].pos[0],
                         self.level_config['player'].pos[1])].sg = False
            self.level_config['player'].score += SUPERGUM_POINTS


    def handle_events(self) -> None:
        """Handle keyboard and window events for the renderer."""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

                if event.key == pg.K_ESCAPE:
                    pass
                    # self.app.menu.pause_menu(self.app)

                if event.key == pg.K_RIGHT:
                    # self.level_config['player'].moving['x_next'] = 'r'
                    if self._graph[(self.level_config['player'].pos[0], self.level_config['player'].pos[1])].value & Dir.E == 0:
                        self.level_config['player'].rect.x += self.edge
                        self.level_config['player'].pos[0] += 1

                    pass

                if event.key == pg.K_LEFT:
                    if self._graph[(self.level_config['player'].pos[0], self.level_config['player'].pos[1])].value & Dir.W == 0:
                        self.level_config['player'].rect.x -= self.edge
                        self.level_config['player'].pos[0] -= 1
                    pass

                if event.key == pg.K_UP:
                    if self._graph[(self.level_config['player'].pos[0], self.level_config['player'].pos[1])].value & Dir.N == 0:
                        self.level_config['player'].rect.y -= self.edge
                        self.level_config['player'].pos[1] -= 1
                    pass

                if event.key == pg.K_DOWN:
                    if self._graph[(self.level_config['player'].pos[0], self.level_config['player'].pos[1])].value & Dir.S == 0:
                        self.level_config['player'].rect.y += self.edge
                        self.level_config['player'].pos[1] += 1
                    pass

                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        return
