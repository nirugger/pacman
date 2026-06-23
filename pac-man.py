import json
import pygame as pg
import sys

from src.core.engine import App

if __name__ == "__main__":
    # import sys
    # import os
    #
    # sys.stdout = open(os.devnull, "w")
    # # sys.stderr = open(os.devnull, "w")
    with open('config.json', 'r') as file:
        data = json.load(file)
    pg.init()
    app = App(data)
    app.run()
