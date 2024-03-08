import pygame
import sys
import random
import math

from scripts.utils import load_image, load_images
from scripts.entities import Player, Enemy, Bullet, Camera, Background, Chunk, Card
class Game:
    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((960, 540))
        pygame.display.set_caption("Engineering Survivors")

        self.display = pygame.Surface((self.screen.get_width(), self.screen.get_height()))

        self.clock = pygame.time.Clock()

        self.assets = {

            'player': load_images('player'),
            'student': load_images('enemy/student'),
            'background': load_images('background'),
            'bullet': load_images('bullet'),
            'dmg': load_images('level/buffs/dmg'),
            'mvs': load_images('level/buffs/mvs'),
            'hp': load_images('level/buffs/hp'),
            'ats': load_images('level/buffs/ats')

        }

        # player initialization
        player_size = self.assets['player'][0].get_size()
        player_pos = (self.screen.get_width() // 2 - player_size[0] // 2, self.screen.get_height() // 2 - player_size[1] // 2)
        self.player = Player(self, player_pos, player_size)
        self.camera = Camera(self, self.player.center())
        # player movement
        self.movement = [False, False, False, False]

        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction = self.camera.apply_inverse(pygame.Vector2(mouse_x, mouse_y))

        bullet_pos = [self.player.pos[0] + (self.player.size[0] // 2), self.player.pos[1] + (self.player.size[1] // 2)]
        bullet_size = [5, 5]
        bullet_speed = 3
        bullet_interval = self.player.atkspd
        self.bullet = Bullet(self, bullet_pos, bullet_size, bullet_speed, bullet_interval, False, direction)
        self.shoot_timer = 0
        self.shoot_interval = self.bullet.interval
        self.bullets = []

        self.enemies = []
        self.spawn_timer = pygame.time.get_ticks()

        bg_size = self.assets['background'][0].get_size()
        bg_pos = (self.display.get_width() // 2 - self.assets['background'][0].get_width() // 2, self.display.get_height() // 2 - self.assets['background'][0].get_height() // 2)
        self.background = Background(self, bg_size, bg_pos)

        self.load_chunks = []
        self.loaded_chunks = []

        self.second_time = 0
        self.pause_time = 0
        self.run_time = pygame.time.get_ticks() - self.pause_time

        self.dmg = Card(self, self.assets['dmg'][0].get_size(), [0,0], 'dmg')
        self.ats = Card(self, self.assets['ats'][0].get_size(), [0,0], 'ats')
        self.mvs = Card(self, self.assets['mvs'][0].get_size(), [0,0], 'mvs')
        self.hp = Card(self, self.assets['hp'][0].get_size(), [0,0], 'hp')
        self.buff_list = [self.dmg, self.ats, self.mvs, self.hp]
        self.render_list = []
        self.cards = []

        self.game_state = 'running'

    def run(self):
        while True:

            self.display.fill((15, 220, 250))

            self.background.render(self.display, self.camera, 'background', 0)
            self.chunks_to_load()

            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x_on_screen = self.camera.apply_inverse(pygame.Vector2(mouse_x, mouse_y))

            self.player.render(self.display, self.camera, mouse_x_on_screen[0])

            for bullet in self.bullets:
                bullet.render(self.display, self.camera)

            for enemy in self.enemies:
                enemy.render(self.display, self.camera)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_p:
                        if self.game_state == 'running':
                            self.is_paused()
                        elif self.game_state == 'paused':
                            self.is_running()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False



            if self.game_state == 'running':
                self.update_game()
            elif self.game_state == 'paused':
                self.pause_time = pygame.time.get_ticks() - self.run_time
                font = pygame.font.Font(None, 128)
                text = font.render("Paused", True, (0, 0, 0))
                self.display.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))

            self.check_player_xp()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.flip()

            '''print(f'Total Run Time: {self.run_time}\nTotal Pause Time: {self.pause_time}\nTotal Tick Time: {pygame.time.get_ticks()}')'''

    def shoot_bullet(self, current_time):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction = self.camera.apply_inverse(pygame.Vector2(mouse_x, mouse_y))

        bullet_pos = [self.player.pos[0] + self.player.size[0] // 2, self.player.pos[1] + self.player.size[1] // 2]
        bullet_size = [5, 5]
        bullet_speed = 3.5
        bullet_interval = self.player.atkspd
        self.bullets.append(Bullet(self, bullet_pos, bullet_size, bullet_speed, bullet_interval, False, direction))
        self.shoot_timer = current_time
        self.shoot_interval = self.bullet.interval

    def check_current_chunk(self):
        player_x = int(self.player.pos[0])
        player_y = int(self.player.pos[1])

        while player_x % self.screen.get_height() != 0:
            player_x -= 1
        chunk_left_boundary = player_x

        while player_y % self.screen.get_height() != 0:
            player_y -= 1
        chunk_top_boundary = player_y

        current_chunk = (chunk_left_boundary, chunk_top_boundary)
        return current_chunk

    def chunks_to_load(self):
        chunk_left = self.check_current_chunk()[0]
        chunk_top = self.check_current_chunk()[1]
        self.load_chunks.append(Chunk(self, (chunk_left - self.screen.get_width(), chunk_top - self.screen.get_height())))
        self.load_chunks.append(Chunk(self, (chunk_left, chunk_top - self.screen.get_height())))
        self.load_chunks.append(Chunk(self, (chunk_left + self.screen.get_width(), chunk_top - self.screen.get_height())))
        self.load_chunks.append(Chunk(self, (chunk_left - self.screen.get_width(), chunk_top)))
        self.load_chunks.append(Chunk(self, (chunk_left, chunk_top)))
        self.load_chunks.append(Chunk(self, (chunk_left + self.screen.get_width(), chunk_top)))
        self.load_chunks.append(Chunk(self, (chunk_left - self.screen.get_width(), chunk_top + self.screen.get_height())))
        self.load_chunks.append(Chunk(self, (chunk_left, chunk_top + self.screen.get_height())))
        self.load_chunks.append(Chunk(self, (chunk_left + self.screen.get_width(), chunk_top + self.screen.get_height())))

        for chunk in self.load_chunks:
            if chunk not in self.loaded_chunks:
                self.background = Background(self, (self.screen.get_width(), self.screen.get_height()), chunk.pos)
                self.background.render(self.display, self.camera, 'background', 0)
                self.loaded_chunks.append(chunk)
                self.load_chunks.remove(chunk)

        if not self.loaded_chunks:
            for chunk in self.loaded_chunks:
                if abs(chunk.pos[0] - self.check_current_chunk()[0]) >= 960:
                    self.load_chunks.remove(chunk)
                elif abs(chunk.pos[1] - self.check_current_chunk()[1]) >= 540:
                    self.load_chunks.remove(chunk)

    def spawn_enemies_easy(self, current_time):
        # enemy initialization
        chunk_left = self.check_current_chunk()[0]
        chunk_right = self.check_current_chunk()[0] + (self.screen.get_width() * 2)
        chunk_top = self.check_current_chunk()[1]
        chunk_bottom = self.check_current_chunk()[1] + (self.screen.get_height() * 2)

        spawn_interval = 3000

        student_size = self.assets['student'][0].get_size()
        student_hp = 5
        student_speed = 1.5
        student_xp_worth = 2

        if current_time - self.spawn_timer >= spawn_interval:
            for enemiesToSpawn in range(2):
                # Randomly choose one of the four sides for enemy spawn
                side = random.choice(['left', 'right', 'top', 'bottom'])

                if side == 'left':
                    enemy_pos = [
                        random.randint(chunk_left - self.screen.get_width(), chunk_left),
                        random.randint(chunk_top, chunk_bottom)
                    ]
                elif side == 'right':
                    enemy_pos = [
                        random.randint(chunk_right, chunk_right + self.screen.get_width()),
                        random.randint(chunk_top, chunk_bottom)
                    ]
                elif side == 'top':
                    enemy_pos = [
                        random.randint(chunk_left, chunk_right),
                        random.randint(chunk_top - self.screen.get_height(), chunk_top)
                    ]
                elif side == 'bottom':
                    enemy_pos = [
                        random.randint(chunk_left, chunk_right),
                        random.randint(chunk_bottom, chunk_bottom + self.screen.get_height())
                    ]

                self.enemies.append(Enemy(self, enemy_pos, student_size, student_hp, student_speed, student_xp_worth))

            self.spawn_timer = current_time

    def bullet_enemy_collision(self, bullets_to_remove):

        for bullet in self.bullets:
            bullet_rect = bullet.rect()
            for enemy in self.enemies:
                enemy_rect = enemy.rect()
                if bullet_rect.colliderect(enemy_rect):
                    enemy.eHP = enemy.eHP - self.player.damage
                    print(f'enemy hp - {self.player.damage}')
                    if enemy.eHP <= 0:
                        self.player.currentXP += enemy.eXP
                        print(f'xp + {enemy.eXP}; currentxp {self.player.currentXP}; neededxp {self.player.neededXP}')
                        self.enemies.remove(enemy)
                    bullets_to_remove.append(bullet)

    def remove_bullets(self, bullets_to_remove):

        for bullet in self.bullets:
            if abs(math.atan2(self.player.pos[1] - bullet.pos[1], self.player.pos[0] - bullet.pos[0])) == 1000:
                bullets_to_remove.append(bullet)

        if bullets_to_remove:
            for bullet in bullets_to_remove:
                self.bullets.remove(bullet)

    def check_player_invul(self):
        player_rect = self.player.rect()

        if not self.player.invul:
            for enemy in self.enemies:
                enemy_rect = enemy.rect()
                if player_rect.colliderect(enemy_rect):
                    self.player.take_dmg(1)
                    self.player.apply_invulnerability()

        if self.player.invul:
            current_time = self.run_time
            if current_time - self.player.invul_timer >= 1000:
                self.player.invul = False
                self.player.mvspd = self.player.base_spd

    def update_game(self):
        self.run_time = pygame.time.get_ticks() - self.pause_time
        self.player.update(((self.movement[1] - self.movement[0]), (self.movement[3] - self.movement[2])))
        self.camera.target = self.player.center()

        self.check_current_chunk()

        for bullet in self.bullets:
            bullet.update()

        for enemy in self.enemies:
            enemy.update(self.player)

        current_time = self.run_time
        if current_time - self.shoot_timer >= self.shoot_interval:
            self.shoot_bullet(current_time)

        self.spawn_enemies_easy(current_time)

        self.check_player_invul()

        bullets_to_remove = []
        self.bullet_enemy_collision(bullets_to_remove)
        self.remove_bullets(bullets_to_remove)

        self.second_time = self.run_time // 1000

        font = pygame.font.Font(None, 36)
        text = font.render(str(self.second_time), True, (250, 250, 250))
        self.display.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 10))

        self.clock.tick(60)

    def check_player_xp(self):
        if self.player.currentXP >= self.player.neededXP:
            self.select_buff()

    def select_buff(self):
        self.is_paused()

        card_pos_1 = [((self.display.get_width() // 3) / 2 - self.assets['dmg'][0].get_width() // 2), (self.display.get_height() // 2 - self.assets['dmg'][0].get_height() // 2)]
        card_pos_2 = [(self.display.get_width() // 2 - self.assets['dmg'][0].get_width() // 2), (self.display.get_height() // 2 - self.assets['dmg'][0].get_height() // 2)]
        card_pos_3 = [((((self.display.get_width() // 3) * 2) + (self.display.get_width() // 3) // 2) - self.assets['dmg'][0].get_width() // 2), (self.display.get_height() // 2 - self.assets['dmg'][0].get_height() // 2)]

        card_pos = [card_pos_1, card_pos_2, card_pos_3]

        while len(self.cards) != 3:
            rand = random.randint(0, len(self.buff_list) - 1)
            if self.buff_list[rand] not in self.cards:
                self.cards.append(self.buff_list[rand])

        for index, item in enumerate(self.cards):
            item.pos = card_pos[index]
            self.render_list.append(item)

        self.buff_00 = self.render_list[0]
        self.buff_01 = self.render_list[1]
        self.buff_02 = self.render_list[2]

        self.buff_00.render(self.display, 0)
        self.buff_01.render(self.display, 0)
        self.buff_02.render(self.display, 0)

        buff_00_rect = self.buff_00.rect()
        buff_01_rect = self.buff_01.rect()
        buff_02_rect = self.buff_02.rect()

        if buff_00_rect.collidepoint(pygame.mouse.get_pos()):
            self.buff_00.render(self.display, 1)
        elif buff_01_rect.collidepoint(pygame.mouse.get_pos()):
            self.buff_01.render(self.display, 1)
        elif buff_02_rect.collidepoint(pygame.mouse.get_pos()):
            self.buff_02.render(self.display, 1)

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buff_00_rect.collidepoint(event.pos):
                    self.buff_up(self.buff_00)
                elif buff_01_rect.collidepoint(event.pos):
                    self.buff_up(self.buff_01)
                elif buff_02_rect.collidepoint(event.pos):
                    self.buff_up(self.buff_02)

    def buff_up(self, buff):
        if buff.asset == 'dmg':
            self.player.damage += 2
        elif buff.asset == 'hp':
            self.player.health += 1
        elif buff.asset == 'mvs':
            self.player.mvspd += 0.15
        elif buff.asset == 'ats':
            self.player.atkspd += 100
        self.level_up()

    def level_up(self):
        self.player.playerlvl += 1
        self.player.currentXP -= self.player.neededXP
        self.player.neededXP += self.player.neededXP * 0.3
        self.render_list = []
        self.cards = []
        print(f'level up: level {self.player.playerlvl}; neededXP {self.player.neededXP}')
        self.is_running()

    def is_running(self):
        self.game_state = 'running'
        self.run_time = pygame.time.get_ticks() - self.pause_time

    def is_paused(self):
        self.game_state = 'paused'
        self.run_time = pygame.time.get_ticks() - self.pause_time
