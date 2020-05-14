import sys

import pygame

import world_elements as we
import basic as bs
from models import Models
from level_loader import LevelLoader
from settings import *
from animations.baron_moving_animations import Animation_models


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


def intro_level(screen, intro_timer, manfred):
    font = pygame.font.SysFont("ComicSans", 15)
    text1 = font.render("Kapitanie! Zaatakowały", 1, BLACK)
    text2 = font.render("nas straszne gorgole! AAAAA", 1, BLACK)
    if (intro_timer < 140):
        screen.blit(Models.COMPANION, (300, 200))
        pygame.draw.rect(screen, WHITE, (240, 160, 150, 30))
        screen.blit(text1, (242, 160))
        screen.blit(text2, (242, 175))

    elif(140 < intro_timer < 160):
        screen.blit(Models.COMPANION_DAM, (300, 200))
    if(160> intro_timer > 110):
        screen.blit(Models.FOE_L_IMG, (440, 200))
        if(intro_timer < 140):
            screen.blit(Models.BULLET_IMG, (440 + (110 - intro_timer)*4, 210))

    if(intro_timer > 160):
        if(intro_timer%2 == 0):
            screen.blit(Models.FOE_L_IMG, (440, 200 + (160 - intro_timer)*4))
        else:
            screen.blit(Models.FOE_R_IMG, (440, 200 + (160 - intro_timer)*4))

    text3 = font.render("Zemszczę się...", 1, BLACK)
    if(intro_timer > 260):
        pygame.draw.rect(screen, WHITE, (manfred.position.x - 80, manfred.position.y - 15, 80, 15))
        screen.blit(text3, (manfred.position.x - 78, manfred.position.y - 13))

