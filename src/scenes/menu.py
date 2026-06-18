# import pygame as pg
# import pygame_menu as pgm
# import sys
# from pygame_menu import baseimage, themes

# from src.core.engine import App
# from src.level.level import Level


# class Menu:
#     """Create the main menu and its submenus"""
#     def __init__(self, surface: pg.Surface) -> None:
#         image = baseimage.BaseImage(
#             image_path="src/scenes/sfondo.jpg",
#             drawing_mode=baseimage.IMAGE_MODE_FILL,
#             drawing_offset=(0, 0)
#             )
#         my_theme = themes.THEME_DARK.copy()
#         my_theme.background_color = image

#         my_theme.widget_font_color = (255, 255, 0)
#         self._theme = my_theme
#         self._surface = surface
#         self._x = surface.get_width()
#         self._y = surface.get_height()

#     def start_game(self, app: App) -> None:
#         level = Level(self._surface, {}, app)
#         level.run()

#     @staticmethod
#     def info(surface: pg.Surface) -> None:
#         """Display the instructions for the game"""
#         start = 100
#         running = True
#         line_1 = "Puoi giocare con freccette e WASD"
#         line_2 = "Premi Q per uscire dal gioco"
#         line_3 = "Premi ESC per tornare al menu principale"
#         lines = [line_1, line_2, line_3]
#         surface.fill((15, 20, 25))
#         font = pg.font.SysFont('arial', 16)
#         for line in lines:
#             to_print = font.render(line, True, 'white')
#             surface.blit(to_print, (150, start))
#             start += 16
#         while running:
#             for event in pg.event.get():
#                 if event.type == pg.QUIT:
#                     sys.exit(0)
#                 # if event.type == pg.KEYDOWN:
#                 if event.key == pg.K_ESCAPE:
#                     running = False
#                 if event.key == pg.K_q:
#                     sys.exit()
#             pg.display.flip()

#     def highscores(self, surface: pg.Surface) -> None:
#         """Display the high scores sub-menu."""
#         import json
#         surface.fill((15, 20, 25))
#         start = 100
#         running = True
#         with open('src/scenes/highscores.json', 'r') as high:
#             data = json.load(high)['highscores']
#             text = ""
#             for i, score in enumerate(data):
#                 text += (f"{i + 1}. {data[i]['name']}: {data[i]['score']}"
#                          f" ({data[i]['date']})\n")
#             spl_text = text.split('\n')
#         font = pg.font.SysFont('arial', 50)
#         for line in spl_text:
#             to_print = font.render(line, True, 'white')
#             rect = to_print.get_rect(center=(self._x // 2, start))
#             surface.blit(to_print, rect)
#             start += 50
#         while running:
#             for event in pg.event.get():
#                 if event.type == pg.QUIT:
#                     sys.exit(0)
#                 if event.type == pg.KEYDOWN:
#                     if event.key == pg.K_ESCAPE:
#                         running = False
#                     if event.key == pg.K_q:
#                         sys.exit()
#             pg.display.flip()

#     @staticmethod
#     def quit_game() -> None:
#         pg.quit()
#         sys.exit(0)

#     def main_menu(self, app: App) -> None:
#         """Create and display the main menu."""
#         main_menu = pgm.Menu('Pac-Man', self._x, self._y,
#                              theme=self._theme, onclose=self.quit_game)
#         main_menu.add.button('Play', self.start_game, app)
#         main_menu.add.button('Info', self.info, self._surface)
#         main_menu.add.button('High scores', self.highscores, self._surface)
#         main_menu.add.button('Quit', self.quit_game)
#         main_menu.mainloop(self._surface)

#     def pause_menu(self, app: App) -> dict | None:
#         pause_menu = pgm.Menu('', self._x * 3 // 4, self._y * 3 // 4,
#                               theme=themes.THEME_DARK)
#         pause_menu.add.button('Resume game', )
#         pause_menu.add.button("Back to menu", self.main_menu, app)
#         pause_menu.add.button("Quit", self.quit_game)
#         pause_menu.mainloop(self._surface)

#     # def handle_events(self) -> None:
#     #     for event in pg.event.get():
#     #         if event.type == pg.KEYDOWN:

#     #             if event.type == pg.K_ESCAPE or event.type == pg.K_q:
#     #                 pg.quit()
#     #                 sys.exit(0)
#     #         # if event.type == pg.KEYDOWN:
#     #         #     if event.key == pg.K_ESCAPE:
#     #         #         running = False

#     #         if event.type == pg.QUIT:
#     #             pg.quit()
#     #             sys.exit(0)
