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
explosion_folder = os.path.join(img_folder, 'explosion')

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
        self.image = player_imgs['default']
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
        self.image = player_imgs['default']
        self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        keystate = pg.key.get_pressed()
        # Gestion des tirs
        if keystate[pg.K_SPACE]:
            self.shoot()
        # Deplacement vers la gauche
        if keystate[pg.K_LEFT] and self.rect.left > 10:
            self.speedx = -5
            self.image = pg.transform.scale(player_imgs['left'], (90, 77))
            self.image.set_colorkey(BLACK)  # Permet de rendre le noir transparent
        # Deplacement vers la droite
        if keystate[pg.K_RIGHT] and self.rect.right < WIDTH - 10:
            self.speedx = 5
            self.image = pg.transform.scale(player_imgs['right'], (90, 77))
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
            all_sprites.add(shoot)
            lasers.add(shoot)


class Meteor(pg.sprite.Sprite):

    def __init__(self, size=None):
        pg.sprite.Sprite.__init__(self)
        if size is None:
            size = random.choice(['sm', 'sm', 'sm', 'md', 'md', 'lg'])
        self.size = size
        self.image = random.choice(meteor_imgs[size])
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
        if self.rect.top > HEIGHT + 2 * self.radius or self.rect.left < -2 * self.radius or self.rect.right > WIDTH + 25:
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


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 30

    def update(self, *args):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Ufo(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)


def new_meteor():
    meteor = Meteor()
    mobs.add(meteor)
    all_sprites.add(meteor)


# Graphics
background = pg.image.load(os.path.join(img_folder, 'texture.png')).convert()
background_rect = background.get_rect()
# Chargement des images du joueur
player_imgs = {'default': pg.image.load(os.path.join(ship_folder, 'player.png')).convert(),
               'left': pg.image.load(os.path.join(ship_folder, 'playerLeft.png')).convert(),
               'right': pg.image.load(os.path.join(ship_folder, 'playerRight.png')).convert(),
               'damaged': pg.image.load(os.path.join(ship_folder, 'playerDamaged.png')).convert(), }
# chargement des images des meteores
meteor_imgs = {'lg': [],
               'md': [],
               'sm': []}

img = pg.image.load(os.path.join(meteor_folder, 'meteor_lg.png')).convert()
img.set_colorkey(BLACK)
meteor_imgs['lg'].append(img)
for i in range(1, 3):
    filename = 'meteorBrown_med{}.png'.format(i)
    img = pg.image.load(os.path.join(meteor_folder, filename)).convert()
    img.set_colorkey(BLACK)
    meteor_imgs['md'].append(img)
for i in range(1, 2):
    filename = 'meteorBrown_small{}.png'.format(i)
    img = pg.image.load(os.path.join(meteor_folder, filename)).convert()
    img.set_colorkey(BLACK)
    meteor_imgs['sm'].append(img)
# chargement des images des lasers
laser_img_list = [pg.image.load(os.path.join(laser_folder, 'laserGreen.png')).convert(),
                  pg.image.load(os.path.join(laser_folder, 'laserRed.png')).convert(),
                  pg.image.load(os.path.join(laser_folder, 'laserBlue07.png')).convert(), ]
# chargemenr des images des nombres
numeral_list = []
for i in range(10):
    filename = 'numeral{}.png'.format(i)
    img = pg.image.load(os.path.join(numeral_folder, filename)).convert()
    img.set_colorkey(BLACK)
    numeral_list.append(img)
# Chargement des images des animations
explosion_anim = {'lg': [], 'sm': []}

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(os.path.join(explosion_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)


all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lasers = pg.sprite.Group()
player = Player()
player2 = Player()
all_sprites.add(player)
for i in range(5):
    new_meteor()

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
        if hit.size == 'lg':
            meteor_size = 'md'
            mob1 = Meteor(meteor_size)
            mob1.rect.x = hit.rect.centerx - 5
            mob1.rect.y = hit.rect.centery
            mob1.speedx = -4
            mob1.speedy = 4
            mobs.add(mob1)
            mob2 = Meteor(meteor_size)
            mob2.rect.x = hit.rect.centerx + 5
            mob2.rect.y = hit.rect.centery
            mob2.speedx = 4
            mob2.speedy = 4
            mobs.add(mob2)
            all_sprites.add(mob1)
            all_sprites.add(mob2)
        else:
            new_meteor()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
    # On recupere la liste des mobs qui touchent le joueur
    hits = pg.sprite.spritecollide(player, mobs, False, pg.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'sm')
        hit.kill()
        all_sprites.add(expl)
        mob = Meteor()
        mobs.add(mob)
        all_sprites.add(mob)
        #running = False


    # Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 28, WIDTH / 2, 10)
    pg.display.flip()

pg.quit()
