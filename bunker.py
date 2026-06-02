# bunker.py

import pygame
from settings import BROWN

class Bunker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([6, 6])
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def create_bunkers():
    bunker_group = pygame.sprite.Group()
    for bunk in range(4):
        for row in range(9):
            for column in range(15):
                x = (50 + (190 * bunk)) + 7 * column
                y = 390 + (7 * row)
                bunker = Bunker(x, y)
                bunker_group.add(bunker)
    return bunker_group
