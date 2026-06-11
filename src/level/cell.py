import pygame as pg
from enum import IntFlag
from src.data import CELL_COLOR


class Dir(IntFlag):
    N = 1
    E = 2
    S = 4
    W = 8


class Cell:

    def __init__(self, pos: tuple[int, int], value: int) -> None:
        self.i = pos[1]
        self.j = pos[0]
        self.value = value
        self.rect: pg.Rect

    def render(
            self,
            surface: pg.Surface,
            edge: int
            ) -> pg.Rect:

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
