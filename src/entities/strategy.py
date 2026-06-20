from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.entity import Player
from src.data import MAZE_X, MAZE_Y, Dir
from src.level.cell import Cell

from abc import ABC
from collections import deque
import random


class Strategy(ABC):

    @staticmethod
    def follow(
        start: tuple[int, int],
        end: tuple[int, int],
        graph: dict[tuple[int, int], Cell]
         ) -> tuple[int, int]:

        start_x, start_y = start
        end_x, end_y = end
        shortest_path = ''

        directions = [(0, 1, 4, 'S'), (1, 0, 2, 'E'),
                      (-1, 0, 8, 'W'), (0, -1, 1, 'N')]

        if (start_x, start_y) == (end_x, end_y):
            return (start_x, start_y)

        visited = [[False] * MAZE_X for _ in range(MAZE_Y)]
        visited[start_y][start_x] = True
        queue: deque[tuple[int, int, str]] = deque(
            [(start_x, start_y, '')])
        while queue:
            x, y, ways = queue.popleft()
            for dx, dy, code, way in directions:
                if (graph[(x, y)].value & code) != 0:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < MAZE_X and 0 <= ny < MAZE_Y):
                    continue
                if visited[ny][nx]:
                    continue
                if (nx, ny) == (end_x, end_y):
                    shortest_path = ways + way

                    if shortest_path[0] == 'N':
                        return (start_x, start_y - 1)
                    if shortest_path[0] == 'S':
                        return (start_x, start_y + 1)
                    if shortest_path[0] == 'E':
                        return (start_x + 1, start_y)
                    if shortest_path[0] == 'W':
                        return (start_x - 1, start_y)

                visited[ny][nx] = True
                queue.append((nx, ny, ways + way))
        raise ValueError("FOTTITI")

    @staticmethod
    def random(
        start: tuple[int, int],
        graph: dict[tuple[int, int], Cell]
         ) -> tuple[int, int]:

        x, y = start
        directions = ['N', 'S', 'E', 'W']
        random.shuffle(directions)
        for d in directions:
            match d:
                case 'N':
                    if graph[x, y].value & Dir.N == 0:
                        return (x, y - 1)
                case 'S':
                    if graph[x, y].value & Dir.S == 0:
                        return (x, y + 1)
                case 'E':
                    if graph[x, y].value & Dir.E == 0:
                        return (x + 1, y)
                case 'W':
                    if graph[x, y].value & Dir.W == 0:
                        return (x - 1, y)
        raise ValueError("CAZZO!")

    @staticmethod
    def anticipate(start: tuple[int, int], graph: dict[tuple[int, int], Cell],
                   player: Player) -> tuple[int, int]:
        target = player.last_valid_pos
        player_x, player_y = player.last_valid_pos
        if player.movement['x'] == 1:
            if player_x + 4 < MAZE_X:
                if graph[(player_x + 4, player_y)].value != 15:
                    target = (player_x + 4, player_y)
            else:
                if player.movement['nx'] == 1:
                    if player_x + 4 < MAZE_X:
                        if graph[(player_x + 4,
                                  player_y)].value != 15:
                            target = (player_x + 4, player_y)
                if player.movement['nx'] == -1:
                    if player_x - 4 >= 0:
                        if graph[(player_x - 4,
                                  player_y)].value != 15:
                            target = (player_x - 4, player_y)
                if player.movement['ny'] == -1:
                    if player_y - 4 >= 0:
                        if graph[(player_x,
                                  player_y - 4)].value != 15:
                            target = (player_x, player_y - 4)
                    if player.movement['ny'] == 1:
                        if player_y + 4 >= 0:
                            if graph[(player_x,
                                      player_y + 4)].value != 15:
                                target = (player_x, player_y + 4)
        if player.movement['x'] == -1:
            if player_x - 4 >= 0:
                if graph[(player_x - 4, player_y)].value != 15:
                    target = (player_x - 4, player_y)
            else:
                if player.movement['nx'] == 1:
                    if player_x + 4 < MAZE_X:
                        if graph[(player_x + 4,
                                  player_y)].value != 15:
                            target = (player_x + 4, player_y)
                if player.movement['nx'] == -1:
                    if player_x - 4 >= 0:
                        if graph[(player_x - 4,
                                  player_y)].value != 15:
                            target = (player_x - 4, player_y)
                if player.movement['ny'] == -1:
                    if player_y - 4 >= 0:
                        if graph[(player_x,
                                  player_y - 4)].value != 15:
                            target = (player_x, player_y - 4)
                    if player.movement['ny'] == 1:
                        if player_y + 4 >= 0:
                            if graph[(player_x,
                                      player_y + 4)].value != 15:
                                target = (player_x, player_y + 4)
        if player.movement['y'] == 1:
            if player_y + 4 < MAZE_Y:
                if graph[(player_x, player_y + 4)].value != 15:
                    target = (player_x, player_y + 4)
            else:
                if player.movement['nx'] == 1:
                    if player_x + 4 < MAZE_X:
                        if graph[(player_x + 4,
                                  player_y)].value != 15:
                            target = (player_x + 4, player_y)
                if player.movement['nx'] == -1:
                    if player_x - 4 >= 0:
                        if graph[(player_x - 4,
                                  player_y)].value != 15:
                            target = (player_x - 4, player_y)
                if player.movement['ny'] == -1:
                    if player_y - 4 >= 0:
                        if graph[(player_x,
                                  player_y - 4)].value != 15:
                            target = (player_x, player_y - 4)
                    if player.movement['ny'] == 1:
                        if player_y + 4 >= 0:
                            if graph[(player_x,
                                      player_y + 4)].value != 15:
                                target = (player_x, player_y + 4)
        if player.movement['y'] == -1:
            if player_y - 4 >= 0:
                if graph[(player_x, player_y - 4)].value != 15:
                    target = (player_x, player_y - 4)
            else:
                if player.movement['nx'] == 1:
                    if player_x + 4 < MAZE_X:
                        if graph[(player_x + 4,
                                  player_y)].value != 15:
                            target = (player_x + 4, player_y)
                if player.movement['nx'] == -1:
                    if player_x - 4 >= 0:
                        if graph[(player_x - 4,
                                  player_y)].value != 15:
                            target = (player_x - 4, player_y)
                if player.movement['ny'] == -1:
                    if player_y - 4 >= 0:
                        if graph[(player_x,
                                  player_y - 4)].value != 15:
                            target = (player_x, player_y - 4)
                    if player.movement['ny'] == 1:
                        if player_y + 4 >= 0:
                            if graph[(player_x,
                                      player_y + 4)].value != 15:
                                target = (player_x, player_y + 4)
        return Strategy.follow(start, target, graph)

    @staticmethod
    def eight_cell(start: tuple[int, int],
                   graph: dict[tuple[int, int], Cell],
                   pacman_pos: tuple[int, int],
                   home: tuple[int, int]) -> tuple[int, int]:
        if abs(start[0] - pacman_pos[0]) + abs(start[1] - pacman_pos[1]) > 8:
            target = pacman_pos
        else:
            target = home
        if abs(home[0] - pacman_pos[0]) + abs(home[1] - pacman_pos[1]) < 4:
            target = pacman_pos
        return Strategy.follow(start, target, graph)

    @staticmethod
    def mirror(start: tuple[int, int],
               red_pos: tuple[int, int],
               pacman_pos: tuple[int, int],
               graph: dict[tuple[int, int], Cell],
               last_valid_pos: tuple[int, int]) -> tuple[int, int]:
        candidate = (2 * pacman_pos[0] - red_pos[0],
                     2 * pacman_pos[1] - red_pos[1])
        if not 0 < candidate[0] < MAZE_X:
            target = last_valid_pos
        elif not 0 < candidate[1] < MAZE_Y:
            target = last_valid_pos
        elif graph[candidate].value == 15:
            target = last_valid_pos
        else:
            target = candidate
        return Strategy.follow(start, target, graph)

    @staticmethod
    def scatter(start: tuple[int, int],
                home: tuple[int, int],
                graph: dict[tuple[int, int], Cell]) -> tuple[int, int]:
        if abs(start[0] - home[0]) + abs(start[1] - home[1]) > 4:
            return Strategy.follow(start, home, graph)
        else:
            return Strategy.random(start, graph)
