import json
import pygame as pg
from src.data import MAZE_X, MAZE_Y
import sys

from src.core.engine import App

if __name__ == "__main__":
    with open('config.json', 'r') as file:
        data = json.load(file)
    pg.init()
    sys.setrecursionlimit(500000)
    app = App(data, MAZE_X, MAZE_Y)
    app.run()
