# assets.py

import pygame
from pygame import mixer

def init_audio():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=4, buffer=512)
    mixer.init()

def load_images():
    images = {}
    images["player"] = pygame.image.load('images/player2.png')
    images["laser"] = pygame.image.load('images/laser.png')
    images["invader_laser"] = pygame.image.load('images/invader_laser.png')
    images["background"] = pygame.image.load('images/bg.png')
    images["explosions"] = [
        pygame.image.load(f"images/Explosion{num}.png") for num in range(1, 9)
    ]
    # invader variants will be loaded in invaders.py
    return images

def load_sounds():
    sounds = {}
    sounds["explosion1"] = pygame.mixer.Sound("sounds/explosion.wav")
    sounds["explosion1"].set_volume(0.40)

    sounds["explosion2"] = pygame.mixer.Sound("sounds/explosion2.wav")
    sounds["explosion2"].set_volume(0.40)

    sounds["laser"] = pygame.mixer.Sound("sounds/laser.wav")
    sounds["laser"].set_volume(0.25)

    sounds["bunker_explosion"] = pygame.mixer.Sound('sounds/invaderkilled.wav')
    sounds["bunker_explosion"].set_volume(0.25)

   # --- Alien march sounds (correctly added to dictionary) ---
    sounds["march1"] = pygame.mixer.Sound("sounds/step1.wav")
    sounds["march2"] = pygame.mixer.Sound("sounds/step2.wav")
    sounds["march3"] = pygame.mixer.Sound("sounds/step3.wav")
    sounds["march4"] = pygame.mixer.Sound("sounds/step4.wav")


    return sounds
