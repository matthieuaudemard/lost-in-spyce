import sys

import tools
from sprites import *


class Game:
    def __init__(self):
        """
        creates new game object
        """
        pg.init()   # initialize pygame
        pg.mixer.init()  # initialize pygame mixer
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        self.snd_dir = path.join(self.dir, 'snd')
        self.fnt_dir = path.join(self.dir, 'fnt')
        self.running = True
        self.playing = False
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.mobs = pg.sprite.Group()
        self.lasers = pg.sprite.Group()
        self.meteors = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.powers = pg.sprite.Group()
        self.font_name = path.join(self.fnt_dir, FONT_THIN_NAME)
        self.score_font_name = path.join(self.fnt_dir, FONT_NAME)
        self.spritesheet = tools.Spritesheet(path.join(self.img_dir, SPRITESHEET))
        self.player = None
        self.shield = None
        self.death_explosion = None

    def new(self):
        """
        Creates and initialise a new game
        :return:
        """
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.lasers = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.meteors = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.powers = pg.sprite.Group()
        # creates new background with 20 stars
        while len(self.background) <= STAR_NUMBER:
            Star(self, y=random.randrange(0, HEIGHT))
        for y_position in MOB_INIT_POSITION_LIST:
            Meteor(self, y=y_position)
        self.player = Player(self)
        self.player.shield = Shield(self)
        self.death_explosion = None
        pg.mixer.music.load(path.join(self.snd_dir, LEVEL_MUSIC))
        pg.mixer.music.play(loops=-1)

    def run(self):
        """
        runs the game
        :return:
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """
        listen for events
        :return:
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

    def draw(self):
        """
        draws game elements
        :return:
        """
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_hud()
        pg.display.flip()

    def update(self):
        """
        check collisions and update shown elements on the screen
        :return:
        """
        self.check_collisions()

        # spawn new star
        while len(self.background) < 20:
            Star(self)

        # spawn new meteors
        while len(self.meteors) < MOB_NUMBER:
            Meteor(self)

        self.all_sprites.update()

    def check_mob_collisions(self):
        """
        check collision between player and mobs
        :return:
        """
        # stop checking if the player is hidden or flashing
        if self.player.flashing or self.player.hidden:
            return

        for hit in pg.sprite.spritecollide(self.player, self.mobs, True, pg.sprite.collide_circle):
            # updating player shield power
            if self.player.shield is not None and self.player.shield.power >= 0:
                self.player.shield.power -= hit.radius
                if self.player.shield.power < 0:
                    # if power < 0, triggers the player explosion (death explosion) at player position
                    # hides player
                    self.death_explosion = Explosion(self, self.player.rect.center)
                    self.player.hide()
                    self.player.lives -= 1
                else:
                    # if power >= 0 triggers explosion at hit center position
                    Explosion(self, hit.rect.center)

    def check_laser_collisions(self):
        """
        check collision between mobs and player shots
        :return:
        """
        for hit in pg.sprite.groupcollide(self.mobs, self.lasers, True, True):
            # creates a power-up
            if random.randrange(1000) < 50:
                power_type = random.choice(['shield', 'weapon', 'life'])
                if power_type == 'shield':
                    ShieldUp(self, hit.rect.centerx, hit.rect.centery)
                elif power_type == 'weapon':
                    WeaponUp(self, hit.rect.centerx, hit.rect.centery)
                elif power_type == 'life':
                    LifeUp(self, hit.rect.centerx, hit.rect.centery)
            Explosion(self, hit.rect.center)
            # update player score
            self.player.score += abs(100 - hit.radius * 2)

    def check_power_collisions(self):
        """
        check collision between player and power-up
        :return:
        """
        # stop checking if the player is hidden or flashing
        if self.player.flashing or self.player.hidden:
            return

        for hit in pg.sprite.spritecollide(self.player, self.powers, True):
            # update player characteristics
            self.player.apply_power_up(hit.power)
            hit.kill()

    def check_collisions(self):
        self.check_mob_collisions()

        if self.player.lives < 0 and self.death_explosion is not None and not self.death_explosion.alive():
            pg.mixer.music.stop()
            self.playing = False

        self.check_laser_collisions()

        self.check_power_collisions()

    def show_start_screen(self):
        """
        game start screen
        :return:
        """
        pg.mixer.music.load(path.join(self.snd_dir, START_MUSIC))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE.upper(), self.font_name, 45, WHITE, WIDTH // 2, HEIGHT // 4)
        self.draw_text('[Enter] to start / [Esc] to quit', self.font_name, 15, WHITE, WIDTH // 2, 2 * HEIGHT // 3)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        """
        game over / continue
        :return:
        """
        pg.mixer.music.load(path.join(self.snd_dir, GO_MUSIC))
        pg.mixer.music.play(loops=-1)
        self.draw_text(TITLE.upper(), self.font_name, 45, WHITE, WIDTH // 2, HEIGHT // 4)
        self.draw_text('[Enter] to start / [Esc] to quit', self.font_name, 15, WHITE, WIDTH // 2, 2 * HEIGHT // 3)
        pg.display.flip()
        self.wait_for_key()

    def draw_text(self, text, font_name, size, color, x, y):
        """
        draw text on the game surface at (x, y) position whith given color
        :param text: string to draw
        :param size: size of the text
        :param color: color of the text
        :param x: x coordinate of the text
        :param y: y coordiante of the text
        :return: None
        """
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_hud(self):
        self.draw_score()
        self.draw_shield_bar(SHIELDBAR_X, SHIELDBAR_Y)
        self.draw_player_lives()

    def draw_score(self):
        score_string = str(int(self.player.score)).rjust(SCORE_LENGTH, '0')
        for index, value in enumerate(score_string):
            image = self.spritesheet.get_image('numeral{}.png'.format(value))
            image.set_colorkey(BLACK)
            self.screen.blit(image, ((index * image.get_rect().width) + 10, 10))

    def draw_shield_bar(self, x, y):
        pct = int(self.player.shield.power) if self.player.shield.power >= 0.0 else 0
        fill = (pct / 100) * BAR_LENGTH
        color = GREEN
        if 40 < pct <= 55:
            color = YELLOW
        elif 20 < pct <= 40:
            color = ORANGE
        elif pct <= 20:
            color = RED
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Surface((fill, BAR_HEIGHT))
        fill_rect.set_alpha(120)
        fill_rect.fill(color)
        self.screen.blit(fill_rect, (x, y))
        pg.draw.rect(self.screen, WHITE, outline_rect, 2)

    def draw_player_lives(self):
        amount = self.spritesheet.get_image('numeral{}.png'.format(max(self.player.lives, 0)))
        amount.set_colorkey(BLACK)
        numeral_x = self.spritesheet.get_image('numeralX.png')
        numeral_x.set_colorkey(BLACK)
        image = self.spritesheet.get_image(PLAYER_LIFE_IMAGE)
        image = pg.transform.scale(image, (int(5/6 * image.get_rect().width),
                                           int(5/6 * image.get_rect().height)))
        image.set_colorkey(BLACK)
        self.screen.blit(image, (WIDTH - (image.get_rect().width + 10), 22))
        self.screen.blit(numeral_x, (WIDTH - 2 * (image.get_rect().width - 0.5), 26))
        self.screen.blit(amount, (WIDTH - 3 * (numeral_x.get_rect().width + 10), 24))

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        pg.event.post(pg.event.Event(pg.QUIT, {}))
                    elif event.key == pg.K_RETURN:
                        waiting = False
        pg.mixer.music.stop()
