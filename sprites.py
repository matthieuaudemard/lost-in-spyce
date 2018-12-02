from os import path

import pygame as pg
import random

from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(PLAYER_IMAGE)
        self.image = pg.transform.scale(self.image, (int(PLAYER_SCALE * self.image.get_rect().width),
                                                     int(PLAYER_SCALE * self.image.get_rect().height)))
        self.image.set_colorkey(BLACK)
        self.original_image = self.image.copy()
        self.blank_image = self.game.spritesheet.get_image('blank.png')
        self.blank_image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * .80 // 2
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - SCREEN_OFFSET
        self.speedx = 0
        self.shoot_number = 0
        self.last_shot = pg.time.get_ticks()
        self.shield = None
        self.lives = START_PLAYER_LIVES
        self.weapon = MIN_WEAPON
        self.hidden = False
        self.flashing = False
        self.current_frame = 0
        self.untouchable_timer = pg.time.get_ticks()
        self.hide_timer = pg.time.get_ticks()
        self.load_data()
        self.score = 0

    def load_data(self):
        self.shot_sound = pg.mixer.Sound(path.join(self.game.snd_dir, LASER_SOUND))
        self.shot_sound.set_volume(0.1)
        self.shield_up_sound = pg.mixer.Sound(path.join(self.game.snd_dir, SHIELD_UP_SOUND))

    def events(self):
        keys = pg.key.get_pressed()
        if (keys[pg.K_LEFT] or keys[pg.K_q]) and self.rect.left > SCREEN_OFFSET and not self.hidden:
            self.speedx = -DEFAULT_PLAYER_SPEED

        if (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.rect.right < WIDTH - SCREEN_OFFSET and not self.hidden:
            self.speedx = DEFAULT_PLAYER_SPEED

        if keys[pg.K_SPACE] and not self.hidden:
            self.shoot()

    def update(self, *args):

        if self.hidden:
            self.image = self.blank_image
        elif not self.flashing:
            self.image = self.original_image

        self.speedx = 0

        self.events()

        self.rect.x += self.speedx

        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.renew()

        if self.flashing and pg.time.get_ticks() - self.hide_timer > 2000:
            self.flashing = False

        elif self.flashing and not self.hidden:
            if self.current_frame == 0:
                self.image = self.blank_image
                self.current_frame = 1
            else:
                self.image = self.original_image
                self.current_frame = 0

    def shoot(self):
        now = pg.time.get_ticks()

        if now - self.last_shot >= PLAYER_BURST_DELAY:
            self.shoot_number = 0

        if now - self.last_shot >= PLAYER_SHOOT_DELAY and self.shoot_number <= self.weapon:
            self.shoot_number += 1
            self.last_shot = now
            Laser(self.game, self.rect.centerx, self.rect.top)
            self.shot_sound.play()

    def hide(self):
        self.hidden = True
        self.flashing = True
        self.hide_timer = pg.time.get_ticks()

    def shield_up(self, amount):
        self.shield.power = min(self.shield.power + amount, 100)
        self.shield_up_sound.play()

    def life_up(self, amount):
        self.lives = min(MAX_PLAYER_LIVES, self.lives + amount)

    def weapon_up(self, type):
        self.weapon = min(self.weapon + type, MAX_WEAPON)

    def renew(self):
        self.hidden = False
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - SCREEN_OFFSET
        self.shield = Shield(self.game)
        self.shield_up(100)
        self.weapon = MIN_WEAPON
        self.untouchable_timer = pg.time.get_ticks()

    def apply_power_up(self, powerup):
        self.score += powerup.score
        self.weapon = min(self.weapon + powerup.weapon, MAX_WEAPON)
        self.lives = min(MAX_PLAYER_LIVES, self.lives + powerup.player_life)
        self.shield.power = min(self.shield.power + powerup.shield_power, 100)
        self.shield_up_sound.play()


class Laser(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.lasers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spritesheet.get_image(LASER_IMAGE)
        self.image = pg.transform.scale(self.image, (3 * self.image.get_rect().width // 3,
                                                     3 * self.image.get_rect().height // 3))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speedy = -LASER_SPEED
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self, *args):
        self.rect.y += self.speedy
        if self.rect.bottom < -SCREEN_OFFSET:
            self.kill()


class Meteor(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.meteors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(random.choice(METEOR_IMAGE_LIST))
        self.image.set_colorkey(BLACK)
        self.image_origin = self.image.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * .80 // 2
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(MIN_Y_SPAWN - self.rect.height, MAX_Y_SPAWN - self.rect.height)
        self.speedx = random.randrange(-METEOR_MAX_SPEED_X, METEOR_MAX_SPEED_X)
        self.speedy = random.randrange(METEOR_MIN_SPEED_Y, METEOR_MAX_SPEED_Y)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def update(self, *args):
        if self.rect.top >= HEIGHT + self.rect.height:
            self.kill()
        else:
            self.rect.centerx += self.speedx
            self.rect.centery += self.speedy
            self.rotate()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation += self.rotation_speed % 360
            new_image = pg.transform.rotate(self.image_origin, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Star(pg.sprite.Sprite):
    def __init__(self, game, x=None, y=None):
        self._layer = BACKGROUND_LAYER
        self.groups = game.all_sprites, game.background
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(random.choice(STAR_IMAGE_LIST))
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (int(1/2 * self.image.get_rect().width),
                                                     int(1/2 * self.image.get_rect().height)))
        alpha = random.randrange(30, 100)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH) if x is None else x
        self.rect.y = random.randrange(2 * MIN_Y_SPAWN - self.rect.height,
                                       MAX_Y_SPAWN - self.rect.height) if y is None else y

    def update(self, *args):
        self.rect.centery += BACKGROUND_SPEED
        if self.rect.top >= HEIGHT + self.rect.height:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, game, center):
        self.groups = game.all_sprites
        self._layer = EXPLOSION_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(EXPLOSION_IMAGE_LIST[0])
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 30
        self.sound = pg.mixer.Sound(path.join(self.game.snd_dir, EXPLOSION_SOUND))
        self.sound.set_volume(0.2)
        self.sound.play()

    def update(self, *args):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(EXPLOSION_IMAGE_LIST):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.spritesheet.get_image(EXPLOSION_IMAGE_LIST[self.frame])
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center


class Shield(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = SHIELD_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.power = 100
        self.image = self.game.spritesheet.get_image(SHIELD_IMAGE_LIST[2])
        self.image.set_colorkey(BLACK)
        self.alpha = 3
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center

    def update(self, *args):
        if self.power <= 0:
            self.kill()
        if self.power >= 75:
            level = 2
        elif self.power >= 40:
            level = 1
        else:
            level = 0
        self.image = self.game.spritesheet.get_image(SHIELD_IMAGE_LIST[level])
        self.image.set_colorkey(BLACK)
        self.image.set_alpha(self.alpha)
        self.rect.center = self.game.player.rect.center


class Power:
    def __init__(self, shield_power=0, player_life=0, weapon=0):
        self.shield_power = shield_power
        self.player_life = player_life
        self.weapon = weapon
        self.score = 200


class ShieldUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.power = Power(shield_power=75)
        if self.power.shield_power == 25:
            self.image = self.game.spritesheet.get_image('shield_bronze.png')
        elif self.power.shield_power == 50:
            self.image = self.game.spritesheet.get_image('shield_silver.png')
        elif self.power.shield_power == 75:
            self.image = self.game.spritesheet.get_image('shield_gold.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = POWER_SPEED

    def update(self, *args):
        self.rect.centery += self.speed


class WeaponUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.power = Power(weapon=1)
        self.image = self.game.spritesheet.get_image('bolt_gold.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = POWER_SPEED

    def update(self, *args):
        self.rect.centery += self.speed


class LifeUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.power = Power(player_life=1)
        self.image = self.game.spritesheet.get_image(PLAYER_LIFE_IMAGE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = POWER_SPEED

    def update(self, *args):
        self.rect.centery += self.speed

