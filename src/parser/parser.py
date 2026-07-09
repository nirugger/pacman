"""Contain a small class for parsing config."""
from src.data import Config
import json


class Parser:
    """Parse the config."""

    @staticmethod
    def parser(filename: str) -> Config:
        """
        Parse cconfig file.

        Args:
            filename(str): the name of the file.

        Returns:
            Config: A typedict with the configuration for the game
        """
        default_config = Config(
            highscore_filename="highscores.json",
            resolution={"x": 1280, "y": 720},
            seed=42
        )
        string = ''
        try:
            with open('config.json', 'r') as file:
                for line in file:
                    if line.strip().startswith('#'):
                        continue
                    string += line
                rawdata = json.loads(string)

            highscore_filename = rawdata.get(
                'highscore_filename',
                default_config['highscore_filename'])

            if (not isinstance(highscore_filename, str) or
                    not highscore_filename.endswith('.json')):
                highscore_filename = default_config['highscore_filename']
            resolution = rawdata.get('resolution',
                                     default_config['resolution'])
            if not isinstance(resolution, dict) or \
                    'x' not in resolution or 'y' not in resolution:
                resolution = default_config['resolution']
            elif (not isinstance(resolution['x'], int) or
                  not isinstance(resolution['y'], int) or
                  resolution['y'] > 57 / 100 * resolution['x'] or
                  resolution['x'] > 1980 or resolution['y'] > 1000 or
                  resolution['x'] < 426 or resolution['y'] < 240):
                resolution = default_config['resolution']
            seed = rawdata.get('seed', default_config['seed'])
            if not isinstance(seed, int):
                seed = default_config['seed']
            return Config(
                highscore_filename=highscore_filename,
                resolution=resolution,
                seed=seed
            )

        except (IOError, json.JSONDecodeError, ValueError):
            return default_config
