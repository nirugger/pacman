import pygame as pg
from src.level.level import Level
from src.data import (LevelData, LevelConfig, RESOLUTION,
                      LEVELS_DATA, GameState)

from src.entities.entity import (Player, Red, Pink, Cyan, Orange, Enemy)


LEVEL_SPEED = 2
MAX_GUMS = 50


class App:
    def __init__(self, config: dict[str, str | int], width: int,
                 height: int) -> None:
        from src.scenes.menu import Menu
        self.game_state: GameState = GameState.NEW_GAME
        self.app_config = config
        self.levels_data = LEVELS_DATA
        self.screen = pg.display.set_mode(RESOLUTION, pg.NOFRAME)
        self.player = self._create_player()
        self.enemies = [self._create_enemy("red")]
        # self.enemies = [self._create_enemy("red"),
        #                 self._create_enemy("pink"),
        #                 self._create_enemy("cyan"),
        #                 self._create_enemy("orange")]
        self.menu = Menu(self.screen)
        self.level_data: LevelData
        self.current_level = 1

    def build_level(self, level_id: int) -> Level:

        level_config: LevelConfig = {'player': self.player,
                                     'enemies': self.enemies,
                                     'data': self.levels_data[level_id],
                                     'game_state': GameState.IN_GAME}

        return Level(
            self.screen,
            level_config,
            level_id
        )

    def run(self) -> None:
        while True:
            match self.game_state:
                case GameState.NEW_GAME:
                    level = self.build_level(level_id=1)
                    self.game_config = level.run()
                    self.game_state = self.game_config['game_state']

                case GameState.WIN:
                    self.current_level += 1
                    level = self.build_level(level_id=self.current_level)
                    self.game_config = level.run()
                    self.game_state = self.game_config['game_state']

            # state = menu.run()

        # level_status = level.run()
        # self.menu.main_menu(self)

    @staticmethod
    def _create_player() -> Player:
        player = Player()
        return player

    @staticmethod
    def _create_enemy(color: str) -> Enemy:
        enemy: Enemy
        match color:
            case "red":
                enemy = Red(color)
            case "pink":
                enemy = Pink(color)
            case "cyan":
                enemy = Cyan(color)
            case "orange":
                enemy = Orange(color)
            case _:
                raise ValueError("Unrecognised color")
        return enemy

    # @staticmethod
    # def _create_sg(position: list[int], width: int, height: int) -> SuperGum:
    #     super_gum = SuperGum(position, width, height)
    #     return super_gum
