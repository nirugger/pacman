from src.level.level import Level
from src.entities.entity import Player, Red, Pink, Cyan, Orange, Enemy
from src.data import (LevelData, LevelConfig, RESOLUTION,
                      LEVELS_DATA, GameState)

import pygame as pg
import sys


# LEVEL_SPEED = 2
# MAX_GUMS = 50


class App:
    def __init__(
            self,
            config: dict[str, str | int]
            ) -> None:

        # from src.scenes.menu import Menu
        self.game_state: GameState = GameState.NEW_GAME
        self.app_config = config
        self.levels_data = LEVELS_DATA
        self.screen = pg.display.set_mode(RESOLUTION, pg.NOFRAME)
        self.player = self._create_player()

        # self.menu = Menu(self.screen)
        self.level_data: LevelData
        self.game_config: LevelConfig
        self.current_level = 1

    def build_level(self, level_id: int) -> Level:

        level_config: LevelConfig = {'player': self.player,
                                     'data': self.levels_data[level_id],
                                     'game_state': GameState.IN_GAME}

        self.game_config = level_config
        return Level(self.screen, level_config, level_id)

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

                case GameState.LOSE:
                    self._save_score()
                    print("COGLIONE")
                    pg.quit()
                    sys.exit()

            # state = menu.run()

        # level_status = level.run()
        # self.menu.main_menu(self)

    @staticmethod
    def _create_player() -> Player:
        player = Player()
        return player

    # @staticmethod
    # def _create_enemy(color: str) -> Enemy:
    #     enemy: Enemy
    #     match color:
    #         case "red":
    #             enemy = Red(color)
    #         case "pink":
    #             enemy = Pink(color)
    #         case "cyan":
    #             enemy = Cyan(color)
    #         case "orange":
    #             enemy = Orange(color)
    #         case _:
    #             raise ValueError("Unrecognised color")
    #     return enemy

    def _save_score(self) -> None:
        import json
        from datetime import date
        name = input("Enter your name: ")
        with open("game_data/highscores.json", "r") as score_file:
            scores = json.load(score_file)
            scores['highscores'].append({"name": name,
                                         "score": self.player.score,
                                         "date": date.today().__str__()})
            scores['highscores'] = sorted(scores['highscores'], reverse=True,
                                          key=lambda x: x['score'])
            scores.update({'highscores': scores['highscores'][:10]})
        with open("game_data/highscores.json", "w") as score_file:
            score_file.write(json.dumps(scores, indent=4))
