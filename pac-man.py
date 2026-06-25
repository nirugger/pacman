import json
import pygame as pg
from src.data import Config

from src.core.engine import App


def pac_main():
    with open('config.json', 'r') as file:
        rawdata = json.load(file)
    pg.init()
    data = Config(highscore_filename=rawdata['highscore_filename'],
                  resolution=rawdata['resolution'],
                  seed=rawdata['seed'])
    app = App(data)
    app.run()


if __name__ == "__main__":
    # import sys
    # import os

    # sys.stdout = open(os.devnull, "w")
    # # sys.stderr = open(os.devnull, "w")
    pac_main()
