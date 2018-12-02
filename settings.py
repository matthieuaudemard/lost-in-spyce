# colors definition
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (173, 230, 255)
PURPLE = (58, 46, 63)
ORANGE = (255,165,0)

# gui properties
WIDTH = 600
HEIGHT = 800
WINDOW_DIMENSION = (WIDTH, HEIGHT)
FPS = 60
TITLE = "LOST IN SpyCE 2.0"
FONT_THIN_NAME = 'kenvector_future_thin.ttf'
FONT_NAME = 'kenvector_future.ttf'
SPRITESHEET = 'sheet.png'
BGCOLOR = PURPLE

# game properties
LASER_SPEED = 20
DEFAULT_PLAYER_SPEED = 7
SCREEN_OFFSET = 10
PLAYER_SHOOT_DELAY = 175
PLAYER_BURST_DELAY = 750
PLAYER_SCALE = 3 / 4
MOB_NUMBER = 20
STAR_NUMBER = 20

START_PLAYER_LIVES = 2
MAX_PLAYER_LIVES = 3
MIN_WEAPON = 1
MAX_WEAPON = 2

MIN_Y_SPAWN = -100
MAX_Y_SPAWN = -40

METEOR_MAX_SPEED_X = 5
METEOR_MIN_SPEED_Y = 5
METEOR_MAX_SPEED_Y = 12

BACKGROUND_SPEED = 4

POWER_SPEED = 7

# layers
BACKGROUND_LAYER = 0
MOB_LAYER = BACKGROUND_LAYER + 1
PLAYER_LAYER = MOB_LAYER + 1
SHIELD_LAYER = PLAYER_LAYER + 1
EXPLOSION_LAYER = SHIELD_LAYER + 1

# sounds
LEVEL_MUSIC = 'level1.ogg'
START_MUSIC = 'intro.ogg'
GO_MUSIC = 'finished_long.ogg'
LASER_SOUND = 'laser4.ogg'
EXPLOSION_SOUND = 'explosion.ogg'
SHIELD_UP_SOUND = 'sfx_shieldUp.ogg'

# images
PLAYER_IMAGE = 'playerShip2_orange.png'
PLAYER_LIFE_IMAGE = 'playerLife2_orange.png'
LASER_IMAGE = 'laserRed16.png'
STAR_IMAGE_LIST = ['star{}.png'.format(i) for i in range(1, 4)]
METEOR_IMAGE_LIST = ['meteorBrown_big1.png',
                     'meteorBrown_big2.png',
                     'meteorBrown_big3.png',
                     'meteorBrown_big4.png',
                     'meteorBrown_med1.png',
                     'meteorBrown_med3.png',
                     'meteorBrown_small1.png',
                     'meteorBrown_small2.png',
                     'meteorBrown_tiny1.png',
                     'meteorBrown_tiny2.png',
                     'meteorGrey_big1.png',
                     'meteorGrey_big2.png',
                     'meteorGrey_big3.png',
                     'meteorGrey_big4.png',
                     'meteorGrey_med1.png',
                     'meteorGrey_med2.png',
                     'meteorGrey_small1.png',
                     'meteorGrey_small2.png',
                     'meteorGrey_tiny1.png',
                     'meteorGrey_tiny2.png', ]
EXPLOSION_IMAGE_LIST = ['laserRed11.png',
                        'laserRed10.png',
                        'laserRed09.png',
                        'laserRed08.png', ]
SHIELD_IMAGE_LIST = ['shield1.png',
                     'shield2.png',
                     'shield3.png', ]


# HUD constants
SHIELDBAR_X = 10
SHIELDBAR_Y = 35
BAR_LENGTH = 190
BAR_HEIGHT = 15
SCORE_LENGTH = 10
