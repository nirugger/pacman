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

    string = ''
    try:
        with open('config.json', 'r') as file:
            for line in file:
                if line.strip().startswith('#'):
                    continue
                string += line
            rawdata = json.loads(string)
            # rawdata = json.load(file)
    except (FileNotFoundError, PermissionError,
            IsADirectoryError, json.JSONDecodeError) as e:
        print(f"[ERROR]: {e}")
        return

    data = Config(highscore_filename=rawdata.get('highscore_filename',
                                                 'highscores.json'),
                  resolution=rawdata.get('resolution', {'x': 1080, 'y': 720}),
                  seed=rawdata.get('seed', 42))
    app = App(data)
    app.run()


# con risoluzioni troppo quadrate crasha nel setup della info surface,
# approfondire!!!!!!!!!!!
if __name__ == "__main__":
    pg.init()
    _pac_main()
    pg.quit()
