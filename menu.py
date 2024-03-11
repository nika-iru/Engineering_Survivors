import pygame
import sys
import random
from scripts.utils import load_image, load_images, load_music, load_sfx, Timer
from scripts.menu_utils import Button, Cloud
import game_window


class Menu:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((960, 540))
        pygame.display.set_caption('Main Menu')

        self.display = pygame.Surface((960, 540))

        self.timer = Timer()

        self.assets = {

            'select': load_image('menu/selector.png'),
            'play': load_images('button/play'),
            'exit': load_images('button/exit'),
            'clouds': load_images('menu/clouds'),
            'menu_bg': load_image('menu/menu_bg.png'),
            'menu_bgm': load_music('menu/constant_moderato.mp3'),
            'hover': load_sfx('sfx/hover.mp3'),
            'bgm':load_music('bgm/usagi_flap.mp3')

        }

        self.play = Button(self, self.assets['play'][0].get_size(), ((960 // 2 - self.assets['play'][0].get_width() // 2), (540 // 2 - self.assets['play'][0].get_height()) + 90))
        self.exit = Button(self, self.assets['exit'][0].get_size(), ((960 // 2 - self.assets['exit'][0].get_width() // 2), (540 // 2 - self.assets['exit'][0].get_height()) + 210))
        self.select = Button(self, self.assets['select'].get_size(), (0, 0))

        self.clock = pygame.time.Clock()

        self.game_instance = game_window.Game(self.return_to_menu)

        self.current_state = 'Menu'
        
        self.run_time = self.timer.get_elapsed_time()
        self.spawn_cloud = self.timer.get_elapsed_time()
        self.clouds = []
        self.clouds_to_remove = []
        
        self.bgm = 'paused'

        self.is_hovered = False

    def run(self):
        self.current_state = 'Menu'
        self.timer.reset_timer()
        while True:
            self.run_time = self.timer.get_elapsed_time()

            if self.bgm != 'playing':
                self.play_bgm()
                self.bgm = 'playing'

            self.display.blit(pygame.transform.scale(self.assets['menu_bg'], self.screen.get_size()), (0, 0))

            current_time = self.run_time
            self.render(current_time)

            for cloud in self.clouds:
                cloud.render(self.display, cloud.index, cloud.asset)
                cloud.update()

            self.remove_clouds()

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

            if play_rect.collidepoint(pygame.mouse.get_pos()) or exit_rect.collidepoint(pygame.mouse.get_pos()):
                self.hover()
            else:
                self.is_hovered = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_rect.collidepoint(event.pos):
                        self.current_state = 'Game'
                        pygame.mixer.music.stop()
                    elif exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            if self.current_state == 'Menu':
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            elif self.current_state == 'Game':
                pygame.mixer.music.load(self.assets['bgm'])
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play()
                self.game_instance.run()

            pygame.display.update()
            self.clock.tick(60)

    def play_bgm(self):
        pygame.mixer.music.load(self.assets['menu_bgm'])
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    def render(self, current_time):
        cloud_interval = 4000
        if current_time - self.spawn_cloud >= cloud_interval:
            cloud_select = random.randint(0, 2)
            if cloud_select == 0:
                self.clouds.append(Cloud(self, self.assets['clouds'][0].get_size(), (950, random.randint(0, 100)),'clouds', 0, random.uniform(0.8, 1.8)))
            if cloud_select == 1:
                self.clouds.append(Cloud(self, self.assets['clouds'][1].get_size(), (950, random.randint(0, 50)),'clouds', 1, random.uniform(0.3, 1.3)))
            if cloud_select == 2:
                self.clouds.append(Cloud(self, self.assets['clouds'][2].get_size(), (950, random.randint(0, 100)), 'clouds', 2, random.uniform(1.3, 2.3)))
            self.spawn_cloud = current_time

    def remove_clouds(self):
        for cloud in self.clouds:
            if cloud.pos[0] <= (0 - self.assets[cloud.asset][cloud.index].get_width()):
                self.clouds_to_remove.append(cloud)

        if self.clouds_to_remove:
            for cloud in self.clouds_to_remove:
                self.clouds_to_remove.remove(cloud)

    def hover(self):
        if self.is_hovered == False:
            self.assets['hover'].play()
            self.is_hovered = True

    def return_to_menu(self):
        # Reset any game-specific state if needed
        self.current_state = 'Menu'
        pygame.mixer.music.load(self.assets['menu_bgm'])
        pygame.mixer.music.play(-1)
        Menu().run()

Menu().run()