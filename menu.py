import pygame
import sys
from scripts.utils import load_image, load_images
from scripts.menu_utils import Button
import game_window



class Menu:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((960, 540))
        pygame.display.set_caption('Main Menu')

        self.display = pygame.Surface((960, 540))

        self.assets = {

            'select': load_image('menu/selector.png'),
            'play': load_images('menu/button/play'),
            'exit': load_images('menu/button/exit'),
            'menu_bg': load_image('menu/menu_bg.png')

        }

        self.play = Button(self, self.assets['play'][0].get_size(), ((960 // 2 - self.assets['play'][0].get_width() // 2), (540 // 2 - self.assets['play'][0].get_height()) + 90))
        self.exit = Button(self, self.assets['exit'][0].get_size(), ((960 // 2 - self.assets['exit'][0].get_width() // 2), (540 // 2 - self.assets['exit'][0].get_height()) + 210))
        self.select = Button(self, self.assets['select'].get_size(), (0, 0))

        self.clock = pygame.time.Clock()

        self.game_instance = game_window.Game()

        self.current_state = 'Menu'

    def run(self):
        while True:

            self.display.blit(pygame.transform.scale(self.assets['menu_bg'], self.screen.get_size()), (0, 0))

            play_rect = self.play.rect()
            exit_rect = self.exit.rect()

            if play_rect.collidepoint(pygame.mouse.get_pos()):
                self.play.render(self.display, 'play', 1)

                self.select.pos = (
                (960 // 2 - self.assets['select'].get_width() // 2) - (self.assets['play'][0].get_width() // 2) - 30,
                (540 // 2 - self.assets['select'].get_height()) + 80)

                self.select.select(self.display)
            else:
                self.play.render(self.display, 'play', 0)

            if exit_rect.collidepoint(pygame.mouse.get_pos()):
                self.exit.render(self.display, 'exit', 1)

                self.select.pos = (
                (960 // 2 - self.assets['select'].get_width() // 2) - (self.assets['play'][0].get_width() // 2) - 30,
                (540 // 2 - self.assets['select'].get_height()) + 200)

                self.select.select(self.display)
            else:
                self.exit.render(self.display, 'exit', 0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_rect.collidepoint(event.pos):
                        self.current_state = 'Game'  # Switch to the Game state
                    elif exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            if self.current_state == 'Menu':
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            elif self.current_state == 'Game':
                self.game_instance.run()  # Run the game loop

            pygame.display.update()
            self.clock.tick(60)


Menu().run()