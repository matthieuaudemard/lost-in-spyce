# Pygame template
import pygame as pg
import random
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
ship_folder = os.path.join(img_folder, 'ship')
meteor_folder = os.path.join(img_folder, 'meteor')
laser_folder = os.path.join(img_folder, 'laser')
numeral_folder = os.path.join(img_folder, 'numeral')

WIDTH = 600
HEIGHT = 800
WINDOW_DIMENSION = (WIDTH, HEIGHT)
FPS = 60
TITLE = "py SHOOT"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialisation pygame et creation de la fenetre
pg.init()
pg.mixer.init()
screen = pg.display.set_mode(WINDOW_DIMENSION)
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

font_name = pg.font.match_font('times')
score = 0


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img_list[0], (99, 75))
        self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .80 / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()

    def update(self, *args):
        self.speedx = 0
        self.speedy = 0
        self.image = player_img_list[0]
        self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        keystate = pg.key.get_pressed()
        # Gestion des tirs
        if keystate[pg.K_SPACE]:
            self.shoot()
        # Deplacement vers la gauche
        if keystate[pg.K_LEFT] and self.rect.left > 10:
            self.speedx = -5
            self.image = pg.transform.scale(player_img_list[1], (90, 77))
            self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        # Deplacement vers la droite
        if keystate[pg.K_RIGHT] and self.rect.right < WIDTH - 10:
            self.speedx = 5
            self.image = pg.transform.scale(player_img_list[2], (90, 77))
            self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        self.rect.x += self.speedx
        # Deplacement vers le haut
        if keystate[pg.K_UP] and self.rect.top > 10:
            self.speedy = -5
        # Deplacement vers le bas
        if keystate[pg.K_DOWN] and self.rect.bottom < HEIGHT - 10:
            self.speedy = 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            shoot = Laser(self.rect.centerx, self.rect.top)
            shoot2 = Laser(self.rect.left, self.rect.top)
            all_sprites.add(shoot)
            lasers.add(shoot)


class Meteor(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = random.choice(meteor_img_list)
        self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .80 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot += self.rot_speed % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self, *args):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < - 25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)


class Laser(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = laser_img_list[2]
        self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self, *args):
        self.rect.y += self.speedy
        # Destruction si il depasse le haut de la fenetre
        if self.rect.bottom < 0:
            self.kill()


# Graphics
background = pg.image.load(os.path.join(img_folder, 'texture.png')).convert()
background_rect = background.get_rect()
player_img_list = [pg.image.load(os.path.join(ship_folder, 'player.png')).convert(),
                   pg.image.load(os.path.join(ship_folder, 'playerLeft.png')).convert(),
                   pg.image.load(os.path.join(ship_folder, 'playerRight.png')).convert(),
                   pg.image.load(os.path.join(ship_folder, 'playerDamaged.png')).convert(), ]
meteor_img_list = [pg.image.load(os.path.join(meteor_folder, 'meteorBig.png')).convert(),
                   pg.image.load(os.path.join(meteor_folder, 'meteorSmall.png')).convert(),
                   pg.image.load(os.path.join(meteor_folder, 'meteorBrown_med1.png')).convert(),
                   pg.image.load(os.path.join(meteor_folder, 'meteorBrown_med3.png')).convert(),
                   pg.image.load(os.path.join(meteor_folder, 'meteorSmall.png')).convert(),
                   pg.image.load(os.path.join(meteor_folder, 'meteorBrown_small1.png')).convert(),
                   pg.image.load(os.path.join(meteor_folder, 'meteorBrown_small2.png')).convert(), ]
laser_img_list = [pg.image.load(os.path.join(laser_folder, 'laserGreen.png')).convert(),
                  pg.image.load(os.path.join(laser_folder, 'laserRed.png')).convert(),
                  pg.image.load(os.path.join(laser_folder, 'laserBlue07.png')).convert(), ]
numeral_list = [pg.image.load(os.path.join(numeral_folder, 'numeral0.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral1.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral2.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral3.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral4.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral5.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral6.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral7.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral8.png')).convert(),
                pg.image.load(os.path.join(numeral_folder, 'numeral9.png')).convert(), ]

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lasers = pg.sprite.Group()
player = Player()
player2 = Player()
all_sprites.add(player)
for i in range(20):
    mob = Meteor()
    all_sprites.add(mob)
    mobs.add(mob)

# Game loop
running = True
while running:
    clock.tick(FPS)
    # Events
    for event in pg.event.get():
        # Fermeture de la fenetre
        if event.type == pg.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Gestion des collisions
    # Destruction des lasers et mobs qui se touchent
    hits = pg.sprite.groupcollide(mobs, lasers, True, True)
    for hit in hits:
        score += 56 - hit.radius
        mob = Meteor()
        mobs.add(mob)
        all_sprites.add(mob)
    # On recupere la liste des mobs qui touchen t le joueur
    hits = pg.sprite.spritecollide(player, mobs, False, pg.sprite.collide_circle)
    if hits:
        running = False

    # Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 28, WIDTH / 2, 10)
    pg.display.flip()

pg.quit()
