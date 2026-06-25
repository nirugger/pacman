from src.level.level import Level
from src.entities.entity import Player
from src.data import LevelConfig, GameState, Config, LEVELS_DATA, FONT

import json
from datetime import date
from time import time
import random
import pygame as pg
import sys


class App:
    def __init__(
            self,
            config: Config
            ) -> None:

        self._init_config(config)
        self._init_screen()

        self.levels_data = LEVELS_DATA
        self.game_state: GameState = GameState.MAIN_MENU
        self.buttons: dict[str, pg.Rect] = {}
        self.menu_keys = ["continue", "new_game", "high_scores",
                          "instructions", "reset", "exit"]
        self.yes_no = ["yes", "no"]
        self.total_game_time: float = 0.0
        self.to_new_game_flag = False

        self._init_fonts()
        self._init_scores()
        self._reset_game()

    #  ------ INITIALIZATION -------------------------------------------------

    def _init_config(
            self,
            config: Config
            ) -> None:
        self.first_seed = config['seed']
        self._highscore_path = ('game_data/'
                                + config['highscore_filename'])
        self._highscore_backup_path = ('game_data/backups/'
                                       + config['highscore_filename'])
        self.resolution = (config['resolution']['x'],
                           config['resolution']['y'])

    def _init_screen(self) -> None:
        self.screen = pg.display.set_mode(self.resolution, pg.NOFRAME)
        self.centerx = self.screen.get_width() // 2
        self.centery = self.screen.get_height() // 2

    def _init_fonts(self) -> None:
        self.title_font = pg.font.Font(FONT, 80)
        self.menu_font = pg.font.Font(FONT, 40)
        self.instruction_font = pg.font.Font(FONT, 32)
        self.tip_font = pg.font.Font(FONT, 24)

        # self.title_font = pg.font.SysFont("arial", 90)
        # self.menu_font = pg.font.SysFont("arial", 42)
        # self.instruction_font = pg.font.SysFont("arial", 33)
        # self.tip_font = pg.font.SysFont("arial", 27)

    def _init_scores(self) -> None:
        with open("game_data/highscores.json", "r") as f:
            scores = json.load(f)
        self.scores = scores['highscores']

    def _init_player(self) -> None:
        player = Player()
        self.player = player

    def _init_level(self, level_id: int) -> None:
        self.current_level = level_id
        level_config: LevelConfig = {
            'player': self.player,
            'data': self.levels_data[level_id],
            'game_state': GameState.IN_GAME,
            'seed': self.first_seed,
            'time': 0.0
        }
        self.game_config = level_config
        self.level = Level(self.screen, level_config, level_id)

    def _reset_game(self) -> None:
        self._init_player()
        self._init_level(level_id=1)
        self.record_index = -1
        self.record_name = ""
        self.total_game_time = 0.0

    #  ------ LOOP CYCLE & EVENTS --------------------------------------------

    def run(self) -> None:
        while True:
            self.buttons.clear()
            match self.game_state:
                case GameState.MAIN_MENU:
                    self._main_menu()

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
                    self._high_scores_menu()

                case GameState.RECORD:
                    self._high_scores_menu(record=True)

                case GameState.RECORD_CONFIRM:
                    self._record_confirm_window()

                case GameState.RESET_CONFIRM:
                    self._reset_confirm_window()

                case GameState.INSTRUCTIONS:
                    self._instructions_menu()

                case GameState.WIN:
                    self.total_game_time += self.game_config['time']
                    self._init_level(self.current_level + 1)
                    self.game_config = self.level.run()
                    self.game_state = self.game_config['game_state']

                case GameState.LOSE:
                    self.total_game_time += self.game_config['time']
                    if self._save_score():
                        continue
                    self._reset_game()
                    print("COGLIONE")
                    self.game_state = GameState.MAIN_MENU

            self._handle_events()

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
                    if len(self.record_name) <= 0:
                        return
                    self._reset_game()
                    self.game_state = GameState.MAIN_MENU
                    return

                if event.key == pg.K_BACKSPACE:
                    if len(self.record_name) > 0:
                        self.record_name = self.record_name[:-1]
                    return

                if len(self.record_name) < 10:
                    char = str(event.unicode)
                    if char.isalnum() or char == ' ':
                        self.record_name += char
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

    #  ------ MENUS ----------------------------------------------------------

    def _main_menu(self) -> None:
        surface = pg.surface.Surface(self.resolution)
        surface.fill((15, 20, 25))
        pg.draw.rect(surface, 'yellow', surface.get_rect(), width=10)

        pady = self.menu_font.get_height() + self.instruction_font.get_height()

        title = self.title_font.render("PAC•MAN", True, 'yellow')
        surface.blit(title, (self.centerx - title.get_width() // 2,
                             self.title_font.get_height() + pady))

        pady = -70
        for i in range(len(self.menu_keys)):
            text = self.menu_font.render(self.menu_keys[i].upper(),
                                         True, 'yellow')
            self.buttons[self.menu_keys[i]] = surface.blit(
                text, (self.centerx - text.get_width() // 2,
                       self.centery + pady))
            if self._hovered_button() == self.menu_keys[i]:
                text = self.menu_font.render(
                    "\u2192 " + self.menu_keys[i].upper() + " \u2190",
                    True, 'yellow')
                self.buttons[self.menu_keys[i]] = surface.blit(
                    text, (self.centerx - text.get_width() // 2,
                           self.centery + pady))
            pady += 70

        # text_surface = self.menu_font.render("CONTINUE", True, 'yellow')
        # self.buttons['continue'] = surface.blit(
        #     text_surface, (self.centerx - text_surface.get_width() // 2,
        #                    self.centery - pady))

        # text_surface = self.menu_font.render("NEW GAME", True, 'yellow')
        # self.buttons['new_game'] = surface.blit(
        #     text_surface, (self.centerx - text_surface.get_width() // 2,
        #                    self.centery))

        # text_surface = self.menu_font.render("HIGH SCORES", True, 'yellow')
        # self.buttons['high_scores'] = surface.blit(
        #     text_surface, (self.centerx - text_surface.get_width() // 2,
        #                    self.centery + pady))

        # text_surface = self.menu_font.render("INSTRUCTIONS", True, 'yellow')
        # self.buttons['instructions'] = surface.blit(
        #     text_surface, (self.centerx - text_surface.get_width() // 2,
        #                    self.centery + pady * 2))

        # text_surface = self.menu_font.render("RESET", True, 'yellow')
        # self.buttons['reset'] = surface.blit(
        #     text_surface, (self.centerx - text_surface.get_width() // 2,
        #                    self.centery + pady * 3))

        # text_surface = self.menu_font.render("EXIT", True, 'yellow')
        # self.buttons['exit'] = surface.blit(
        #     text_surface, (self.centerx - text_surface.get_width() // 2,
        #                    self.centery + pady * 4))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def _high_scores_menu(
            self,
            record: bool = False
            ) -> None:
        surface = pg.surface.Surface(self.resolution)
        surface.fill((15, 20, 25))
        pg.draw.rect(surface, 'yellow', surface.get_rect(), width=10)

        # title = self.title_font.render("HIGHSCORES", True, 'yellow')
        # surface.blit(title, (self.centerx - title.get_width() // 2,
        #                      self.menu_font.get_height()))

        with open("game_data/highscores.json", "r") as f:
            scores_dict = json.load(f)
        names = [d['name'] for d in scores_dict['highscores']]
        scores = [d['score'] for d in scores_dict['highscores']]
        columns = self.menu_font.render(':', True, 'yellow')

        padx = columns.get_width()
        pady = self.title_font.get_height() + self.tip_font.get_height()

        for i in range(len(names)):
            mult = i
            pady = (self.menu_font.get_height() * 2 +
                    (self.title_font.get_height() -
                     self.tip_font.get_height()) * mult)

            if record and i == self.record_index:
                color = (random.randint(0, 255), random.randint(0, 255),
                         random.randint(0, 255))
                text = self.menu_font.render(self.record_name, True, color)
                surface.blit(text,
                             (self.centerx - ((padx) + text.get_width()),
                              pady))
                text = self.menu_font.render(str(scores[i]), True, color)
                surface.blit(text, (self.centerx + (padx * 2), pady))
                self._update_record_name()
            else:
                text = self.menu_font.render(names[i], True, 'yellow')
                surface.blit(text,
                             (self.centerx - ((padx) + text.get_width()),
                              pady))
                text = self.menu_font.render(str(scores[i]), True, 'yellow')
                surface.blit(text, (self.centerx + (padx * 2), pady))

            surface.blit(columns, (self.centerx, pady))

        now = time()
        if now - int(now) >= 0.5:
            if record:
                text = self.tip_font.render("enter your name",
                                            True, color)
            else:
                text = self.tip_font.render("press any key to go back to menu",
                                            True, 'yellow')
        else:
            text = self.tip_font.render("", True, 'yellow')
        surface.blit(text, (self.centerx - text.get_width() // 2,
                            self.screen.get_height() - text.get_height() * 2))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def _instructions_menu(self) -> None:
        surface = pg.surface.Surface(self.resolution)
        surface.fill((15, 20, 25))
        pg.draw.rect(surface, 'yellow', surface.get_rect(), width=10)

        title = self.title_font.render("INSTRUCTIONS", True, 'yellow')
        surface.blit(title,
                     (self.centerx - title.get_width() // 2,
                      self.menu_font.get_height()))

        now = time()
        if now - int(now) >= 0.5:
            text = self.tip_font.render("press any key to go back to menu",
                                        True, 'yellow')
        else:
            text = self.tip_font.render("", True, 'yellow')
        surface.blit(text,
                     (self.centerx - text.get_width() // 2,
                      self.screen.get_height() - text.get_height() * 2))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

