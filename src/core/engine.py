from src.level.level import Level
from src.entities.entity import Player, Red, Pink, Cyan, Orange, Enemy
from src.data import (LevelData, LevelConfig, RESOLUTION,
                      LEVELS_DATA, GameState)
from typing import Any

import json
from datetime import date
import pygame as pg
import sys


# LEVEL_SPEED = 2
# MAX_GUMS = 50


class App:
    def __init__(
            self,
            config: dict[str, str | int]
            ) -> None:

        self.title_font = pg.font.SysFont("arial", 90)
        self.menu_font = pg.font.SysFont("arial", 42)
        # from src.scenes.menu import Menu
        self.game_state: GameState = GameState.MAIN_MENU
        self.app_config = config
        self.levels_data = LEVELS_DATA
        self.screen = pg.display.set_mode(RESOLUTION, pg.NOFRAME)
        self.player = self._create_player()

        # self.menu = Menu(self.screen)
        self.level: Level = self.build_level(level_id=1)
        self.level_data: LevelData
        self.game_config: LevelConfig
        self.current_level = 1
        self.scores = self._init_scores()

        self.record_name = ""

        self.buttons: dict[str, pg.Rect] = {}

    def build_level(self, level_id: int) -> Level:

        level_config: LevelConfig = {'player': self.player,
                                     'data': self.levels_data[level_id],
                                     'game_state': GameState.IN_GAME}

        self.game_config = level_config
        return Level(self.screen, level_config, level_id)

    def run(self) -> None:
        while True:
            self.buttons.clear()
            match self.game_state:
                case GameState.MAIN_MENU:
                    self.main_menu()

                case GameState.CONTINUE:
                    self.game_config['game_state'] = GameState.IN_GAME
                    self.game_config = self.level.run()
                    self.game_state = self.game_config['game_state']

                case GameState.NEW_GAME:
                    # print(self.scores)
                    if self.player.score > min([d['score'] for d in self.scores]):
                        self._update_json_scores()
                        self.game_state = GameState.RECORD
                        continue
                    self.player = self._create_player()
                    self.level = self.build_level(level_id=1)
                    self.game_config = self.level.run()
                    self.game_state = self.game_config['game_state']

                case GameState.HIGHSCORES:
                    self.high_scores_menu()

                case GameState.RECORD:
                    self.high_scores_menu(record=True)

                case GameState.INSTRUCTIONS:
                    self.instructions_menu()

                case GameState.WIN:
                    self.current_level += 1
                    self.level = self.build_level(level_id=self.current_level)
                    self.game_config = self.level.run()
                    self.game_state = self.game_config['game_state']

                case GameState.LOSE:
                    self._save_score()
                    print("COGLIONE")
                    self.game_state = GameState.MAIN_MENU

            self.handle_events()

            # state = menu.run()

        # level_status = level.run()
        # self.menu.main_menu(self)

    @staticmethod
    def _create_player() -> Player:
        player = Player()
        return player

    def _init_scores(self) -> list[dict[str, Any]]:
        with open("game_data/highscores.json", "r") as f:
            scores = json.load(f)
        return scores['highscores']

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
        if self.player.score <= min(d['score'] for d in self.scores):
            return
        self._update_json_scores()
        self.game_state = GameState.RECORD


    def high_scores_menu(self, record=False) -> None:
        surface = pg.surface.Surface(RESOLUTION)
        surface.fill((15, 20, 25))
        title = self.title_font.render("HIGHSCORES", True, 'yellow')
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, self.menu_font.get_height()))

        with open("game_data/highscores.json", "r") as f:
            scores_dict = json.load(f)
        names = [d['name'] for d in scores_dict['highscores']]
        scores = [d['score'] for d in scores_dict['highscores']]
        columns = self.menu_font.render(':', True, 'yellow')
        centerx = surface.get_width() // 2
        padx = columns.get_width()
        pady = self.title_font.get_height() + self.menu_font.get_height()

        record_index = -1
        if record:
            record_index = 0
            while record_index < len(scores):
                if self.player.score > scores[record_index]:
                    break
                record_index += 1

        for i in range(len(names)):
            mult = i + 2
            pady = self.title_font.get_height() + (self.menu_font.get_height() * mult)
            if i == record_index:
                text = self.menu_font.render(self.record_name, True, 'yellow')
                surface.blit(text, (centerx - ((padx * 2) + text.get_width()), pady))
                text = self.menu_font.render(str(self.player.score), True, 'yellow')
                surface.blit(text, (centerx + (padx * 3), pady))
                self._update_record_name(index=i)
            else:
                text = self.menu_font.render(names[i], True, 'yellow')
                surface.blit(text, (centerx - ((padx * 2) + text.get_width()), pady))
                text = self.menu_font.render(str(scores[i]), True, 'yellow')
                surface.blit(text, (centerx + (padx * 3), pady))
            surface.blit(columns, (centerx, pady))

        # if record:
        #     with open("game_data/highscores.json", "w") as score_file:
        #         score_file.write(json.dumps(scores, indent=4))


        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def instructions_menu(self) -> None:
        surface = pg.surface.Surface(RESOLUTION)
        surface.fill((15, 20, 25))
        title = self.title_font.render("INSTRUCTIONS", True, 'yellow')
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 0))
        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def main_menu(self) -> None:
        surface = pg.surface.Surface(RESOLUTION)
        surface.fill((15, 20, 25))

        font_h = self.menu_font.get_height()

        title = self.title_font.render("PAC-MAN", True, 'yellow')
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, self.title_font.get_height()))

        text_surface = self.menu_font.render("CONTINUE", True, 'yellow')
        self.buttons['continue'] = surface.blit(text_surface,
                                                (surface.get_width() // 2 -
                                                 text_surface.get_width() // 2,
                                                 surface.get_height() // 2 -
                                                 (font_h * 2)))

        text_surface = self.menu_font.render("NEW GAME", True, 'yellow')
        self.buttons['new_game'] = surface.blit(text_surface,
                                                (surface.get_width() // 2 -
                                                 text_surface.get_width() // 2,
                                                 surface.get_height() // 2 -
                                                 font_h))

        text_surface = self.menu_font.render("HIGH SCORES", True, 'yellow')
        self.buttons['high_scores'] = surface.blit(text_surface,
                                                (surface.get_width() // 2 -
                                                 text_surface.get_width() // 2,
                                                 surface.get_height() // 2 +
                                                 font_h))

        text_surface = self.menu_font.render("INSTRUCTIONS", True, 'yellow')
        self.buttons['instructions'] = surface.blit(text_surface,
                                                (surface.get_width() // 2 -
                                                 text_surface.get_width() // 2,
                                                 surface.get_height() // 2 +
                                                 (font_h * 2)))
        
        text_surface = self.menu_font.render("EXIT", True, 'yellow')
        self.buttons['exit'] = surface.blit(text_surface,
                                                (surface.get_width() // 2 -
                                                 text_surface.get_width() // 2,
                                                 surface.get_height() // 2 +
                                                 (font_h * 3)))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def _update_record_name(self, index: int) -> None:
        with open("game_data/highscores.json", "r") as f:
            scores = json.load(f)
        scores['highscores'][index]['name'] = self.record_name
        with open("game_data/highscores.json", "w") as score_file:
            score_file.write(json.dumps(scores, indent=4))


    def _update_json_scores(self) -> None:
        with open("game_data/highscores.json", "r") as score_file:
            scores = json.load(score_file)
            scores['highscores'].append({"name": self.record_name,
                                        "score": self.player.score,
                                        "date": date.today().__str__()})
            scores['highscores'] = sorted(scores['highscores'], reverse=True,
                                        key=lambda x: x['score'])
            scores.update({'highscores': scores['highscores'][:10]})
        with open("game_data/highscores.json", "w") as score_file:
            score_file.write(json.dumps(scores, indent=4))

    def handle_events(self) -> None:
        for event in pg.event.get():


            if ((event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN) and (self.game_state is GameState.HIGHSCORES or self.game_state is GameState.INSTRUCTIONS)):
                self.game_state = GameState.MAIN_MENU
                return

            if event.type == pg.KEYDOWN and self.game_state is GameState.RECORD:
                if event.key == pg.K_RETURN:
                    self.player = self._create_player()
                    self.game_state = GameState.HIGHSCORES
                    return
                if event.key == pg.K_BACKSPACE:
                    if len(self.record_name) == 0:
                        return
                    self.record_name = self.record_name[:-1]
                    return
                self.record_name += chr(event.key)
                return

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:

                if ('continue' in self.buttons and self.buttons['continue'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.CONTINUE
                    return

                if ('new_game' in self.buttons and self.buttons['new_game'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.NEW_GAME
                    return

                if ('high_scores' in self.buttons and self.buttons['high_scores'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.HIGHSCORES
                    return

                if ('instructions' in self.buttons and self.buttons['instructions'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.INSTRUCTIONS
                    return

                if ('exit' in self.buttons and self.buttons['exit'].
                        collidepoint(pg.mouse.get_pos())):
                    pg.quit()
                    sys.exit()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
