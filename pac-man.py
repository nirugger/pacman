"""Main module for the project."""

import subprocess
import sys

import pygame as pg
from src.data import FILENAME
from src.parser.parser import Parser

from src.core.engine import App


def _pac_main() -> None:
    # import sys
    # import os

    # sys.stdout = open(os.devnull, "w")
    # # sys.stderr = open(os.devnull, "w")

    data = Parser.parser(FILENAME)

    try:
        path = 'game_data/' + data['highscore_filename']
        f = open(path, 'r')
        f.close()
    except IOError:
        path = 'game_data/' + data['highscore_filename']
        subprocess.run(['cp', 'game_data/backups/base_highscores.json',
                        path])
        subprocess.run(['chmod', '666', path])
    app = App(data)
    app.run()


if __name__ == "__main__":
    try:
        pg.init()
        pg.mouse.set_cursor(pg.cursors.broken_x)
        _pac_main()
        pg.quit()
    except pg.error:
        print("pygame did not load")
        sys.exit(1)
    except KeyboardInterrupt:
        print("eh volevi")
        sys.exit(1)
