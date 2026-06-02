import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ROWS, COLS, WHITE, INVADER_RECHARGE, load_fonts
from assets import init_audio, load_images, load_sounds
from player import Player
from invaders import InvaderFormation
from laser import LaserBeam, AlienRounds
from bunker import create_bunkers
from explosion import Explosion

game_state = "playing"   # "playing", "won", "lost"


def show_end_overlay(screen, state, score, font):
    """Overlay win/lose text on top of the existing background."""
    if state == "won":
        title = font.render("YOU SAVED EARTH!", True, (0, 255, 0))
    else:
        title = font.render("EARTH HAS FALLEN...", True, (255, 0, 0))

    option1 = font.render("1 - Restart", True, (255, 255, 255))
    option2 = font.render("2 - Quit", True, (255, 255, 255))

    # Draw text centered on screen WITHOUT clearing background
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 250))
    # Perfect alignment for menu options

    menu_x = SCREEN_WIDTH // 2 - 80   # adjust this number left/right

    screen.blit(option1, (menu_x, 330))
    screen.blit(option2, (menu_x, 380))


    pygame.display.update()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    reset_game()
                    waiting = False
                elif event.key == pygame.K_2:
                    pygame.quit()
                    exit()


def reset_game():
    """Reset the game to initial state."""
    global formation, player, lives, score, game_state

    lives[0] = 3
    score[0] = 0
    game_state = "playing"

    formation = InvaderFormation(ROWS, COLS)
    player.rect.centerx = SCREEN_WIDTH // 2


def main():
    global formation, player, lives, score, game_state

    pygame.init()
    init_audio()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()

    font30, font40 = load_fonts()
    images = load_images()
    sounds = load_sounds()

    # Alien march sound setup
    march_sounds = [
        sounds["march1"],
        sounds["march2"],
        sounds["march3"],
        sounds["march4"]
    ]

    march_index = 0
    last_march_time = pygame.time.get_ticks()
    march_delay = 600   # start slow


    # Game state
    score = [0]
    lives = [3]
    last_invader_shot = pygame.time.get_ticks()

    # Sprite groups
    player_group = pygame.sprite.Group()
    laser_group = pygame.sprite.Group()
    invader_laser_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    bunker_group = create_bunkers()

    # Entities
    formation = InvaderFormation(ROWS, COLS)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90,
                    laser_group, sounds["laser"], SCREEN_WIDTH)
    player_group.add(player)

    background = images["background"]
    game_on = True

    while game_on:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

        # UPDATE
        player_group.update()
        formation.update()

        # Speed up invaders as they die
        remaining = len(formation.group)
        formation.speed = max(0.5, 3 - remaining * 0.03)

        # Speed up invaders as they die
        remaining = len(formation.group)
        formation.speed = max(1, 6 - remaining * 0.05)

        # Speed up marching sound
        #march_delay = max(80, remaining * 8)
        march_delay = max(200, remaining * 15)

        # Alien marching sound loop
        now = pygame.time.get_ticks()
        if now - last_march_time > march_delay:
            march_sounds[march_index].play()
            march_index = (march_index + 1) % 4
            last_march_time = now


        # WIN CONDITION
        if len(formation.group) == 0:
            game_state = "won"

        # LOSE CONDITION: no lives
        if lives[0] <= 0:
            game_state = "lost"

        # LOSE CONDITION: invaders reached the ground
        for inv in formation.group:
            if inv.rect.bottom >= SCREEN_HEIGHT - 100:
                game_state = "lost"
                break

        # If game ended, show overlay and freeze gameplay
        if game_state != "playing":
            show_end_overlay(screen, game_state, score, font40)
            continue

        # Laser updates
        #laser_group.update()
        for laser in laser_group.sprites():
            laser.update(formation, invader_laser_group, explosion_group,
                         sounds["explosion2"], score)

        for alien_laser in invader_laser_group.sprites():
            alien_laser.update(player_group, laser_group, bunker_group,
                               explosion_group, sounds["explosion1"],
                               sounds["bunker_explosion"], lives, SCREEN_HEIGHT)

        explosion_group.update()

        # Invader shooting
        now_time = pygame.time.get_ticks()
        if (now_time - last_invader_shot > INVADER_RECHARGE
                and len(invader_laser_group) < 3
                and len(formation.group) > 0):
            attacker = formation.choose_attacker()
            if attacker:
                invader_laser = AlienRounds(attacker.rect.centerx, attacker.rect.bottom)
                invader_laser_group.add(invader_laser)
                last_invader_shot = now_time

        # DRAW
        screen.blit(background, (0, 0))

        # HUD
        text = font30.render("Pedro's Invaders", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 25))
        screen.blit(text, text_rect)

        text1 = font30.render(f"Score: {score[0]}", True, WHITE)
        screen.blit(text1, (650 - text1.get_width() // 2, 15))

        text3 = font30.render(f"Lives left : {lives[0]}", True, WHITE)
        screen.blit(text3, (100 - text3.get_width() // 2, 15))

        # Draw sprites
        player_group.draw(screen)
        formation.draw(screen)
        laser_group.draw(screen)
        invader_laser_group.draw(screen)
        explosion_group.draw(screen)
        bunker_group.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
