import sys

import pygame

import world_elements as we
import basic as bs
from models import Models
from level_loader import LevelLoader
from settings import *


def game_intro(screen):
    intro = True
    title = pygame.image.load(IMAGE_PATH + "title.png")

    # Visual intro
    screen.blit(title, (250, 0))

    font = pygame.font.SysFont("ComicSans", 60)
    text1 = font.render("Start", 1, BLACK)
    text2 = font.render("Quit", 1, BLACK)

    pygame.draw.rect(screen, LIGHT_GREEN, (290, 300, 100, 40))
    screen.blit(text1, (290, 300))

    pygame.draw.rect(screen, RED, (510, 300, 100, 40))
    screen.blit(text2, (510, 300))
    pygame.display.update()

    # Intro logic
    while (intro):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (290 < pos[0] < 390 and 300 < pos[1] < 340):
                    intro = False
                if (510 < pos[0] < 610 and 300 < pos[1] < 340):
                    pygame.quit()
                    quit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                intro = False


def main():
    # Basics init.
    pygame.init()

    pygame.mixer.init()

    pygame.mixer.music.load(SOUND_PATH + "theme.wav")
    baron_shoot_sound = pygame.mixer.Sound(SOUND_PATH + "baron_shoot.wav")
    if (not DEBUG):
        pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_intro(screen)

    # Images for level loader.
    level_objects_images = {
        'platform': Models.PLATFORM_IMG,
        'flag': Models.FOE_FLAG_IMG,
        'foe': Models.FOE_L_IMG,
        'tower': Models.TOWER_IMG,
        'bridge': Models.BRIDGE_IMG
    }

    # First level init.
    first_level = LevelLoader(LEVELS_PATH + "test_level").load_level(
        level_objects_images)
    manfred = we.Hero(first_level, Models.BARON_R_IMG)

    # Main loop.
    pause = False
    ax = 0
    clock = pygame.time.Clock()
    while (True):

        ay = 0
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP and
                    (event.key == pygame.K_LEFT or
                     event.key == pygame.K_RIGHT)):
                ax = 0
            if (event.type == pygame.QUIT):
                sys.exit(0)
            elif (event.type == pygame.KEYDOWN):
                if (not pause):
                    if (event.key == pygame.K_RIGHT and not manfred.squat):
                        ax = HORIZONTAL_ACCELERATION
                    if (event.key == pygame.K_LEFT and not manfred.squat):
                        ax = -HORIZONTAL_ACCELERATION
                    if (event.key == pygame.K_UP):
                        if (manfred.squat):
                            manfred.change_squat_state()
                        else:
                            ay = -JUMP_ACCELERATION
                    if (event.key == pygame.K_DOWN and not manfred.jumping):
                        if(manfred.squat and manfred.position.y < 400):
                            manfred.dig()
                        manfred.change_squat_state()
                    if (event.key == pygame.K_SPACE and not manfred.squat):
                        
                        baron_shoot_sound.play()
                        manfred.shoot()
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                if (event.key == pygame.K_0):
                    manfred.die()
                if (DEBUG and event.key == pygame.K_p):
                    pause = not pause

        if (DEBUG and pause):
            text = pygame.font.Font(None, 60).render("Pause", True,
                                                     LIGHT_GREEN)
            text_rect = text.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])
            pygame.display.set_caption("Pause")
            pygame.display.flip()
            continue

        screen.fill(BLACK)

        # Apply motions logic.
        manfred.accelerate(ax, ay)
        hero_displacement = manfred.update()
        first_level.foes.update()

        # Make screen following the hero if his velocity is significant.
        if (manfred.rect.centerx > 0.5 * SCREEN_WIDTH and
                hero_displacement.x > 0):
            first_level.follow_hero(-hero_displacement.x)

        flags_in_touch = pygame.sprite.spritecollide(manfred,
                                                     first_level.flags, False)
        for flag in flags_in_touch:
            if (not flag.captured):
                flag.image = Models.BARON_FLAG_IMG
                flag.captured = True

        first_level.shoot_towers()
        first_level.move_bullets()
        first_level.move_foes()

        if (manfred.direction is bs.Direction.RIGHT):
            if (manfred.squat is True):
                manfred.image = Models.BARON_R_SQUAT_IMG
            else:
                if (manfred.immortality_timer == 0):
                    manfred.image = Models.BARON_R_IMG
                else:
                    manfred.image = Models.BARON_R_DAM_IMG
        elif (manfred.direction is bs.Direction.LEFT):
            if (manfred.squat is True):
                manfred.image = Models.BARON_L_SQUAT_IMG
            else:
                if (manfred.immortality_timer == 0):
                    manfred.image = Models.BARON_L_IMG
                else:
                    manfred.image = Models.BARON_L_DAM_IMG

        # Draw things.
        first_level.all_platforms.draw(screen)
        first_level.flags.draw(screen)
        first_level.bridges.draw(screen)
        first_level.towers.draw(screen)
        first_level.bullets.draw(screen)

        manfred.adjust_visual()
        for foe in first_level.foes:
            foe.adjust_visual()

        first_level.heroes.draw(screen)
        first_level.foes.draw(screen)

        hero_health = manfred.health
        while (hero_health > 0):
            screen.blit(Models.HEART_IMG, (hero_health * 45, 40))
            hero_health -= 1

        if (DEBUG):
            pygame.sprite.Group([manfred.ground_detector]).draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if (__name__ == "__main__"):
    main()
