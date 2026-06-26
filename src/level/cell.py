import pygame as pg
from src.data import Dir, EDGE_THICK


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

        x, y = self.i * edge + EDGE_THICK, self.j * edge + EDGE_THICK

        if self.value & Dir.N:
            pg.draw.line(surface, color,
                         (x - EDGE_THICK, y - EDGE_THICK),
                         (x + edge, y - EDGE_THICK),
                         width=EDGE_THICK)
        if self.value & Dir.E:
            pg.draw.line(surface, color,
                         (x + edge, y - EDGE_THICK),
                         (x + edge, y + edge),
                         width=EDGE_THICK)
        if self.value & Dir.S:
            pg.draw.line(surface, color,
                         (x - EDGE_THICK, y + edge),
                         (x + edge, y + edge),
                         width=EDGE_THICK)
        if self.value & Dir.W:
            pg.draw.line(surface, color,
                         (x - EDGE_THICK, y - EDGE_THICK),
                         (x - EDGE_THICK, y + edge),
                         width=EDGE_THICK)

        return pg.Rect(x, y, edge, edge)