def main():
    # Basics init.
    pygame.init()

    pygame.mixer.init()

    baron_shoot_sound = pygame.mixer.Sound(SOUND_PATH + "baron_shoot.wav")
    if (not DEBUG):
        pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_intro(screen)
    pygame.mixer.music.load(SOUND_PATH + "theme.wav")
    # Images for level loader.
    level_objects_images = {
        'platform': Models.PLATFORM_IMG,
        'flag': Models.FOE_FLAG_IMG,
        'foe': Models.FOE_L_IMG,
        'tower': Models.TOWER_IMG,
        'bridge': Models.BRIDGE_IMG,
        'boss': Models.COMPANION
    }

    # First level init.
    zero_level = LevelLoader(LEVELS_PATH + "intro_level").load_level(level_objects_images)

    first_level = LevelLoader(LEVELS_PATH + "first_level").load_level(
        level_objects_images)

    second_level = LevelLoader(LEVELS_PATH + "second_level").load_level(
        level_objects_images)

    boss_level = LevelLoader(LEVELS_PATH + "boss_level").load_level(
        level_objects_images)

    level_list = [zero_level, boss_level, first_level, second_level]
    level_counter = 0
    ahead_counter = 0
    timer = 0
    manfred = we.Hero(level_list[level_counter], Models.BARON_R_IMG)

    # Main loop.
    pause = False
    ax = 0
    clock = pygame.time.Clock()
    manfred_animations_model = Animation_models()
    intro_timer = 0
    while (True):
        if (ahead_counter != level_counter and timer == 0):
            level_counter += 1
            manfred = we.Hero(level_list[level_counter], Models.BARON_R_IMG)
        if (timer > 0):
            timer -= 1
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
                    if (event.key == pygame.K_RIGHT):
                        ax = HORIZONTAL_ACCELERATION
                    if (event.key == pygame.K_LEFT):
                        ax = -HORIZONTAL_ACCELERATION
                    if (event.key == pygame.K_UP):
                        if (manfred.squat):
                            manfred.change_squat_state()
                        else:
                            ay = -JUMP_ACCELERATION
                    if (event.key == pygame.K_DOWN and not manfred.jumping):
                        if (manfred.squat and manfred.position.y < 400):
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
        if (manfred.squat):
            ax = 0
            ay = 0

        old_position = manfred.position

        manfred.accelerate(ax, ay)
        hero_displacement = manfred.update()
        level_list[level_counter].foes.update()

        # Make screen following the hero if his velocity is significant.
        if (manfred.rect.centerx > 0.5 * SCREEN_WIDTH and
                hero_displacement.x > 0):
            level_list[level_counter].follow_hero(-hero_displacement.x)

        flags_in_touch = pygame.sprite.spritecollide(manfred,
                                                     level_list[level_counter].flags, False)
        for flag in flags_in_touch:
            if (not flag.captured):
                flag.image = Models.BARON_FLAG_IMG
                flag.captured = True
                ahead_counter += 1
                timer = IMMORTALITY_TIME

        level_list[level_counter].shoot_towers()
        level_list[level_counter].move_bullets()
        level_list[level_counter].move_foes()
        level_list[level_counter].move_boss()
        if (manfred.rect.x != old_position.x and manfred.rect.y == old_position.y and manfred.immortality_timer == 0):
            if (manfred.direction is bs.Direction.RIGHT):
                manfred.image = manfred_animations_model.models_list[(1, manfred.current_animation_model)]
                manfred.next_animation_model()
            else:
                manfred.image = manfred_animations_model.models_list[(2, manfred.current_animation_model)]
                manfred.next_animation_model()
        else:
            manfred.current_animation_model = 0
            if (manfred.direction is bs.Direction.RIGHT):

                if (manfred.squat is True):
                    manfred.image = Models.BARON_R_SQUAT_IMG

                elif (manfred.jumping):
                    if (manfred.immortality_timer == 0):
                        manfred.image = Models.BARON_R_JUMPING_IMG
                    else:
                        manfred.image = Models.BARON_R_DAM_JUMPING_IMG

                elif (1 < manfred.velocity.x < HORIZONTAL_ACCELERATION * 4):
                    if (manfred.immortality_timer == 0):
                        manfred.image = Models.BARON_R_BRAKING_IMG
                    else:
                        manfred.image = Models.BARON_R_DAM_BRAKING_IMG

                else:
                    if (manfred.immortality_timer == 0):
                        manfred.image = Models.BARON_R_IMG
                    else:
                        manfred.image = Models.BARON_R_DAM_IMG

            elif (manfred.direction is bs.Direction.LEFT):

                if (manfred.squat is True):
                    manfred.image = Models.BARON_L_SQUAT_IMG

                elif (manfred.jumping):
                    if (manfred.immortality_timer == 0):
                        manfred.image = Models.BARON_L_JUMPING_IMG
                    else:
                        manfred.image = Models.BARON_L_DAM_JUMPING_IMG

                elif (-1 > manfred.velocity.x > -HORIZONTAL_ACCELERATION * 4):
                    if (manfred.immortality_timer == 0):
                        manfred.image = Models.BARON_L_BRAKING_IMG
                    else:
                        manfred.image = Models.BARON_L_DAM_BRAKING_IMG
                else:
                    if (manfred.immortality_timer == 0):
                        manfred.image = Models.BARON_L_IMG
                    else:
                        manfred.image = Models.BARON_L_DAM_IMG

        # Draw things.
        level_list[level_counter].all_platforms.draw(screen)
        level_list[level_counter].flags.draw(screen)
        level_list[level_counter].bridges.draw(screen)
        level_list[level_counter].towers.draw(screen)
        level_list[level_counter].bullets.draw(screen)
        level_list[level_counter].boss.draw(screen)

        if(level_counter == 0 and intro_timer < 300):
            intro_level(screen, intro_timer, manfred)
            intro_timer += 1
            print(intro_timer)

        manfred.adjust_visual()
        for foe in level_list[level_counter].foes:
            foe.adjust_visual()

        level_list[level_counter].heroes.draw(screen)
        level_list[level_counter].foes.draw(screen)

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
