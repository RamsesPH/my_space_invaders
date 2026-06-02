import pygame
import random

class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img_id = random.randint(1, 3)
        self.image = pygame.image.load(f"images/invader{img_id}.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class InvaderFormation:
    """
    Controls the entire block of invaders:
    - moves them as a unit
    - shifts down when changing direction
    - chooses attackers for shooting
    """
    def __init__(self, rows, cols, start_x=100, start_y=100,
                 x_spacing=60, y_spacing=40, screen_width=800):

        self.group = pygame.sprite.Group()
        self.move_direction = 1
        self.speed = 1.0
        self.screen_width = screen_width
        self.just_dropped = False   # prevents repeated drops

        # Create the block of invaders
        for row in range(rows):
            for col in range(cols):
                invader = Invader(start_x + col * x_spacing,
                                  start_y + row * y_spacing)
                self.group.add(invader)

    def update(self):
        # Move horizontally
        for inv in self.group:
            inv.rect.x += self.move_direction * self.speed

        # Boundary detection
        hit_right = any(inv.rect.right >= self.screen_width - 10 for inv in self.group)
        hit_left  = any(inv.rect.left <= 10 for inv in self.group)

        # Reverse + drop ONCE per boundary hit
        if (hit_right or hit_left) and not self.just_dropped:
            self.move_direction *= -1

            # Drop down
            for inv in self.group:
                inv.rect.y += 5

            # Push away from wall so they don't get stuck
            push = 5 if hit_right else -5
            for inv in self.group:
                inv.rect.x += push

            self.just_dropped = True

        # Reset drop flag when fully away from walls
        if not hit_right and not hit_left:
            self.just_dropped = False


    def draw(self, screen):
        self.group.draw(screen)

    def choose_attacker(self):
        """Pick a random invader from the block to shoot."""
        if len(self.group) == 0:
            return None
        return random.choice(self.group.sprites())
