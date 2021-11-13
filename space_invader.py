import random
import sys
import pygame
import time
from pygame import mixer


# Button class
class Button:
    def __init__(self, text, width, height, pos):
        # Core attributes
        self.pressed = False

        # top rectangle
        self.rect = pygame.Rect(pos, (width, height))
        self.color = '#475F77'

        # text
        self.gui_font = pygame.font.Font("Fonts/Wellbutrin.ttf", 25)
        self.text_surf = self.gui_font.render(text, True, (255, 255, 255))  # white
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect, border_radius=12)
        SCREEN.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = '#D74B4B'  # red
            if pygame.mouse.get_pressed(num_buttons=3)[0]:  # Check if left mouse button is pressed
                mixer.Sound("Sounds/menu_selection.wav").play()
                return True
        else:
            self.color = '#475F77'
        return False


# Power Ups class
class PowerUps(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Images/Star.png"), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        # remove when out of screen
        if self.rect.y > SCREEN_HEIGHT:
            damagePowerUps.remove(self)


class HealthPowerUps(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Images/heart.png"), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(30, SCREEN_WIDTH - 30)
        self.rect.y = 150
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        # remove when out of screen
        if self.rect.y > SCREEN_HEIGHT:
            damagePowerUps.remove(self)


# Enemy class
class EnemyLv1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(10):
            self.sprites.append(pygame.image.load(f"Images/enemy_lv1/sprite_0{i}.png"))
            self.sprites.append(pygame.image.load(f"Images/enemy_lv1/sprite_0{i}.png"))
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-1000, -300)
        self.health = 25
        self.speed = random.randint(3, 6)
        self.sound = mixer.Sound("Sounds/explosion_enemy.wav")
        self.reset()

    def power_ups(self):
        if random.randint(0, 7) == 1:
            damagePowerUps.add(
                PowerUps(self.rect.x - self.image.get_width() / 2, self.rect.y - self.image.get_height() / 2))

    def update(self):
        global PLAYER_DAMAGE
        global SCORE
        global LEVEL
        self.rect.y += self.speed
        # remove when out of screen
        if self.rect.top > SCREEN.get_height():
            self.reset()
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (100, 100))

        # Laser Collisions
        for laser in laser_player:
            if pygame.sprite.collide_mask(self, laser):
                laser_player.remove(laser)
                self.health -= PLAYER_DAMAGE
                if self.health <= 0:
                    level1Enemies.remove(self)
                    explosion.add(EnemyExplosion(self.rect.center))
                    self.power_ups()
                    self.sound.play()
                    SCORE += 10

    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-1000, 0)
        self.speed = random.randint(2, 5)


class EnemyLv2(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(9):
            self.sprites.append(pygame.image.load(f"Images/enemy_lv2/sprite_{i}.png"))
            self.sprites.append(pygame.image.load(f"Images/enemy_lv2/sprite_{i}.png"))
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.direction = 2
        self.health = 35
        self.sound = mixer.Sound("Sounds/explosion_enemy.wav")

    def power_ups(self):
        if random.randint(0, 7) == 1:
            damagePowerUps.add(
                PowerUps(self.rect.x - self.image.get_width() / 2, self.rect.y - self.image.get_height() / 2))

    def update(self):
        global PLAYER_DAMAGE
        global SCORE
        global LEVEL
        self.rect.x += self.direction
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (90, 95))

        if random.randint(1, 300) == 1:
            laser_enemy.add(EnemyLaser(self.rect.midbottom))

        # Laser Collisions
        for laser in laser_player:
            if pygame.sprite.collide_mask(self, laser):
                laser_player.remove(laser)
                self.health -= PLAYER_DAMAGE
                if self.health <= 0:
                    level2Enemies.remove(self)
                    explosion.add(EnemyExplosion(self.rect.center))
                    self.power_ups()
                    self.sound.play()
                    SCORE += 10


