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
explosion_folder = os.path.join(img_folder, 'effect')
powerup_folder = os.path.join(img_folder, 'powerup')
effect_folder = os.path.join(img_folder, 'effect')

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
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .80 / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.gun_type = 1

    def update(self, *args):
        self.speedx = 0
        self.speedy = 0
        self.image = player_imgs['default']
        keystate = pg.key.get_pressed()
        # Gestion des tirs
        if keystate[pg.K_SPACE]:
            self.shoot()
        # Deplacement vers la gauche
        if keystate[pg.K_LEFT] and self.rect.left > 10:
            self.speedx = -5
            self.image = pg.transform.scale(player_imgs['left'], (90, 77))
        # Deplacement vers la droite
        if keystate[pg.K_RIGHT] and self.rect.right < WIDTH - 10:
            self.speedx = 5
            self.image = pg.transform.scale(player_imgs['right'], (90, 77))
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
            if self.gun_type > 1:
                shoot1 = Laser(self.rect.left, self.rect.top + 30)
                all_sprites.add(shoot1)
                lasers.add(shoot1)
                shoot2 = Laser(self.rect.right, self.rect.top + 30)
                all_sprites.add(shoot2)
                lasers.add(shoot2)

    def power_up(self):
        if self.gun_type < 3:
            self.gun_type += 1


class Meteor(pg.sprite.Sprite):

    def __init__(self, size=None, center=None, speed=None):
        pg.sprite.Sprite.__init__(self)
        if size is None:
            size = random.choice(['sm', 'sm', 'sm', 'md', 'md', 'lg'])
        self.size = size
        self.image = random.choice(meteor_imgs[self.size])
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .80 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width) if center is None else center[0]
        self.rect.y = random.randrange(-100, -40) if center is None else center[1]
        self.speedx = random.randrange(-3, 3) if speed is None else speed[0]
        self.speedy = random.randrange(1, 8) if speed is None else speed[1]
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
        # Si un meteore sors du cadre on le repositionne et on lui change sa vitesse et sa taille
        if self.rect.top > HEIGHT + 2 * self.radius \
                or self.rect.left < -2 * self.radius \
                or self.rect.right > WIDTH + 25:
            # definition de sa position initiale
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            # definition de sa vitesse
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)
            # definition de sa taille et de son image
            self.size = random.choice(['sm', 'sm', 'sm', 'md', 'md', 'lg'])
            self.image = random.choice(meteor_imgs[self.size])


class Laser(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = laser_imgs[1]
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


class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(list(power_imgs.keys()))
        self.image = power_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self, *args):
        self.rect.y += self.speedy
        # On detruit le powerup s'il depasse l'ecran
        if self.rect.top > HEIGHT:
            self.kill()


class ScoreNumeral(pg.sprite.Sprite):
    def __init__(self, numeral_string, x, y):
        pg.sprite.Sprite.__init__(self)
        if int(numeral_string) in range(9):
            self.image = numeral_imgs[int(numeral_string)]
        else:
            self.image = numeral_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x


def new_meteor(size=None, center=None, speed=None):
    meteor = Meteor(size, center, speed)
    mobs.add(meteor)
    all_sprites.add(meteor)


