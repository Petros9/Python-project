import pygame

import world_elements as we
import basic as bs
from level import LevelLoader
import settings_and_data as sd
import animations as ani


def game_intro(screen):
    intro = True
    title = sd.ModelsAndSounds.TITLE

    # Visual intro
    screen.blit(title, (250, 0))

    font = pygame.font.SysFont("ComicSans", 60)
    text1 = font.render("Start", 1, sd.BLACK)
    text2 = font.render("Quit", 1, sd.BLACK)

    pygame.draw.rect(screen, sd.LIGHT_GREEN, (290, 300, 100, 40))
    screen.blit(text1, (290, 300))

    pygame.draw.rect(screen, sd.RED, (510, 300, 100, 40))
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
    text1 = font.render("Kapitanie! Zaatakowały", 1, sd.BLACK)
    text2 = font.render("nas straszne gorgole! AAAAA", 1, sd.BLACK)
    if (intro_timer < 140):
        screen.blit(sd.ModelsAndSounds.COMPANION_L, (300, 200))
        pygame.draw.rect(screen, sd.WHITE, (240, 160, 150, 30))
        screen.blit(text1, (242, 160))
        screen.blit(text2, (242, 175))

    elif (140 < intro_timer < 160):
        screen.blit(sd.ModelsAndSounds.COMPANION_L_DAM, (300, 200))
    if (160 > intro_timer > 110):
        screen.blit(sd.ModelsAndSounds.FOE_L_IMG, (440, 200))
        if (intro_timer < 140):
            screen.blit(sd.ModelsAndSounds.BULLET_IMG,
                        (440 + (110 - intro_timer) * 4, 210))

    if (intro_timer > 160):
        screen.blit(sd.ModelsAndSounds.FOE_L_IMG,
                    (440, 200 + (160 - intro_timer) * 4))
        if (intro_timer % 2 == 0):
            screen.blit(sd.ModelsAndSounds.FOE_R_IMG,
                        (440, 200 + 4 * (160 - intro_timer)))
        else:
            pass

    text3 = font.render("Zemszczę się...", 1, sd.BLACK)
    if (intro_timer > 260):
        pygame.draw.rect(screen, sd.WHITE, (
            manfred.position.x - 80, manfred.position.y - 15, 80, 15))
        screen.blit(text3, (manfred.position.x - 78, manfred.position.y - 13))


def end_level(screen, bosses):
    font = pygame.font.SysFont("ComicSans", 15)
    text = font.render("Niespodzianka!", 1, sd.BLACK)
    for boss in bosses:
        pygame.draw.rect(screen, sd.WHITE, (boss.position.x - 80,
                                            boss.position.y - 15, 80, 15))
        screen.blit(text, (boss.position.x - 78, boss.position.y - 13))


def end_game(screen):
    screen.fill(sd.BLACK)
    font = pygame.font.SysFont("ComicSans", 60)
    text1 = font.render("Golgors are gone!", 1, sd.BLACK)
    text2 = font.render("Quit", 1, sd.BLACK)

    pygame.draw.rect(screen, sd.WHITE, (250, 100, 360, 40))
    screen.blit(text1, (250, 100))

    pygame.draw.rect(screen, sd.RED, (410, 300, 100, 40))
    screen.blit(text2, (410, 300))
    pygame.display.update()

    # Endgame logic
    while (True):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (410 < pos[0] < 510 and 300 < pos[1] < 340):
                    pygame.quit()
                    quit()


