"""Main module for the project."""

import json
import pygame as pg
from src.data import Config, DEFAULT_CONFIG

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

    highscore_filename = rawdata.get('highscore_filename',
                                     DEFAULT_CONFIG['highscore_filename'])
    if not isinstance(highscore_filename, str):
        highscore_filename = DEFAULT_CONFIG['highscore_filename']
    resolution = rawdata.get('resolution', DEFAULT_CONFIG['resolution'])
    if not isinstance(resolution, dict) or \
            'x' not in resolution or 'y' not in resolution:
        resolution = DEFAULT_CONFIG['resolution']
    elif (not isinstance(resolution['x'], int) or
          not isinstance(resolution['y'], int)):
        resolution = DEFAULT_CONFIG['resolution']
    seed = rawdata.get('seed', DEFAULT_CONFIG['seed'])
    if not isinstance(seed, int):
        seed = DEFAULT_CONFIG['seed']

    data = Config(highscore_filename=highscore_filename,
                  resolution=resolution,
                  seed=seed)
    app = App(data)
    app.run()


# con risoluzioni troppo quadrate crasha nel setup della info surface,
# approfondire!!!!!!!!!!!
if __name__ == "__main__":
    pg.init()
    _pac_main()
    pg.quit()
