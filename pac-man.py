import json
import pygame as pg

from src.core.engine import App

if __name__ == "__main__":
    with open('config.json', 'r') as file:
        data = json.load(file)
    pg.init()
    app = App(data, 21, 21)
    app.run()
