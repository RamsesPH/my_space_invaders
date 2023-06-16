import pygame
from pygame import mixer
import random

# pygame needs to be initialized
pygame.init()

# define fps
clock = pygame.time.Clock()
fps = 60

#Define Variables
rows = 5
cols = 7
white = (255, 255, 255)
green = (0, 255, 0)
brown = (186, 74, 0)
score = 0
lives = 3
invader_recharge = 1200
last_invader_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()

# creates the screen and set the size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

# define fonts
font30 = pygame.font.SysFont('Courier New', 20)
font40 = pygame.font.SysFont('Courier New', 40)

# mixer initialization 1st call pre_init before the init
pygame.mixer.pre_init(frequency=44100, size=-16, channels=4, buffer=512)
mixer.init()

# load sound effects
explosion_sound_1 = pygame.mixer.Sound("sounds/explosion.wav")
explosion_sound_1.set_volume(0.40)

explosion_sound_2 = pygame.mixer.Sound("sounds/explosion2.wav")
explosion_sound_2.set_volume(0.40)

laser_sound = pygame.mixer.Sound("sounds/laser.wav")
laser_sound.set_volume(0.25)

bunker_explosion = pygame.mixer.Sound('sounds/invaderkilled.wav')
bunker_explosion.set_volume(0.25)


# <!--------------------- classes ----------------->


# create the Spaceship Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)          # inherits functionality of Sprite class
        self.image = pygame.image.load('images/player2.png')
        self.rect = self.image.get_rect()            # convert the image into a rectangle
        self.rect.center = [x, y]                    # position coordinates of rect
        self.last_shot = pygame.time.get_ticks()     # when laser beam was spawned
        self.mask = pygame.mask.from_surface(self.image)  # update mask

    def update(self):
        # create a movement increment
        increment = 7
        #key event key control
        key = pygame.key.get_pressed()
        # recharge_time for laser ready
        recharge_time = 400  # time in mile-seconds
        # record current time
        time_now = pygame.time.get_ticks()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= increment
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += increment
        if key[pygame.K_SPACE] and time_now - self.last_shot > recharge_time:
            laser_sound.play()
            laser = LaserBeam(self.rect.centerx, self.rect.top)
            laserBeam_group.add(laser)
            self.last_shot = time_now

class Bunker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([6, 6])
        self.image.fill(brown)
        self.rect = self.image.get_rect()

# # laser class
class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/laser.png')
        self.rect = self.image.get_rect()                   # fit img into rectangle
        self.rect.center = [x, y]

    def update(self):
        global score
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()          # delete laser beam once it leaves the screen
        if pygame.sprite.spritecollide(self, invader_group, True):
            self.kill()         # laser beam disappears once it kills the invader
            score += 1
            explosion_sound_2.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            self.kill()
        if pygame.sprite.spritecollide(self, invader_laser_group, True):
            self.kill()

# # create Invader class
class Invaders(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/invader" + str(random.randint(1, 3)) + ".png")
        self.rect = self.image.get_rect()   # convert img into rectangle
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 80:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

# Alien_Rounds class
class AlienRounds(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # inherits the functionality of class pygame.sprite.Sprite
        self.image = pygame.image.load('images/invader_laser.png')
        self.rect = self.image.get_rect()  # fit img into rectangle
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)  # Generate mask for the sprite

    def update(self):
        global lives
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()  # that is to delete bullet once it leaves the screen
        # pygame.sprite.collide() is provided by the pygame library for sprite groups
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            self.kill()
            lives -= 1
            explosion_sound_1.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
        if pygame.sprite.spritecollide(self, laserBeam_group, True):
            self.kill()
        if pygame.sprite.spritecollide(self, bunker_list, True,):
            bunker_explosion.play()
            self.kill()


# create explosions class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 9):
            img = pygame.image.load(f"images/Explosion{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (150, 150))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

#create sprite groups
player_group = pygame.sprite.Group()
laserBeam_group = pygame.sprite.Group()
invader_group = pygame.sprite.Group()
invader_laser_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
bunker_list = pygame.sprite.Group()

def create_invaders():
    # generate invaders
    for row in range(rows):
        for item in range(cols):
            invader = Invaders(100 + item * 100, 100 + row * 50)
            invader_group.add(invader)

def create_bunker():
    for bunk in range(4):
        for row in range(9):
            for column in range(15):
                bunker = Bunker()
                bunker.rect.x = (50 + (190 * bunk)) + 7 * column
                bunker.rect.y = 390 + (7 * row)
                bunker_list.add(bunker)


#Create the text used to display the score and draw it on the screen
def draw_score():
    # Game Title Section
    global score
    text = font30.render("Pedro's Invaders", True, white)
    text_rect = text.get_rect()
    text_rect.center = (screen_width / 2, 25)
    screen.blit(text, text_rect)
    # Score Section
    text1 = font30.render(f"Score: {score}", False, white)
    text_rect1 = text1.get_rect()
    text_rect1.center = (650, 25)
    screen.blit(text1, text_rect1)
    #lives section
    text3 = font30.render(f"Lives left : {lives}", False, white)
    text_rect3 = text3.get_rect()
    text_rect3.center = (100, 25)
    screen.blit(text3, text_rect3)

##create sprites
create_invaders()
create_bunker()
##create a player
player = Player(int(screen_width/2), screen_height - 90)
player_group.add(player)  # instance created is added to the group


# <! -------------- GAME LOOP ------------------>

background = pygame.image.load('images/bg.png')
game_on = True
while game_on:

    clock.tick(fps)

    # draw background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # update
    draw_score()
    player.update()
    invader_group.update()
    laserBeam_group.update()
    invader_laser_group.update()
    explosion_group.update()
    bunker_list.update()

    # Draw sprite groups
    player_group.draw(screen)
    invader_group.draw(screen)
    laserBeam_group.draw(screen)
    invader_laser_group.draw(screen)
    explosion_group.draw(screen)
    bunker_list.draw(screen)

    # creating invaders laser instance
    now_time = pygame.time.get_ticks()
    if now_time - last_invader_shot > invader_recharge and len(invader_laser_group) < 3 and len(invader_group) > 0:
        attacker = random.choice(invader_group.sprites())
        invader_laser = AlienRounds(attacker.rect.centerx, attacker.rect.bottom)
        invader_laser_group.add(invader_laser)
        last_invader_shot = now_time

    # score keeper & lives keeper
    if score == 35 or lives == 0:
        text2 = font40.render("GAME OVER", True, white)
        textRect2 = text2.get_rect()
        textRect2.center = (screen_width / 2, 250)
        screen.blit(text2, textRect2)
        # game_on = False

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

    # update  the screen
    pygame.display.update()

pygame.quit()
