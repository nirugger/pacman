"""Module defining the Cell class for representing a cell in the maze."""

import pygame as pg
from src.data import Dir, EDGE_THICK, dc_draw_line


class Cell:
    """Class representing a cell in the maze."""

    def __init__(self, pos: tuple[int, int], value: int) -> None:
        """Initialize a cell with its position and value.

        Args:
            pos (tuple[int, int]): The (i, j) position of the cell in the grid.
            value (int): The value representing the walls of the cell.
        """
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
        """Draw the cell on the given surface.

        Args:
            surface (pg.Surface): The surface to draw the cell on.
            edge (int): The length of the edge of the cell.
            color (tuple[int, int, int]): The color of the walls of the cell.

        Returns:
            pg.Rect: The rectangle representing the cell's position and size.
        """
        x, y = self.i * edge + EDGE_THICK, self.j * edge + EDGE_THICK

        if self.value & Dir.N:
            dc_draw_line(x - EDGE_THICK, y - EDGE_THICK,
                         x + edge, y - EDGE_THICK,
                         surface, color)
        if self.value & Dir.E:
            dc_draw_line(x + edge, y - EDGE_THICK,
                         x + edge, y + edge,
                         surface, color)
        if self.value & Dir.S:
            dc_draw_line(x - EDGE_THICK, y + edge,
                         x + edge, y + edge,
                         surface, color)
        if self.value & Dir.W:
            dc_draw_line(x - EDGE_THICK, y - EDGE_THICK,
                         x - EDGE_THICK, y + edge,
                         surface, color)

        # if self.value == 15:
        #     pg.draw.rect(surface, color, self.rect, width=edge // 3)

        return pg.Rect(x, y, edge, edge)
