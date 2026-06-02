import pygame
from explosion import Explosion

class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/laser.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, invader_formation, invader_laser_group, explosion_group,
               explosion_sound_2, score_ref):
        self.rect.y -= 5

        if self.rect.bottom < 0:
            self.kill()
            return

        hit_list = pygame.sprite.spritecollide(self, invader_formation.group, True)
        if hit_list:
            self.kill()
            score_ref[0] += len(hit_list)
            explosion_sound_2.play()
            for hit in hit_list:
                explosion = Explosion(hit.rect.centerx, hit.rect.centery, 2)
                explosion_group.add(explosion)
            return

        if pygame.sprite.spritecollide(self, invader_laser_group, True):
            self.kill()


class AlienRounds(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/invader_laser.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, player_group, laser_group, bunker_group,
               explosion_group, explosion_sound_1, bunker_explosion_sound,
               lives_ref, screen_height):
        self.rect.y += 2

        if self.rect.top > screen_height:
            self.kill()
            return

        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            self.kill()
            lives_ref[0] -= 1
            explosion_sound_1.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            return

        if pygame.sprite.spritecollide(self, laser_group, True):
            self.kill()
            return

        if pygame.sprite.spritecollide(self, bunker_group, True):
            bunker_explosion_sound.play()
            self.kill()