def show_gameover():
    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.blit(background_img, background_rect)
        # Gestion des messages a afficher
        draw_text(screen, "py SHOOT!", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "Arrow keys to move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Press Return to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
        # Gestion du curseur
        cursor_rect = cursor_img.get_rect()
        cursor_rect.center = pg.mouse.get_pos()
        screen.blit(cursor_img, cursor_rect)
        pg.display.flip()
        for e in pg.event.get():
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                waiting = False
                pg.event.post(pg.event.Event(pg.QUIT))
            if e.type == pg.KEYUP and e.key == pg.K_RETURN:
                waiting = False


def draw_score(score_to_draw):
    score_string = str(score_to_draw)
    score_string = ('0' * (len(score_sprites) - len(score_string))) + score_string
    score_len = len(score_sprites) - 1

    for score_char in score_string[::-1]:
        score_sprites[score_len].image = numeral_imgs[int(score_char)]
        score_len -= 1


# Graphics
background_img = pg.image.load(os.path.join(img_folder, 'texture.png')).convert()
background_rect = background_img.get_rect()
# Chargement des images du joueur
player_imgs = {'default': pg.image.load(os.path.join(ship_folder, 'player.png')).convert_alpha(),
               'left': pg.image.load(os.path.join(ship_folder, 'playerLeft.png')).convert_alpha(),
               'right': pg.image.load(os.path.join(ship_folder, 'playerRight.png')).convert_alpha(),
               'damaged': pg.image.load(os.path.join(ship_folder, 'playerDamaged.png')).convert_alpha(), }

# chargement des images des meteores
meteor_imgs = {'lg': [pg.image.load(os.path.join(meteor_folder, 'meteor_lg.png')).convert_alpha()],
               'md': [],
               'sm': []}

for i in range(1, 3):
    filename = 'meteorBrown_med{}.png'.format(i)
    img = pg.image.load(os.path.join(meteor_folder, filename)).convert_alpha()
    meteor_imgs['md'].append(img)
for i in range(1, 2):
    filename = 'meteorBrown_small{}.png'.format(i)
    img = pg.image.load(os.path.join(meteor_folder, filename)).convert_alpha()
    meteor_imgs['sm'].append(img)
# chargement des images des lasers
laser_imgs = [pg.image.load(os.path.join(laser_folder, 'laserGreen.png')).convert_alpha(),
              pg.image.load(os.path.join(laser_folder, 'laserRed.png')).convert_alpha(),
              pg.image.load(os.path.join(laser_folder, 'laserBlue07.png')).convert_alpha(), ]
# chargemenr des images des nombres
numeral_imgs = []
for i in range(10):
    numeral_imgs.append(pg.image.load(os.path.join(numeral_folder, 'numeral{}.png'.format(i))).convert_alpha())
numeral_imgs.append(pg.image.load(os.path.join(numeral_folder, 'numeralX.png')).convert_alpha())
# Chargement des images des animations
explosion_anim = {'lg': [], 'sm': []}
for i in range(9):
    img = pg.image.load(os.path.join(explosion_folder, 'regularExplosion0{}.png'.format(i))).convert_alpha()
    explosion_anim['lg'].append(pg.transform.scale(img, (75, 75)))
    explosion_anim['sm'].append(pg.transform.scale(img, (32, 32)))

power_imgs = {'gun': pg.image.load(os.path.join(powerup_folder, 'gun.png')).convert_alpha()}

cursor_img = pg.image.load(os.path.join(ship_folder, 'cursor.png')).convert_alpha()

effect_imgs = {'booster': []}
for i in range(14, 16):
    booster_img = pg.image.load(os.path.join(effect_folder, 'fire{}.png'.format(i))).convert_alpha()
    effect_imgs['booster'].append(booster_img)

img_life = pg.image.load(os.path.join(ship_folder, 'life.png')).convert_alpha()

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lasers = pg.sprite.Group()
player = Player()
all_sprites.add(player)
power_sprites = pg.sprite.Group()

# Game loop
running = True
game_over = True

while running:
    pg.mouse.set_visible(False)
    if game_over:
        show_gameover()
        game_over = False
        all_sprites = pg.sprite.Group()
        # Creation du score
        score_sprites = []
        for i in range(9):
            score_sprite = ScoreNumeral(0, 20 * i + 20, 30)
            score_sprites.append(score_sprite)
            all_sprites.add(score_sprite)
        mobs = pg.sprite.Group()
        lasers = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(5):
            new_meteor()
        score = 0

    clock.tick(FPS)
    # Events
    for event in pg.event.get():
        # Fermeture de la fenetre
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False

    # Update
    all_sprites.update()

    # Gestion des collisions
    # Destruction des lasers et mobs qui se touchent
    hits = pg.sprite.groupcollide(mobs, lasers, True, True)
    for hit in hits:
        score += 20 if hit.size == 'sm' else 10 if hit.size == 'md' else 1
        if hit.size == 'lg':
            # Creation du meteore de gauche quand un meteore de taille 'lg' est detruit
            new_meteor('md', (hit.rect.centerx - 5, hit.rect.centery), (-4, 4))
            # Creation du meteore de droite quand un meteore de taille 'lg' est detruit
            new_meteor('md', (hit.rect.centerx + 5, hit.rect.centery), (4, 4))
            if random.random() >= 0.9:
                powup = Pow(hit.rect.center)
                all_sprites.add(powup)
                power_sprites.add(powup)
        else:
            new_meteor()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)

    # On recupere la liste des powers up qui touchent le joueur
    hits = pg.sprite.spritecollide(player, power_sprites, False, pg.sprite.collide_circle)
    for hit in hits:
        hit.kill()
        player.power_up()

    # On recupere la liste des mobs qui touchent le joueur
    hits = pg.sprite.spritecollide(player, mobs, False, pg.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'sm')
        hit.kill()
        all_sprites.add(expl)
        mob = Meteor()
        mobs.add(mob)
        all_sprites.add(mob)
        game_over = True

    # Render
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    # draw_text(screen, str(score), 28, WIDTH / 2, 10)
    draw_score(score)
    pg.display.flip()

pg.quit()