#   TODO far diventare questo flusso una death screen
    def _record_confirm_window(self) -> None:
        surface = pg.surface.Surface(self.resolution)
        surface.fill((15, 20, 25))
        pg.draw.rect(surface, 'yellow', surface.get_rect(), width=10)
        # stats = []
        msg = self.tip_font.render("DO YOU WANT TO SAVE YOUR LAST SCORE?",
                                   True, 'yellow')
        surface.blit(msg, (self.centerx - msg.get_width() // 2,
                           self.title_font.get_height()))
        padx = -220
        for i in range(len(self.yes_no)):
            text = self.title_font.render(self.yes_no[i].upper(),
                                          True, 'yellow')
            npadx = padx - text.get_width() // 2
            self.buttons[self.yes_no[i]] = surface.blit(
                text, (self.centerx + npadx, self.centery))
            if self.yes_no[i] == self._hovered_button():
                rect = self.buttons[self.yes_no[i]]
                pg.draw.line(surface, 'yellow',
                             rect.bottomleft, rect.bottomright, 5)
            padx = +210
        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    def _reset_confirm_window(self) -> None:
        surface = pg.surface.Surface(self.resolution, pg.SRCALPHA)
        surface.fill((15, 20, 25, 200))
        pg.draw.rect(surface, 'yellow', surface.get_rect(), width=10)

        msg = self.menu_font.render("DO YOU WANT TO",
                                    True, 'yellow')
        surface.blit(msg, (self.centerx - msg.get_width() // 2,
                           self.title_font.get_height()))
        msg = self.menu_font.render("RESET HIGHSCORES !?",
                                    True, 'yellow')
        surface.blit(msg, (self.centerx - msg.get_width() // 2,
                           self.title_font.get_height() * 2))

        padx = -220
        for i in range(len(self.yes_no)):
            text = self.title_font.render(self.yes_no[i].upper(),
                                          True, 'yellow')
            npadx = padx - text.get_width() // 2
            self.buttons[self.yes_no[i]] = surface.blit(
                text, (self.centerx + npadx, self.centery))
            if self.yes_no[i] == self._hovered_button():
                rect = self.buttons[self.yes_no[i]]
                pg.draw.line(surface, 'yellow',
                             rect.bottomleft, rect.bottomright, 5)
            padx = +210

        # text_surface = self.title_font.render("NO", True, 'red')
        # padx = text_surface.get_width()
        # self.buttons['no'] = surface.blit(
        #     text_surface, (self.centerx + padx, self.centery))

        # text_surface = self.title_font.render("YES", True, 'green')
        # padx = text_surface.get_width() * 2
        # self.buttons['yes'] = surface.blit(
        #     text_surface, (self.centerx - padx, self.centery))

        self.screen.blit(surface, (0, 0))
        pg.display.flip()

    #  ------ HIGHSCORES -----------------------------------------------------

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

    def _save_score(self) -> bool:
        if self.player.has_been_cheating:
            return False
        if self.player.score > min(d['score'] for d in self.scores):
            self.game_state = GameState.RECORD_CONFIRM
            return True
        return False

    def _reset_high_scores(self) -> None:
        with open("game_data/backups/base_highscores.json", "r") as f:
            scores = json.load(f)
        with open("game_data/highscores.json", "w") as score_file:
            score_file.write(json.dumps(scores, indent=4))

    def _hovered_button(self) -> str | None:
        mx, my = pg.mouse.get_pos()
        for name, button in self.buttons.items():
            if button.collidepoint(mx, my):
                return name
        return None
