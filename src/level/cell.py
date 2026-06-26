import pygame as pg
from src.data import Dir, EDGE_THICK, CELL_COLOR


class Cell:

    def __init__(self, pos: tuple[int, int], value: int) -> None:
        self.i = pos[0]
        self.j = pos[1]
        self.value = value
        self.rect: pg.Rect

        self.center: pg.math.Vector2

        self.sg = False
        self.g = False
        self.fruit = False

    def draw(
            self,
            surface: pg.Surface,
            edge: int,
            color: tuple[int, int, int]
            ) -> pg.Rect:

        x, y = self.i * edge, self.j * edge

        if self.value & Dir.N:
            pg.draw.line(surface, color,
                         (x, y), (x + edge, y), width=EDGE_THICK)
        if self.value & Dir.E:
            pg.draw.line(surface, color,
                         (x + edge, y), (x + edge, y + edge), width=EDGE_THICK)
        if self.value & Dir.S:
            pg.draw.line(surface, color,
                         (x, y + edge), (x + edge, y + edge), width=EDGE_THICK)
        if self.value & Dir.W:
            pg.draw.line(surface, color,
                         (x, y), (x, y + edge), width=EDGE_THICK)

        return pg.Rect(x, y, edge, edge)