class EnemyLv3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(8):
            self.sprites.append(pygame.image.load(f"Images/enemy_lv3/sprite_{i}.png"))
            self.sprites.append(pygame.image.load(f"Images/enemy_lv3/sprite_{i}.png"))
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (55, 55))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, 0)
        self.health = 45
        self.speed_x = random.randint(-1, 2)
        self.speed_y = random.randint(2, 5)
        self.sound = mixer.Sound("Sounds/explosion_enemy.wav")
        self.reset()

    def power_ups(self):
        if random.randint(0, 7) == 1:
            damagePowerUps.add(
                PowerUps(self.rect.x - self.image.get_width() / 2, self.rect.y - self.image.get_height() / 2))

    def update(self):
        global PLAYER_DAMAGE
        global SCORE
        global LEVEL
        # enemy movement
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # remove when out of screen
        if self.rect.top > SCREEN.get_height():
            self.reset()
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (55, 55))

        if random.randint(1, 300) == 1:
            laser_enemy.add(EnemyLaser(self.rect.midbottom))

        # Laser Collisions
        for laser in laser_player:
            if pygame.sprite.collide_mask(self, laser):
                laser_player.remove(laser)
                self.health -= PLAYER_DAMAGE
                if self.health <= 0:
                    level3Enemies.remove(self)
                    explosion.add(EnemyExplosion(self.rect.center))
                    self.power_ups()
                    self.sound.play()
                    SCORE += 10

    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, 0)
        self.speed_x = random.randint(-1, 1)
        self.speed_y = random.randint(2, 5)


class EnemyLv4(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(10):
            self.sprites.append(pygame.image.load(f"Images/boss/sprite_0{i}.png"))
        for i in range(10):
            self.sprites.append(pygame.image.load(f"Images/boss/sprite_1{i}.png"))
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (350, 300))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 2
        # health
        self.current_health = 1000
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 270
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5
        self.sound = mixer.Sound("Sounds/explosion_enemy.wav")

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def update(self):
        global PLAYER_DAMAGE
        global SCORE
        global LEVEL
        self.rect.x += self.direction
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (350, 300))

        # add laser
        temp_x = random.randint(self.rect.x + 40, self.rect.x + 320)
        temp_y = self.rect.y + 250
        if random.randint(1, 80) == 1:
            laser_enemy.add(EnemyLaser((temp_x, temp_y)))
        if random.randint(1, 130) == 1:
            laser_enemy.add(EnemyLaser((temp_x, temp_y)))
            laser_enemy.add(EnemyLaser((temp_x - 40, temp_y - 25)))
            laser_enemy.add(EnemyLaser((temp_x + 40, temp_y - 25)))
            laser_enemy.add(EnemyLaser((temp_x - 80, temp_y - 50)))
            laser_enemy.add(EnemyLaser((temp_x + 80, temp_y - 50)))
        if random.randint(1, 200) == 1:
            laser_enemy.add(EnemyLaser((temp_x, temp_y), 0, 6))
            laser_enemy.add(EnemyLaser((temp_x, temp_y), 3, 6))
            laser_enemy.add(EnemyLaser((temp_x, temp_y), -3, 6))
            laser_enemy.add(EnemyLaser((temp_x, temp_y), 6, 3))
            laser_enemy.add(EnemyLaser((temp_x, temp_y), -6, 3))

        # Laser Collisions
        for laser in laser_player:
            if pygame.sprite.collide_mask(self, laser):
                laser_player.remove(laser)
                self.get_damage(PLAYER_DAMAGE)
                SCORE += 5
                if self.target_health <= 0:
                    level4Enemies.remove(self)
                    explosion.add(EnemyExplosion(self.rect.center))
                    SCORE += 100
                    self.sound.play()

        self.basic_health()

    def basic_health(self):
        pygame.draw.rect(SCREEN, (252, 194, 0),
                         (self.rect.x + 37, self.rect.y - 12, int(self.target_health / self.health_ratio), 18),
                         border_radius=1)
        pygame.draw.rect(SCREEN, (250, 250, 250), (self.rect.x + 37, self.rect.y - 12, self.health_bar_length, 18), 2,
                         border_radius=1)


# Laser class
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, pos, speed_x=0, speed_y=6):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(6):
            self.sprites.append(pygame.image.load(f"Images/enemy_bullet/sprite_{i}.png"))
        self.current_sprite = -1
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (40, 37))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = 100
        self.sound = mixer.Sound("Sounds/weapon_enemy.wav")
        self.sound.set_volume(0.3)
        self.sound.play()

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (40, 37))
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # remove when out of screen
        if self.rect.bottom > SCREEN_HEIGHT:
            laser_enemy.remove(self)


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(3):
            self.sprites.append(pygame.image.load(f"Images/bullet/sprite_{i}.png"))
            self.sprites.append(pygame.image.load(f"Images/bullet/sprite_{i}.png"))
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (34, 32))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 11
        self.sound = mixer.Sound("Sounds/weapon_player.wav")
        self.sound.set_volume(0.3)
        self.sound.play()
        self.damage = 5

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (34, 32))
        self.rect.y -= self.speed
        # remove when out of screen
        if self.rect.top < 0:
            laser_player.remove(self)


