
from enum import IntFlag
import pygame as pg
import sys
from mazegenerator import MazeGenerator
from src.level.cell import Cell
from src.data import PACMAN_COLOR, PAD, SUPERGUM_COLOR


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
            level_config: dict,
            level_id: int = 1,
            seed: int = 42,
            ) -> None:

        self.level_id = level_id
        self.maze = MazeGenerator(size=(21, 21), seed=seed)
        self._graph: dict[tuple[int, int], Cell] = self._build_graph()
        self.surface = surface
        self.level_config = level_config
        self.paused = False
        self.layout: pg.Surface = self.build_layout()

    def _build_graph(self) -> dict[tuple[int, int], Cell]:
        graph: dict[tuple[int, int], Cell] = {}
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[0])):
                graph[(i, j)] = Cell((i, j), self.maze.maze[i][j])
        return graph

    def build_layout(self) -> pg.Surface:
        screen_w = self.surface.get_width()
        screen_h = self.surface.get_height()
        edge = min(
            (screen_h - 2 * PAD) // len(self.maze.maze),
            (screen_w - 2 * PAD) // len(self.maze.maze[0])
        )
        surface_sizes = (edge * len(self.maze.maze) + 1, edge * len(self.maze.maze[0]) + 1)

        level_surface = pg.Surface(surface_sizes)
        level_surface.fill((15, 20, 25))

        for c in self._graph.values():
            c.rect = c.render(level_surface, edge)

        return level_surface

    # def draw_pacman(self) -> None:
    #     pg.draw.circle(self.layout, PACMAN_COLOR,
    #                    self.level_config['player'].get_player_position(self._graph),
    #                    15)

    def draw_super_gums(self) -> None:

        for item in self.level_config['super_gums']:
            pg.draw.circle(
                self.layout, SUPERGUM_COLOR,
                self._graph[(item.pos[0], item.pos[1])].rect.center,
                radius=10, width=4
            )

    def run(self) -> dict:
        clock = pg.time.Clock()
        while True:
            dt = clock.tick(60)

            if self.handle_events() == "menu":
                return self.level_config

            self.surface.fill((15, 20, 25))
            self.surface.blit(self.layout, (PAD, PAD))
            self.draw_super_gums()
            # self.draw_pacman(self.app.screen, self.app)
            pg.display.flip()

    def handle_events(self) -> str | None:
        """Handle keyboard and window events for the renderer."""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

                if event.key == pg.K_ESCAPE:
                    pass
                    # self.app.menu.pause_menu(self.app)

                if event.key == pg.K_RIGHT:
                    pass

                if event.key == pg.K_LEFT:
                    pass

                if event.key == pg.K_UP:
                    pass

                if event.key == pg.K_DOWN:
                    pass

                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