def main():
    # Basics init.
    pygame.init()

    pygame.mixer.init()

    screen = pygame.display.set_mode((sd.SCREEN_WIDTH, sd.SCREEN_HEIGHT))

    game_intro(screen)
    if (not sd.DEBUG):
        # Load music theme here, because it is only used once here to play
        # music.
        try:
            pygame.mixer.music.load(sd.SOUND_PATH + "theme.wav")
        except IOError as er:
            print("I/O error while loading music theme: " + er.strerror)
        pygame.mixer.music.play(-1)

    # Images for level loader.
    level_objects_images = {
        'platform': sd.ModelsAndSounds.PLATFORM_IMG,
        'flag': sd.ModelsAndSounds.FOE_FLAG_IMG,
        'foe': sd.ModelsAndSounds.FOE_L_IMG,
        'tower': sd.ModelsAndSounds.TOWER_IMG,
        'bridge': sd.ModelsAndSounds.BRIDGE_IMG,
        'boss': sd.ModelsAndSounds.COMPANION_L
    }

    # Levels init.
    level_loader = LevelLoader(level_objects_images)
    level_list = [
        level_loader.load_level(sd.LEVELS_PATH + "intro_level"),
        level_loader.load_level(sd.LEVELS_PATH + "first_level"),
        level_loader.load_level(sd.LEVELS_PATH + "second_level"),
        level_loader.load_level(sd.LEVELS_PATH + "boss_level"),
    ]

    level_counter = 0
    level_change_indicator = False
    timer = 0
    manfred = we.Hero(level_list[level_counter],
                      sd.ModelsAndSounds.BARON_R_IMG)

    # Main loop.
    pause = False
    ax = 0
    clock = pygame.time.Clock()
    intro_timer = 0
    end_timer = 0
    while (True):
        if (level_change_indicator is True and timer == 0):
            level_counter += 1
            manfred = we.Hero(level_list[level_counter],
                              sd.ModelsAndSounds.BARON_R_IMG)
            level_change_indicator = False
        if (timer > 0):
            timer -= 1
        ay = 0
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP and
                    (event.key == pygame.K_LEFT or
                     event.key == pygame.K_RIGHT)):
                ax = 0
            if (event.type == pygame.QUIT):
                pygame.quit()
                exit()
            elif (event.type == pygame.KEYDOWN):
                if (not pause):
                    # Movement and action keys
                    if (event.key == pygame.K_RIGHT):
                        ax = sd.HORIZONTAL_ACCELERATION
                    if (event.key == pygame.K_LEFT):
                        ax = -sd.HORIZONTAL_ACCELERATION
                    if (event.key == pygame.K_UP):
                        if (manfred.squat):
                            manfred.squat = not manfred.squat
                        else:
                            ay = -sd.JUMP_ACCELERATION
                    if (event.key == pygame.K_DOWN and not manfred.jumping):
                        if (manfred.squat):
                            manfred.dig()
                        manfred.squat = not manfred.squat
                    if (event.key == pygame.K_SPACE and not manfred.squat):
                        if (not sd.DEBUG):
                            sd.ModelsAndSounds.BARON_SHOOT_SOUND.play()
                        manfred.shoot()

                    # Functional keys
                    if (event.key == pygame.K_0):
                        manfred.die()
                    if (sd.DEBUG and event.key == pygame.K_k):
                        level_change_indicator = True
                # Actions independent on pause
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                if (sd.DEBUG and event.key == pygame.K_p):
                    pause = not pause

        if (sd.DEBUG and pause):
            text = pygame.font.Font(None, 60).render("Pause", True,
                                                     sd.LIGHT_GREEN)
            text_rect = text.get_rect()
            text_x = sd.SCREEN_WIDTH / 2 - text_rect.width / 2
            text_y = sd.SCREEN_HEIGHT / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])
            pygame.display.set_caption("Pause")
            pygame.display.flip()
            continue

        screen.fill(sd.BLACK)

        # Apply motions logic.
        if (manfred.squat):
            manfred.velocity.x = 0
            ax = 0
            ay = 0

        old_position = manfred.position

        manfred.accelerate(ax, ay)
        hero_displacement = manfred.update()
        level_list[level_counter].foes.update()
        level_list[level_counter].bosses.update()

        # Make screen following the hero if his velocity is significant.
        if (manfred.rect.centerx > 0.5 * sd.SCREEN_WIDTH and
                hero_displacement.x > 0):
            level_list[level_counter].follow_hero(-hero_displacement.x)

        flags_in_touch = pygame.sprite.spritecollide(manfred,
                                                     level_list[
                                                         level_counter].flags,
                                                     False)
        for flag in flags_in_touch:
            if (not flag.captured):
                flag.image = sd.ModelsAndSounds.BARON_FLAG_IMG
                flag.captured = True
                level_change_indicator = True
                timer = sd.IMMORTALITY_TIME

        level_list[level_counter].shoot_towers()
        level_list[level_counter].move_bullets()
        level_list[level_counter].move_foes()
        level_list[level_counter].move_boss()
        level_list[level_counter].update_bridges_statuses()

        if (manfred.rect.x != old_position.x and
                manfred.rect.y == old_position.y and
                manfred.immortality_timer == 0):
            manfred.image = ani.MovingAnimations.BARON_MOVING_ANIMATION[
                (manfred.direction, manfred.current_animation_model)]
            manfred.next_animation_model()
        else:
            manfred.current_animation_model = 0
            if (manfred.direction is bs.Direction.RIGHT):

                if (manfred.squat is True):
                    manfred.image = sd.ModelsAndSounds.BARON_R_SQUAT_IMG

                elif (manfred.jumping):
                    if (manfred.immortality_timer == 0):
                        manfred.image = sd.ModelsAndSounds.BARON_R_JUMPING_IMG
                    else:
                        manfred.image = sd.ModelsAndSounds.BARON_R_DAM_JUMPING_IMG  # noqa

                elif (1 < manfred.velocity.x < sd.HORIZONTAL_ACCELERATION * 4):
                    if (manfred.immortality_timer == 0):
                        manfred.image = sd.ModelsAndSounds.BARON_R_BRAKING_IMG
                    else:
                        manfred.image = sd.ModelsAndSounds.BARON_R_DAM_BRAKING_IMG  # noqa

                else:
                    if (manfred.immortality_timer == 0):
                        manfred.image = sd.ModelsAndSounds.BARON_R_IMG
                    else:
                        manfred.image = sd.ModelsAndSounds.BARON_R_DAM_IMG

            elif (manfred.direction is bs.Direction.LEFT):

                if (manfred.squat is True):
                    manfred.image = sd.ModelsAndSounds.BARON_L_SQUAT_IMG

                elif (manfred.jumping):
                    if (manfred.immortality_timer == 0):
                        manfred.image = sd.ModelsAndSounds.BARON_L_JUMPING_IMG
                    else:
                        manfred.image = sd.ModelsAndSounds.BARON_L_DAM_JUMPING_IMG  # noqa

                elif (
                        -1 > manfred.velocity.x > -sd.HORIZONTAL_ACCELERATION * 4):  # noqa
                    if (manfred.immortality_timer == 0):
                        manfred.image = sd.ModelsAndSounds.BARON_L_BRAKING_IMG
                    else:
                        manfred.image = sd.ModelsAndSounds.BARON_L_DAM_BRAKING_IMG  # noqa
                else:
                    if (manfred.immortality_timer == 0):
                        manfred.image = sd.ModelsAndSounds.BARON_L_IMG
                    else:
                        manfred.image = sd.ModelsAndSounds.BARON_L_DAM_IMG

        # Draw things.
        level_list[level_counter].all_platforms.draw(screen)
        level_list[level_counter].flags.draw(screen)
        level_list[level_counter].bridges.draw(screen)
        level_list[level_counter].towers.draw(screen)
        level_list[level_counter].bullets.draw(screen)
        level_list[level_counter].bosses.draw(screen)

        # Draw intro cut scene.
        if (level_counter == 0 and intro_timer < 300):
            intro_level(screen, intro_timer, manfred)
            intro_timer += 1

        elif (level_counter == 3 and end_timer < 100):
            end_level(screen, level_list[level_counter].bosses)
            end_timer += 1
        if level_list[level_counter].end_game:
            end_game(screen)
        # Adjust moving characters to make them move to the left realistically.
        manfred.adjust_visual()
        for foe in level_list[level_counter].foes:
            foe.adjust_visual()

        level_list[level_counter].heroes.draw(screen)
        level_list[level_counter].foes.draw(screen)

        # Draw hp.
        hero_health = manfred.health
        while (hero_health > 0):
            screen.blit(sd.ModelsAndSounds.HEART_IMG, (hero_health * 45, 40))
            hero_health -= 1

        if (sd.DEBUG):
            pygame.sprite.Group([manfred.ground_detector]).draw(screen)

        pygame.display.flip()
        clock.tick(sd.FPS)


if (__name__ == "__main__"):
    main()