# Explosion
class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(8):
            self.sprites.append(pygame.image.load(f"Images/explosion/sprite_{i}.png"))
            self.sprites.append(pygame.image.load(f"Images/explosion/sprite_{i}.png"))
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0
        self.max_count = 25

    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (70, 70))
        self.counter = self.counter + 1
        if self.counter == self.max_count:
            self.kill()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load("Images/player/sprite_0.png"))
        self.sprites.append(pygame.image.load("Images/player/sprite_1.png"))
        self.sprites.append(pygame.image.load("Images/player/sprite_2.png"))
        self.sprites.append(pygame.image.load("Images/player/sprite_3.png"))
        # parameter
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (100, 93))
        self.rect = self.image.get_rect()
        self.shoot_time = 0
        # health
        self.heart = pygame.transform.scale(pygame.image.load("Images/heart.png"), (110, 110))
        self.current_health = 800
        self.target_health = 800
        self.max_health = 800
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5
        # sound
        self.sound_player_hit = mixer.Sound("Sounds/explosion_player.wav")
        self.sound_star = mixer.Sound("Sounds/star.wav")

    def update(self):
        self.current_sprite += 1
        # reset
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (100, 93))
        # Vi tri may bay la vi tri mouse
        self.rect.center = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            self.fire()
        self.check_collisions()
        self.player_health_bar()
        SCREEN.blit(self.heart, (-25, 657))

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def player_health_bar(self):
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (250, 240, 80)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255, 255, 0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(20, 700, health_bar_width, 25)
        transition_bar = pygame.Rect(health_bar.right, 700, transition_width, 25)

        if self.current_health == self.max_health:
            pygame.draw.rect(SCREEN, (0, 255, 0), health_bar, border_radius=5)
        else:
            pygame.draw.rect(SCREEN, (255, 0, 0), health_bar, border_radius=5)
        pygame.draw.rect(SCREEN, transition_color, transition_bar, border_radius=5)
        pygame.draw.rect(SCREEN, (255, 255, 255), (20, 700, self.health_bar_length, 25), 4, border_radius=5)

    def fire(self):
        self.shoot_time += 1
        if self.shoot_time == 12:
            laser_player.add(Laser(self.rect.midtop))
            self.shoot_time = 0

    def check_collisions(self):
        global SCORE
        global LEVEL
        global PLAYER_DAMAGE

        for i in damagePowerUps:
            if pygame.sprite.collide_rect(self, i):
                self.sound_star.play()
                damagePowerUps.remove(i)
                PLAYER_DAMAGE += 1
                SCORE += 5
                pygame.display.update()

        for i in healthPowerUps:
            if pygame.sprite.collide_rect(self, i):
                self.sound_star.play()
                self.get_health(200)
                healthPowerUps.remove(i)
                SCORE += 5
                pygame.display.update()

        for enemy in level1Enemies:
            if pygame.sprite.collide_mask(self, enemy):
                self.sound_player_hit.play()
                level1Enemies.remove(enemy)
                self.get_damage(100)
                SCORE += 5
                pygame.display.update()
                if self.target_health <= 0:
                    for ene in level1Enemies:
                        level1Enemies.remove(ene)
                    game_over()
                elif not level1Enemies:
                    level_completed()
                    LEVEL = 2

        for enemy in level2Enemies:
            if pygame.sprite.collide_mask(self, enemy):
                self.sound_player_hit.play()
                level2Enemies.remove(enemy)
                self.get_damage(150)
                SCORE += 5
                pygame.display.update()
                if self.target_health <= 0:
                    for ene in level2Enemies:
                        level2Enemies.remove(ene)
                    game_over()
                elif not level2Enemies:
                    level_completed()
                    LEVEL = 3

        for enemy in level3Enemies:
            if pygame.sprite.collide_mask(self, enemy):
                self.sound_player_hit.play()
                level3Enemies.remove(enemy)
                self.get_damage(200)
                SCORE += 5
                pygame.display.update()
                if self.target_health <= 0:
                    for ene in level3Enemies:
                        level3Enemies.remove(ene)
                    game_over()
                elif not level3Enemies:
                    level_completed()
                    LEVEL = 4

        for enemy in level4Enemies:
            if pygame.sprite.collide_mask(self, enemy):
                self.get_damage(4)
                pygame.display.update()
                if self.target_health <= 0:
                    for ene in level4Enemies:
                        level4Enemies.remove(ene)
                    game_over()

        for laser in laser_enemy:
            if pygame.sprite.collide_rect(self, laser):
                self.sound_player_hit.play()
                laser_enemy.remove(laser)
                self.get_damage(100)
                if self.target_health <= 0:
                    game_over()
                    LEVEL = 0


