# Pygame template
import pygame as pg
import random
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
mob_folder = os.path.join(img_folder, 'meteor')

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


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (100, 76))
        self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self, *args):
        self.speedx = 0
        keystate = pg.key.get_pressed()
        # Deplacement vers la gauche
        if keystate[pg.K_LEFT] and self.rect.left > 10:
            self.speedx = -12
        # Deplacement vers la droite
        if keystate[pg.K_RIGHT] and self.rect.right < WIDTH - 10:
            self.speedx = 12
        self.rect.x += self.speedx

    def shoot(self):
        bullet = Laser(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        lasers.add(bullet)


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = mob_list[random.randrange(0, len(mob_list))]
        self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self, *args):
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
        self.image = laser_img
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
background = pg.image.load(os.path.join(img_folder, 'corona_up.png')).convert()
background_rect = background.get_rect()
player_img = pg.image.load(os.path.join(img_folder, 'playerShip1_red.png')).convert()
mob_list = [pg.image.load(os.path.join(mob_folder, 'meteorBrown_big1.png')).convert(),
            pg.image.load(os.path.join(mob_folder, 'meteorBrown_med1.png')).convert(),
            pg.image.load(os.path.join(mob_folder, 'meteorBrown_med3.png')).convert(),
            pg.image.load(os.path.join(mob_folder, 'meteorBrown_small1.png')).convert(),
            pg.image.load(os.path.join(mob_folder, 'meteorBrown_small1.png')).convert(),
            pg.image.load(os.path.join(mob_folder, 'meteorBrown_small2.png')).convert(),
            pg.image.load(os.path.join(mob_folder, 'meteorBrown_small2.png')).convert(),
            pg.image.load(os.path.join(mob_folder, 'meteorBrown_tiny1.png')).convert(),
            pg.image.load(os.path.join(mob_folder, 'meteorBrown_tiny2.png')).convert(), ]
laser_img = pg.image.load(os.path.join(img_folder, 'laserBlue01.png')).convert()

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lasers = pg.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(40):
    mob = Mob()
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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Gestion des collisions
    # Destruction des lasers et mobs qui se touchent
    hits = pg.sprite.groupcollide(mobs, lasers, True, True)
    for hit in hits:
        mob = Mob()
        mobs.add(mob)
        all_sprites.add(mob)
    # On recupere la liste des mobs qui touchent le joueur
    hits = pg.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    # Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
