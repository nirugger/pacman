from abc import ABC
from src.data import Config, DEFAULT_CONFIG
import json


class Parser:
    """Parse the config"""
    @staticmethod
    def parser(filename: str) -> Config:
        """
        Parse cconfig file.

        Args:
            filename(str): the name of the file.

        Returns:
            Config: A typedict with the configuration for the game
        """
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
                DEFAULT_CONFIG['highscore_filename'])

            if (not isinstance(highscore_filename, str) or
                    not highscore_filename.endswith('.json')):
                highscore_filename = DEFAULT_CONFIG['highscore_filename']
            resolution = rawdata.get('resolution', DEFAULT_CONFIG['resolution'])
            if not isinstance(resolution, dict) or \
                    'x' not in resolution or 'y' not in resolution:
                resolution = DEFAULT_CONFIG['resolution']
            elif (not isinstance(resolution['x'], int) or
                  not isinstance(resolution['y'], int) or
                  resolution['y'] > 57 / 100 * resolution['x'] or
                  resolution['x'] > 1980 or resolution['y'] > 1000 or
                  resolution['x'] < 426 or resolution['y'] < 240):
                resolution = DEFAULT_CONFIG['resolution']
            seed = rawdata.get('seed', DEFAULT_CONFIG['seed'])
            if not isinstance(seed, int):
                seed = DEFAULT_CONFIG['seed']
            return Config(
                highscore_filename=highscore_filename,
                resolution=resolution,
                seed=seed
            )

        except (IOError, json.JSONDecodeError, ValueError) as e:
            return Config(
                highscore_filename=DEFAULT_CONFIG['highscore_filename'],
                resolution=DEFAULT_CONFIG['resolution'],
                seed=DEFAULT_CONFIG['seed'])
