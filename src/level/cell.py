import pygame as pg
from enum import IntFlag


class Dir(IntFlag):
    N = 1
    E = 2
    S = 4
    W = 8


class Cell:

    def __init__(self, pos: tuple[int, int], value: int) -> None:
        self.i = pos[0]
        self.j = pos[1]
        self.value = value
        self.rect: pg.Rect
        self.sg = False
        self.g = False

    def render(
            self,
            surface: pg.Surface,
            edge: int
            ) -> pg.Rect:
        from src.data import CELL_COLOR

        x, y = self.i * edge, self.j * edge

        if self.value & Dir.N:
            pg.draw.line(surface, CELL_COLOR,
                         (x, y), (x + edge, y))
        if self.value & Dir.E:
            pg.draw.line(surface, CELL_COLOR,
                         (x + edge, y), (x + edge, y + edge))
        if self.value & Dir.S:
            pg.draw.line(surface, CELL_COLOR,
                         (x, y + edge), (x + edge, y + edge))
        if self.value & Dir.W:
            pg.draw.line(surface, CELL_COLOR,
                         (x, y), (x, y + edge))

        return pg.Rect(x, y, edge, edge)
