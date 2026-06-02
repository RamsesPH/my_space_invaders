# settings.py

import pygame

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (186, 74, 0)

# Game
ROWS = 5
COLS = 7
FPS = 60

# Invaders
INVADER_RECHARGE = 1200  # ms

# Fonts (initialized after pygame.init())
def load_fonts():
    font30 = pygame.font.SysFont('Courier New', 20)
    font40 = pygame.font.SysFont('Courier New', 40)
    return font30, font40
