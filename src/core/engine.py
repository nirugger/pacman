import pygame as pg
from src.level.level import Level
from src.data import MAZE_X, MAZE_Y, LevelConfig, RESOLUTION

from src.entities.entity import (Player, Red, Pink, Cyan, Orange, Enemy)


class App:
    def __init__(self, config: dict[str, str | int], width: int,
                 height: int) -> None:
        from src.scenes.menu import Menu
        self.app_config = config
        # self.screen = pg.display.set_mode(config['resolution'])
        self.screen = pg.display.set_mode(RESOLUTION, pg.NOFRAME)
        self.player = self._create_player(MAZE_X, MAZE_Y)
        self.enemies = [self._create_enemy(width, height, "red"),
                        self._create_enemy(width, height, "pink"),
                        self._create_enemy(width, height, "cyan"),
                        self._create_enemy(width, height, "orange")]
        # self.super_gums = [self._create_sg([0, 0], width, height),
        #                    self._create_sg([0, height - 1], width, height),
        #                    self._create_sg([width - 1, 0], width, height),
        #                    self._create_sg([width - 1, height - 1], width,
        #                                    height)]
        self.menu = Menu(self.screen)
        self.level_config: LevelConfig = {'player': self.player, 'enemies': self.enemies}

    def run(self) -> None:
        level = Level(self.screen, self.level_config)
        level.run()
        # self.menu.main_menu(self)

    @staticmethod
    def _create_player(width: int, height: int) -> Player:
        player = Player((width // 2, height // 2), width, height)
        return player

    @staticmethod
    def _create_enemy(width: int, height: int, color: str) -> Enemy:
        enemy: Enemy
        match color:
            case "red":
                enemy = Red((0, height - 1), width, height)
            case "pink":
                enemy = Pink((0, 0), width, height)
            case "cyan":
                enemy = Cyan((width - 1, height - 1), width, height)
            case "orange":
                enemy = Orange((width - 1, height - 1), width, height)
            case _:
                raise ValueError("Unrecognised color")
        return enemy

    # @staticmethod
    # def _create_sg(position: list[int], width: int, height: int) -> SuperGum:
    #     super_gum = SuperGum(position, width, height)
    #     return super_gum