class Game:
    def __init__(self):
        # set player
        self.player = Player()

    def playLevel1(self):
        global LEVEL
        # add player
        level1.add(self.player)
        # music game
        mixer.music.load("Sounds/level1_music.wav")
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
        # Background image
        background_image = pygame.transform.scale(pygame.image.load("Images/background/background_lv1.png"),
                                                  (SCREEN_WIDTH, SCREEN_HEIGHT))
        # hide mouse cursor
        pygame.mouse.set_visible(False)
        # add enemy
        for i in range(13):
            level1Enemies.add(EnemyLv1())
        keep_going = True
        while keep_going:
            # set FPS = 60
            clock.tick(60)
            if LEVEL != 1:
                break
            SCREEN.blit(background_image, (0, 0))
            # event quit window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause()

            # show score player
            score_font = pygame.font.Font("Fonts/Montserrat-ExtraBold.ttf", 40)
            score_label = score_font.render(f"Score: {SCORE}", True, (255, 255, 255))
            SCREEN.blit(score_label, (10, 5))

            # complete level
            if not level1Enemies:
                level_completed()
                LEVEL = 2
                pygame.display.update()
                break

            level1Enemies.draw(SCREEN)
            level1.draw(SCREEN)
            laser_player.draw(SCREEN)
            explosion.draw(SCREEN)
            damagePowerUps.draw(SCREEN)

            level1.update()
            level1Enemies.update()
            laser_player.update()
            explosion.update()
            damagePowerUps.update()
            pygame.display.update()

    def playLevel2(self):
        global LEVEL
        # add player
        level2.add(self.player)
        # Background image
        background_image = pygame.transform.scale(pygame.image.load("Images/background/background_lv2.png"),
                                                  (SCREEN_WIDTH, SCREEN_HEIGHT))
        # hide mouse cursor
        pygame.mouse.set_visible(False)
        # add enemy
        for i in range(6):
            for j in range(3):
                if j % 2 == 0:
                    level2Enemies.add(EnemyLv2(180 + i * 150, 50 + j * 100))
                else:
                    level2Enemies.add(EnemyLv2(110 + i * 150, 50 + j * 100))

        keep_going = True
        while keep_going:
            # set FPS = 60
            clock.tick(60)
            if LEVEL != 2:
                break
            SCREEN.blit(background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause()

            # enemy_level2 move
            shift = False
            for alien in (level2Enemies.sprites()):
                if alien.rect.left <= 0 or alien.rect.right >= SCREEN_WIDTH - 50:
                    shift = True
            if shift:
                for alien in (level2Enemies.sprites()):
                    # Shift down
                    if alien.rect.bottom <= SCREEN_HEIGHT - 200:
                        alien.rect.y += 12
                    else:
                        alien.rect.y -= 24
                    # Reverse the direction and move the alien off the edge so 'shift' doesn't trigger
                    alien.direction = -1 * alien.direction
                    alien.rect.x += alien.direction

            # Power up
            spawn_health = random.randint(1, 1500)
            if spawn_health == 1:
                healthPowerUps.add(HealthPowerUps())

            # ve thong tin diem so cua player
            score_font = pygame.font.Font("Fonts/Montserrat-ExtraBold.ttf", 40)
            score_label = score_font.render(f"Score: {SCORE}", True, (255, 255, 255))
            SCREEN.blit(score_label, (10, 5))

            if not level2Enemies:
                level_completed()
                LEVEL = 3
                pygame.display.update()
                break

            level2Enemies.draw(SCREEN)
            level2.draw(SCREEN)
            laser_player.draw(SCREEN)
            laser_enemy.draw(SCREEN)
            explosion.draw(SCREEN)
            damagePowerUps.draw(SCREEN)
            healthPowerUps.draw(SCREEN)

            level2.update()
            level2Enemies.update()
            laser_player.update()
            laser_enemy.update()
            explosion.update()
            damagePowerUps.update()
            healthPowerUps.update()
            pygame.display.update()

    def playLevel3(self):
        clock.tick(60)
        global LEVEL
        level3.add(self.player)
        background_image = pygame.transform.scale(pygame.image.load("Images/background/background_lv3.png"),
                                                  (SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mouse.set_visible(False)
        for i in range(13):
            level3Enemies.add(EnemyLv3())
        keep_going = True
        while keep_going:
            if LEVEL != 3:
                break
            SCREEN.blit(background_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause()

            spawn_health = random.randint(1, 2000)
            if spawn_health == 1:
                healthPowerUps.add(HealthPowerUps())

            # ve thong tin diem so cua player
            score_font = pygame.font.Font("Fonts/Montserrat-ExtraBold.ttf", 40)
            score_label = score_font.render(f"Score: {SCORE}", True, (255, 255, 255))
            SCREEN.blit(score_label, (10, 5))

            if not level3Enemies:
                level_completed()
                LEVEL = 4
                pygame.display.update()
                break

            level3Enemies.draw(SCREEN)
            level3.draw(SCREEN)
            laser_player.draw(SCREEN)
            laser_enemy.draw(SCREEN)
            explosion.draw(SCREEN)
            damagePowerUps.draw(SCREEN)
            healthPowerUps.draw(SCREEN)

            level3.update()
            level3Enemies.update()
            laser_player.update()
            laser_enemy.update()
            explosion.update()
            damagePowerUps.update()
            healthPowerUps.update()
            pygame.display.update()

    def playLevel4(self):
        global LEVEL
        global SCORE
        # add player
        level4.add(self.player)
        mixer.music.load("Sounds/level4_music.wav")
        mixer.music.play(-1)
        # Background image
        background_image = pygame.transform.scale(pygame.image.load("Images/background/background_lv4.png"),
                                                  (SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.mouse.set_visible(False)

        # Create a boss
        level4Enemies.add(EnemyLv4(100, 35))
        while True:
            clock.tick(60)
            if LEVEL != 4:
                break
            SCREEN.blit(background_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause()

            # enemy_level4 movement
            shift = False
            for alien in (level4Enemies.sprites()):
                if alien.rect.left <= 0 or alien.rect.right >= SCREEN_WIDTH:
                    shift = True
            if shift:
                for alien in (level4Enemies.sprites()):
                    # Shift down
                    if alien.rect.bottom <= SCREEN_HEIGHT - 300:
                        alien.rect.y += 25
                    else:
                        alien.rect.y -= 50

                    # Reverse the direction and move the alien off the edge so 'shift' doesn't trigger
                    alien.direction = -1 * alien.direction
                    alien.rect.x += alien.direction

            # health power_ups
            if random.randint(1, 2000) == 1:
                healthPowerUps.add(HealthPowerUps())
            if random.randint(1, 500) == 1:
                level1Enemies.add(EnemyLv1())

            # ve thong tin diem so cua player
            score_font = pygame.font.Font("Fonts/Montserrat-ExtraBold.ttf", 40)
            score_label = score_font.render(f"Score: {SCORE}", True, (255, 255, 255))
            SCREEN.blit(score_label, (10, 5))

            # win game
            if not level4Enemies:
                mixer.music.load("Sounds/level_complete.wav")
                mixer.music.set_volume(0.5)
                mixer.music.play()
                win_game = pygame.transform.scale(pygame.image.load("Images/win_game.png"), (600, 520))
                SCREEN.blit(win_game, (270, 90))
                pygame.display.update()
                time.sleep(7)
                pygame.mouse.set_visible(True)
                LEVEL = 0
                SCORE = 0
                level1Enemies.empty()
                level2Enemies.empty()
                level3Enemies.empty()
                level4Enemies.empty()
                level1.empty()
                level2.empty()
                level3.empty()
                level4.empty()
                pygame.display.update()

            # draw
            level1Enemies.draw(SCREEN)
            level4Enemies.draw(SCREEN)
            level4.draw(SCREEN)
            laser_player.draw(SCREEN)
            laser_enemy.draw(SCREEN)
            explosion.draw(SCREEN)
            damagePowerUps.draw(SCREEN)
            healthPowerUps.draw(SCREEN)

            # update
            level1Enemies.update()
            level4Enemies.update()
            level4.update()
            laser_player.update()
            laser_enemy.update()
            explosion.update()
            damagePowerUps.update()
            healthPowerUps.update()
            pygame.display.update()

    def start(self):
        while True:
            clock.tick(60)
            global LEVEL
            if LEVEL == 0:
                MainMenu()
                break
            elif LEVEL == 1:
                self.playLevel1()
            elif LEVEL == 2:
                self.playLevel2()
            elif LEVEL == 3:
                self.playLevel3()
            elif LEVEL == 4:
                self.playLevel4()


def pause():
    paused = True
    pygame.mouse.set_visible(True)
    mixer.music.pause()
    pause_image = pygame.transform.scale(pygame.image.load("Images/background/pause_background.jpg"), (1100, 750))
    SCREEN.blit(pause_image, (0, 0))
    score_font = pygame.font.Font("Fonts/Montserrat-ExtraBold.ttf", 120)
    score_label = score_font.render(f"Paused", True, (255, 140, 0))
    SCREEN.blit(score_label, (330, 250))
    score_font = pygame.font.Font("Fonts/Montserrat-ExtraBold.ttf", 40)
    score_label = score_font.render(f"Press C to continue or Q to quit.", True, (255, 255, 255))
    SCREEN.blit(score_label, (200, 450))
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pygame.mouse.set_visible(False)
                    mixer.music.unpause()
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(5)


def level_completed():
    mixer.music.pause()
    completed_sound = mixer.Sound("Sounds/level_complete.wav")
    completed_sound.play().set_volume(0.5)
    completed_level_label = pygame.image.load("Images/completed_level_text.png")
    SCREEN.blit(completed_level_label, (SCREEN_WIDTH / 2 - 353, SCREEN_HEIGHT / 2 - 26))
    pygame.display.update()
    time.sleep(7)
    mixer.music.unpause()


def game_over():
    global SCORE
    global LEVEL
    pygame.mixer.music.stop()
    game_over_label = pygame.image.load("Images/game_over_text.png")
    SCREEN.blit(game_over_label, (SCREEN_WIDTH / 2 - 260, SCREEN_HEIGHT / 2 - 33))
    pygame.display.update()
    mixer.Sound("Sounds/game_over.wav").play()
    time.sleep(7)
    LEVEL = 0
    SCORE = 0
    level1Enemies.empty()
    level2Enemies.empty()
    level3Enemies.empty()
    level4Enemies.empty()
    level1.empty()
    level2.empty()
    level3.empty()
    level4.empty()
    pygame.mouse.set_visible(True)


def aboutMenu():
    background_image = pygame.transform.scale(pygame.image.load("Images/background/about_menu.png"), (1100, 750))
    # menu
    button_quit = Button('Quit', 200, 50, (420, 630))

    while True:
        SCREEN.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        button_quit.draw()
        # bam nut
        if button_quit.check_click():
            MainMenu()
            break
        pygame.display.update()


def MainMenu():
    # intro music
    mixer.music.load("Sounds/welcome_background_music.wav")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    # intro background
    background_image = pygame.transform.scale(pygame.image.load("Images/background/background_menu.png"), (1100, 750))

    # menu
    button_start = Button('Start', 200, 50, (420, 410))
    button_about = Button('About', 200, 50, (420, 490))
    button_quit = Button('Quit', 200, 50, (420, 570))

    while True:
        clock.tick(60)
        SCREEN.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        button_start.draw()
        button_about.draw()
        button_quit.draw()
        # bam nut
        if button_start.check_click():
            global LEVEL
            LEVEL = 1
            Game().start()
            break
        if button_about.check_click():
            aboutMenu()
            break
        if button_quit.check_click():
            pygame.quit()
            sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()

    # Game window
    pygame.display.set_caption("Space Invaders")  # set caption
    icon = pygame.image.load('Images/ufo.png')
    pygame.display.set_icon(icon)  # set icon

    # list objects
    level1 = pygame.sprite.Group()
    level2 = pygame.sprite.Group()
    level3 = pygame.sprite.Group()
    level4 = pygame.sprite.Group()

    level1Enemies = pygame.sprite.Group()
    level2Enemies = pygame.sprite.Group()
    level3Enemies = pygame.sprite.Group()
    level4Enemies = pygame.sprite.Group()

    laser_player = pygame.sprite.Group()
    laser_enemy = pygame.sprite.Group()
    explosion = pygame.sprite.Group()
    damagePowerUps = pygame.sprite.Group()
    healthPowerUps = pygame.sprite.Group()

    # global variable
    SCREEN_WIDTH = 1100
    SCREEN_HEIGHT = 750
    LEVEL = 1
    SCORE = 0
    PLAYER_DAMAGE = 5

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    MainMenu()
    pygame.quit()
    sys.exit()
