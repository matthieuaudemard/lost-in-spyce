# Pygame template
import pygame as pg
import random


WIDTH = 480
HEIGHT = 600
WINDOW_DIMENSION = (WIDTH, HEIGHT)
FPS = 60
TITLE = "py SHOOT"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialisation pygame et creation de la fenetre
pg.init()
pg.mixer.init()
screen = pg.display.set_mode(WINDOW_DIMENSION)
pg.display.set_caption(TITLE)
clock = pg.time.Clock()


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((98, 75))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self, *args):
        self.speedx = 0
        keystate = pg.key.get_pressed()
        # Deplacement vers la gauche
        if keystate[pg.K_LEFT] and self.rect.left > 10:
            self.speedx = -8
        # Deplacement vers la droite
        if keystate[pg.K_RIGHT] and self.rect.right < WIDTH - 10:
            self.speedx = 8
        self.rect.x += self.speedx


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface
        self.image = pg.Surface((33, 26))
        self.image.fill(RED)
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


all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
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
    # Update

    # Render
    screen.fill(BLACK)
    all_sprites.update()
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
