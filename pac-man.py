"""Main module for the project."""

import json
import pygame as pg
from src.data import Config

from src.core.engine import App


def _pac_main() -> None:
    # import sys
    # import os

    # sys.stdout = open(os.devnull, "w")
    # # sys.stderr = open(os.devnull, "w")

    try:
        with open('config.json', 'r') as file:
            rawdata = json.load(file)
    except (FileNotFoundError, PermissionError,
            IsADirectoryError, json.JSONDecodeError) as e:
        print(f"[ERROR]: {e}")
        return

    data = Config(highscore_filename=rawdata['highscore_filename'],
                  resolution=rawdata['resolution'],
                  seed=rawdata['seed'])
    app = App(data)
    app.run()


# con risoluzioni troppo quadrate crasha nel setup della info surface,
# approfondire!!!!!!!!!!!
if __name__ == "__main__":
    pg.init()
    _pac_main()
    pg.quit()
