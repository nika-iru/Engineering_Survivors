import pygame
import sys
import random
from scripts.utils import load_image, load_images, load_music
from scripts.menu_utils import Button, Cloud
import game_window


class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((960, 540))
        pygame.display.set_caption('Main Menu')

        self.display = pygame.Surface((960, 540))

        self.assets = {

            'select': load_image('menu/selector.png'),
            'play': load_images('menu/button/play'),
            'exit': load_images('menu/button/exit'),
            'clouds': load_images('menu/clouds'),
            'menu_bg': load_image('menu/menu_bg.png'),
            'menu_bgm': load_music('menu/constant_moderato.mp3')

        }

        self.play = Button(self, self.assets['play'][0].get_size(), ((960 // 2 - self.assets['play'][0].get_width() // 2), (540 // 2 - self.assets['play'][0].get_height()) + 90))
        self.exit = Button(self, self.assets['exit'][0].get_size(), ((960 // 2 - self.assets['exit'][0].get_width() // 2), (540 // 2 - self.assets['exit'][0].get_height()) + 210))
        self.select = Button(self, self.assets['select'].get_size(), (0, 0))

        self.clock = pygame.time.Clock()

        self.game_instance = game_window.Game()

        self.current_state = 'Menu'

        self.current_time = 0

        self.clouds = []

        self.bgm = 'paused'

    def run(self):
        while True:

            if self.bgm != 'playing':
                self.play_bgm()
                self.bgm = 'playing'

            self.display.blit(pygame.transform.scale(self.assets['menu_bg'], self.screen.get_size()), (0, 0))

            for cloud in self.clouds:
                cloud.render(self.display, cloud.index)
                cloud.update()

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

    def play_bgm(self):
        pygame.mixer.music.load(self.assets['menu_bgm'])
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(10)

    def render(self, current_time):
        current_time = pygame.time.get_ticks() - current_time
        if pygame.time.get_ticks() - current_time <= 0:
            cloud_select = random.randint(0, 2)
            if cloud_select == 0:
                self.clouds.append(Cloud(self, self.assets['clouds'][0].get_size(), (540, random.randint(0, 140)),'clouds', 0, 3.5))
            if cloud_select == 1:
                self.clouds.append(Cloud(self, self.assets['clouds'][1].get_size(), (540, random.randint(0, 140)),'clouds', 1, 2.5))
            if cloud_select == 2:
                self.clouds.append(Cloud(self, self.assets['clouds'][2].get_size(), (540, random.randint(0, 140)), 'clouds', 2, 1.5))


Menu().run()