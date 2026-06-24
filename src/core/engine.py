from src.level.level import Level
from src.entities.entity import Player
from src.data import LevelConfig, GameState, Config, LEVELS_DATA

import json
from datetime import date
import pygame as pg
import sys


class App:
    def __init__(
            self,
            config: Config
            ) -> None:

        self.first_seed = config['seed']
        self._hs = 'game_data/' + config['highscore_filename']
        self._hs_backup = 'game_data/backups/' + config['highscore_filename']
        self.resolution = (config['resolution']['x'],
                           config['resolution']['y'])

        self.screen = pg.display.set_mode(self.resolution, pg.NOFRAME)
        self.centerx = self.screen.get_width() // 2
        self.centery = self.screen.get_height() // 2
        self.levels_data = LEVELS_DATA
        self.game_state: GameState = GameState.MAIN_MENU
        self.buttons: dict[str, pg.Rect] = {}
        self.to_new_game_flag = False

        self._init_fonts()
        self._init_scores()
        self._reset_game()

    def _init_fonts(self) -> None:
        self.title_font = pg.font.SysFont("arial", 90)
        self.menu_font = pg.font.SysFont("arial", 42)
        self.instruction_font = pg.font.SysFont("arial", 33)
        self.tip_font = pg.font.SysFont("arial", 27)

    def _init_level(self, level_id: int) -> None:

        self.current_level = level_id
        level_config: LevelConfig = {
            'player': self.player,
            'data': self.levels_data[level_id],
            'game_state': GameState.IN_GAME,
            'seed': self.first_seed
        }
        self.game_config = level_config
        self.level = Level(self.screen, level_config, level_id)

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
                    if self._save_score():
                        self.to_new_game_flag = True
                        continue
                    self._reset_game()
                    self.game_config = self.level.run()
                    self.game_state = self.game_config['game_state']

                case GameState.HIGHSCORES:
                    self.high_scores_menu()

                case GameState.RECORD:
                    self.high_scores_menu(record=True)

                case GameState.RECORD_CONFIRM:
                    self._record_confirm()

                case GameState.RESET_CONFIRM:
                    self._reset_confirm()

                case GameState.INSTRUCTIONS:
                    self.instructions_menu()

                case GameState.WIN:
                    self._init_level(self.current_level + 1)
                    self.game_config = self.level.run()
                    self.game_state = self.game_config['game_state']

                case GameState.LOSE:
                    if self._save_score():
                        continue
                    self._reset_game()
                    print("COGLIONE")
                    self.game_state = GameState.MAIN_MENU

            self._handle_events()

    def _init_player(self) -> None:
        player = Player()
        self.player = player

    def _init_scores(self) -> None:
        with open("game_data/highscores.json", "r") as f:
            scores = json.load(f)
        self.scores = scores['highscores']

    def _save_score(self) -> bool:
        if self.player.has_been_cheating:
            return False
        if self.player.score > min(d['score'] for d in self.scores):
            self.game_state = GameState.RECORD_CONFIRM
            return True
        return False

    def _record_confirm(self) -> None:
        surface = pg.surface.Surface(self.resolution)
        surface.fill((15, 20, 25))
        msg = self.menu_font.render("DO YOU WANT TO SAVE YOUR LAST SCORE?",
                                    True, 'yellow')
        surface.blit(msg, (self.centerx - msg.get_width() // 2,
                           self.title_font.get_height()))

        text_surface = self.title_font.render("YES", True, 'yellow')
        padx = text_surface.get_width()
        self.buttons['yes'] = surface.blit(text_surface,
                                           (self.centerx - padx * 2,
                                            self.centery))

        text_surface = self.title_font.render("NO", True, 'yellow')
        self.buttons['no'] = surface.blit(text_surface,
                                          (self.centerx + padx,
                                           self.centery))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def _reset_game(self) -> None:
        self._init_player()
        self._init_level(level_id=1)
        self.record_index = -1
        self.record_name = ""

    def high_scores_menu(self, record: bool = False) -> None:
        surface = pg.surface.Surface(self.resolution)
        surface.fill((15, 20, 25))

        title = self.title_font.render("HIGHSCORES", True, 'yellow')
        surface.blit(title, (self.centerx - title.get_width() // 2,
                             self.menu_font.get_height()))

        with open("game_data/highscores.json", "r") as f:
            scores_dict = json.load(f)
        names = [d['name'] for d in scores_dict['highscores']]
        scores = [d['score'] for d in scores_dict['highscores']]
        columns = self.menu_font.render(':', True, 'yellow')

        padx = columns.get_width()
        pady = self.title_font.get_height() + self.menu_font.get_height()

        for i in range(len(names)):
            mult = i + 2
            pady = (self.title_font.get_height() +
                    (self.menu_font.get_height() * mult))

            if record and i == self.record_index:
                text = self.menu_font.render(self.record_name, True, 'yellow')
                surface.blit(text,
                             (self.centerx - ((padx * 2) + text.get_width()),
                              pady))
                self._update_record_name()
            else:
                text = self.menu_font.render(names[i], True, 'yellow')
                surface.blit(text,
                             (self.centerx - ((padx * 2) + text.get_width()),
                              pady))

            text = self.menu_font.render(str(scores[i]), True, 'yellow')
            surface.blit(text, (self.centerx + (padx * 3), pady))
            surface.blit(columns, (self.centerx, pady))

        text = self.tip_font.render("press any key to go back to menu",
                                    True, 'yellow')
        surface.blit(text, (self.centerx - text.get_width() // 2,
                            self.screen.get_height() - text.get_height() * 2))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def _reset_confirm(self) -> None:
        surface = pg.surface.Surface(self.resolution, pg.SRCALPHA)
        surface.fill((15, 20, 25, 200))

        msg = self.menu_font.render("DO YOU WANT TO RESET HIGHSCORES?",
                                    True, 'yellow')
        surface.blit(msg, (self.centerx - msg.get_width() // 2,
                           self.title_font.get_height()))

        text_surface = self.title_font.render("YES", True, 'yellow')
        padx = text_surface.get_width() * 2
        self.buttons['yes'] = surface.blit(text_surface,
                                           (self.centerx - padx, self.centery))

        text_surface = self.title_font.render("NO", True, 'yellow')
        padx = text_surface.get_width()
        self.buttons['no'] = surface.blit(text_surface,
                                          (self.centerx + padx, self.centery))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def _reset_high_scores(self) -> None:
        with open("game_data/backups/base_highscores.json", "r") as f:
            scores = json.load(f)
        with open("game_data/highscores.json", "w") as score_file:
            score_file.write(json.dumps(scores, indent=4))

    def instructions_menu(self) -> None:
        surface = pg.surface.Surface(self.resolution)
        surface.fill((15, 20, 25))

        title = self.title_font.render("INSTRUCTIONS", True, 'yellow')
        surface.blit(title,
                     (self.centerx - title.get_width() // 2,
                      self.menu_font.get_height()))

        text = self.tip_font.render("press any key to go back to menu",
                                    True, 'yellow')

        surface.blit(text,
                     (self.centerx - text.get_width() // 2,
                      self.screen.get_height() - text.get_height() * 2))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def main_menu(self) -> None:
        surface = pg.surface.Surface(self.resolution)
        surface.fill((15, 20, 25))

        font_h = self.menu_font.get_height()

        title = self.title_font.render("PAC-MAN", True, 'yellow')
        surface.blit(title, (self.centerx - title.get_width() // 2,
                             self.title_font.get_height()))

        text_surface = self.menu_font.render("CONTINUE", True, 'yellow')
        self.buttons['continue'] = surface.blit(
            text_surface, (self.centerx - text_surface.get_width() // 2,
                           self.centery - font_h * 2))

        text_surface = self.menu_font.render("NEW GAME", True, 'yellow')
        self.buttons['new_game'] = surface.blit(
            text_surface, (self.centerx - text_surface.get_width() // 2,
                           self.centery - font_h))

        text_surface = self.menu_font.render("HIGH SCORES", True, 'yellow')
        self.buttons['high_scores'] = surface.blit(
            text_surface, (self.centerx - text_surface.get_width() // 2,
                           self.centery + font_h))

        text_surface = self.menu_font.render("INSTRUCTIONS", True, 'yellow')
        self.buttons['instructions'] = surface.blit(
            text_surface, (self.centerx - text_surface.get_width() // 2,
                           self.centery + font_h * 2))

        text_surface = self.menu_font.render("RESET", True, 'yellow')
        self.buttons['reset'] = surface.blit(
            text_surface, (self.centerx - text_surface.get_width() // 2,
                           self.centery + font_h * 4))

        text_surface = self.menu_font.render("EXIT", True, 'yellow')
        self.buttons['exit'] = surface.blit(
            text_surface, (self.centerx - text_surface.get_width() // 2,
                           self.centery + font_h * 5))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def _update_record_name(self) -> None:
        with open("game_data/highscores.json", "r") as f:
            scores = json.load(f)
        scores['highscores'][self.record_index]['name'] = self.record_name
        with open("game_data/highscores.json", "w") as score_file:
            score_file.write(json.dumps(scores, indent=4))

    def _update_json_scores(self) -> None:
        with open("game_data/highscores.json", "r") as score_file:
            scores = json.load(score_file)
            scores['highscores'].append({"name": self.record_name,
                                         "score": self.player.score,
                                         "date": date.today().__str__()})

            scores['highscores'] = sorted(scores['highscores'],
                                          reverse=True,
                                          key=lambda x: (x['score'],
                                                         x['date']))

            scores.update({'highscores': scores['highscores'][:10]})
            self.record_index = scores['highscores'].index(
                {"name": self.record_name,
                 "score": self.player.score,
                 "date": date.today().__str__()})

        with open("game_data/highscores.json", "w") as score_file:
            score_file.write(json.dumps(scores, indent=4))

    def _handle_events(self) -> None:
        for event in pg.event.get():

            if ((event.type == pg.KEYDOWN
                 or event.type == pg.MOUSEBUTTONDOWN)
                and (self.game_state is GameState.HIGHSCORES
                     or self.game_state is GameState.INSTRUCTIONS)):
                self.game_state = GameState.MAIN_MENU
                return

            if (event.type == pg.MOUSEBUTTONDOWN
                    and self.game_state is GameState.RESET_CONFIRM):

                if ('yes' in self.buttons and self.buttons['yes'].
                        collidepoint(pg.mouse.get_pos())):
                    self._reset_high_scores()
                    self.game_state = GameState.MAIN_MENU
                    return

                if ('no' in self.buttons and self.buttons['no'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.MAIN_MENU
                    return

            if (event.type == pg.MOUSEBUTTONDOWN
                    and self.game_state is GameState.RECORD_CONFIRM):

                if ('yes' in self.buttons and self.buttons['yes'].
                        collidepoint(pg.mouse.get_pos())):
                    self._update_json_scores()
                    self.game_state = GameState.RECORD
                    return

                if ('no' in self.buttons and self.buttons['no'].
                        collidepoint(pg.mouse.get_pos())):
                    self._reset_game()
                    if self.to_new_game_flag:
                        self.to_new_game_flag = False
                        self.game_state = GameState.NEW_GAME
                        return
                    self.game_state = GameState.MAIN_MENU
                    return

            if (event.type == pg.KEYDOWN
                    and self.game_state is GameState.RECORD):

                if event.key == pg.K_RETURN:
                    self._reset_game()
                    self.game_state = GameState.MAIN_MENU
                    return

                if event.key == pg.K_BACKSPACE:
                    if len(self.record_name) == 0:
                        return
                    self.record_name = self.record_name[:-1]
                    return

                if len(self.record_name) < 10:
                    char = event.unicode
                    self.record_name += char.upper()
                return

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if ('continue' in self.buttons and
                        self.buttons['continue'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.CONTINUE
                    return

                if ('new_game' in self.buttons and
                        self.buttons['new_game'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.NEW_GAME
                    return

                if ('high_scores' in self.buttons and
                        self.buttons['high_scores'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.HIGHSCORES
                    return

                if ('instructions' in self.buttons and
                        self.buttons['instructions'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.INSTRUCTIONS
                    return

                if ('reset' in self.buttons and
                        self.buttons['reset'].
                        collidepoint(pg.mouse.get_pos())):
                    self.game_state = GameState.RESET_CONFIRM
                    return

                if ('exit' in self.buttons and
                        self.buttons['exit'].
                        collidepoint(pg.mouse.get_pos())):
                    pg.quit()
                    sys.exit()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
