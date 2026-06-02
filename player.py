# player.py

import pygame
from laser import LaserBeam

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, laser_group, laser_sound, screen_width):
        super().__init__()
        self.image = pygame.image.load('images/player2.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)
        self.laser_group = laser_group
        self.laser_sound = laser_sound
        self.screen_width = screen_width

    def update(self):
        increment = 7
        key = pygame.key.get_pressed()
        recharge_time = 400
        time_now = pygame.time.get_ticks()

        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= increment
        if key[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += increment
        if key[pygame.K_SPACE] and time_now - self.last_shot > recharge_time:
            self.shoot(time_now)

    def shoot(self, time_now):
        self.laser_sound.play()
        laser = LaserBeam(self.rect.centerx, self.rect.top - 10)
        self.laser_group.add(laser)
        self.last_shot = time_now
