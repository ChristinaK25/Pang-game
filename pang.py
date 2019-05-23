import sys
import math
from random import randrange
import pygame as pg
import self
import time
from pygame.sprite import Group

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
RED = (255, 0, 0)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720


class Ball(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(groups)
        self.image = pg.Surface((80, 80), pg.SRCALPHA)
        col = RED
        pg.draw.circle(self.image, col, (40, 40), 40)
        self.rect = self.image.get_rect(center=pos)
        self.vel = pg.math.Vector2(5, 0).rotate(randrange(360))
        self.pos = pg.math.Vector2(pos)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

        if self.rect.left < 10 or self.rect.right > 1170:
            self.vel.x *= -1
        if self.rect.top < 30 or self.rect.bottom > 650:
            self.vel.y *= -1

    def overlaps(self, other_rect):
        return self.rect.colliderect(other_rect)


class BallSmall(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(groups)
        self.image = pg.Surface((50, 50), pg.SRCALPHA)
        col = RED
        pg.draw.circle(self.image, col, (25, 25), 25)
        self.rect = self.image.get_rect(center=pos)
        self.vel = pg.math.Vector2(5, 0).rotate(randrange(360))
        self.pos = pg.math.Vector2(pos)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

        if self.rect.left < 10 or self.rect.right > 1170:
            self.vel.x *= -1
        if self.rect.top < 30 or self.rect.bottom > 650:
            self.vel.y *= -1

    def overlaps(self, other_rect):
        return self.rect.colliderect(other_rect)


class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.movex = 1
        self.movey = 0
        self.lives = 5
        self.images = []
        # load hero image
        player_image = pg.image.load("pangs1.png").convert()
        player_image.set_colorkey(GREEN)
        playerS_image = pg.image.load("pangsh3.png").convert()
        playerS_image.set_colorkey(GREEN)
        player_mini_img = pg.transform.scale(player_image, (30, 21))
        player_mini_img.set_colorkey(GREEN)
        self.images.append(player_image)
        self.images.append(playerS_image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def is_alive(self):
        return self.hp > 0

    def control(self, x, y):
        self.movex = x
        self.movey = y

    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        if self.rect.left < 0 or self.rect.right > 1200:
            self.rect.x = -self.rect.x
        if self.rect.top < 30 or self.rect.bottom > 650:
            self.rect.y = 500

    def attack(self):
        dmg = 1
        self.lives = self.lives - dmg


class Bullet(pg.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.images = []
        for i in range(1, 5):
            bullet_image = pg.image.load('bullet' + str(i) + '.png').convert()
            bullet_image.set_colorkey(GREEN)
            self.images.append(bullet_image)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 7


font_name = pg.font.match_font('Times New Roman')


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


pg.init()

screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
backdropbox = screen.get_rect()

pg.display.set_caption("My Game")

done = False
shoot = False
b = True

# Used to manage how fast the screen updates
clock = pg.time.Clock()

sprite_group = pg.sprite.Group()
ball = Ball((320, 240))
ball_list = pg.sprite.Group()
ballSmall_list = pg.sprite.Group()

ballSmall = BallSmall((320, 240))

# List of each bullet
bullet_list = pg.sprite.Group()

score = 0

# load intro
intro_image = pg.image.load("intro.png").convert()

# load start
start_image = pg.image.load("start.png").convert()

# load image bg
lvl1_image = pg.image.load("lvl1.jpg").convert()
lvl2_image = pg.image.load("lvl2.png").convert()

# lvl2 transition
trans2_image = pg.image.load("lvl2trans.png").convert()

# load image over
game_overI = pg.image.load("over.png").convert()

# load image won
won_image = pg.image.load("won.png").convert()

# load hero image shooting
playerS_image = pg.image.load("pangsh3.png").convert()
playerS_image.set_colorkey(GREEN)

# load hero image
player_image = pg.image.load("pangs1.png").convert()
player_image.set_colorkey(GREEN)

# lives
player_mini_img = pg.transform.scale(player_image, (30, 21))
player_mini_img.set_colorkey(GREEN)
# load sound
shot_sound = pg.mixer.Sound("shot.wav")
menu_music = pg.mixer.Sound("theme.wav")
win_sound = pg.mixer.Sound("win.wav")
loss_sound = pg.mixer.Sound("loss.wav")

# spawn player
player = Player()

# current hero pos
player.rect.x = 600
player.rect.y = 500
player_list = pg.sprite.Group()
player_list.add(player)

# how fast move
steps = 4

# initialisation of needed checks
hit = False
over = False
start = False
won = False
check = True

lvl1 = False
lvl2 = False

menu_music.play()
screen.blit(intro_image, [0, 0])
pg.display.flip()
time.sleep(3)
previous_time = pg.time.get_ticks()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    if not start:
        screen.blit(start_image, [0, 0])

    if event.type == pg.KEYDOWN:
        if event.key == ord("1"):
            start = True
            lvl1 = True
        elif event.key == ord("2"):
            done = True

    if start:
        if not won:


        # --- Game logic should go here
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == ord('a'):
                    player.control(-steps, 0)
                if event.key == pg.K_RIGHT or event.key == ord('d'):
                    player.control(steps, 0)
                if event.key == pg.K_UP or event.key == ord('w'):
                    shoot = True
                    shot_sound.play()

                    # Fire a bullet if the user uses keyup

                    current_time = pg.time.get_ticks()

                    if current_time - previous_time > 300:
                        previous_time = current_time
                        bullet = Bullet()

                    # Set the bullet so it is where the player is
                    bullet.rect.x = player.rect.x
                    bullet.rect.y = player.rect.y
                    # Add the bullet to the lists
                    sprite_group.add(bullet)
                    bullet_list.add(bullet)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == ord('a') or event.key == pg.K_RIGHT or event.key == ord('d') :
                    player.control(0, 0)
        # lvl 1
        if lvl1:
            while b:
                for i in range(0, 3):
                    ball_list.add(Ball((320, 240)))
                    sprite_group.add(ball_list)

                b = False

            sprite_group.update()
            ball.update()
            screen.blit(lvl1_image, [0, 0])

        # lvl 2
        elif lvl2:
            while b:
                for i in range(0, 6):
                    ball_list.add(Ball((320, 240)))
                    sprite_group.add(ball_list)

                b = False

            sprite_group.update()
            ball.update()
            screen.blit(lvl2_image, [0, 0])

        # lvl 3 placeholder

        for bullet in bullet_list:
            # See if it hit a block
            ball_hit_list = pg.sprite.spritecollide(bullet, ball_list, True)

            # For each block hit, remove the bullet and add to the score
            for ball in ball_hit_list:
                bullet_list.remove(bullet)
                sprite_group.remove(bullet)

                ballSmall_list.add(BallSmall((320, 240)))
                sprite_group.add(ballSmall_list)
                ballSmall_list.add(BallSmall((320, 240)))
                sprite_group.add(ballSmall_list)

                score += 1
                print("score=", score)

                # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                sprite_group.remove(bullet)

        for bullet in bullet_list:
            # See if it hit a block
            ballSmall_hit_list = pg.sprite.spritecollide(bullet, ballSmall_list, True)

            # For each block hit, remove the bullet and add to the score
            for ball in ballSmall_hit_list:
                bullet_list.remove(bullet)
                sprite_group.remove(bullet)

                score += 2
                print("score=", score)

                # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                sprite_group.remove(bullet)

        if pg.sprite.spritecollide(player, ball_list, False, pg.sprite.collide_mask) or pg.sprite.spritecollide(player,
                                                                                                                ballSmall_list,
                                                                                                                False,
                                                                                                                pg.sprite.collide_mask):
            hit = True

            if hit and count:
                player.attack()
                print("hp=", player.lives)
                if player.lives <= 0:
                    over = True
                if ball.rect.bottom > 500:
                    ball.vel.y *= -1
                count = False
        else:
            count = True

        if score == 15:
            lvl2 = True
            if lvl1:
                b = True
                screen.blit(trans2_image, [0, 0])
                pg.display.flip()
                time.sleep(2)
            lvl1 = False

        if score == 45:
            won = True
        if over:
            menu_music.stop()
            if check:
                loss_sound.play()
                check = False
            screen.blit(game_overI, [0, 0])
        elif won:
            menu_music.stop()
            if check:
                win_sound.play()
                check = False
            screen.blit(won_image, [0, 0])
        else:
            player.update()
            player_list.draw(screen)
            while shoot:
                if lvl1:
                    screen.blit(lvl1_image, [0, 0])
                elif lvl2:
                    screen.blit(lvl2_image, [0, 0])
                screen.blit(playerS_image, [player.rect.x, player.rect.y])
                shoot = False
            sprite_group.draw(screen)

        if not won:
            draw_lives(screen, SCREEN_WIDTH - 150, 5, player.lives, player_mini_img)
            draw_text(screen, str(score), 36, SCREEN_WIDTH / 2, 10)


    # --- Go ahead and update the screen with what we've drawn.
    pg.display.flip()

    # --- Limit to 60 frames per second

    clock.tick(60)

# Close the window and quit.
pg.quit()