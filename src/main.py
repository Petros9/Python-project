import sys
import time

import pygame

from level_loader import LevelLoader
from world_elements.bridge import Bridge
from world_elements.foe import Foe
from world_elements.flag import Flag
from world_elements.hero import Hero
from world_elements.level import Level
from world_elements.tower import Tower
from world_elements.platform import Platform

TMP_JUMP_HEIGHT = 10
TMP_HERO_HORIZONTAL_STEP = 1


def is_over_start_button(pos):
    return 290 < pos[0] < 390 and 300 < pos[1] < 340


def is_over_quit_button(pos):
    return 510 < pos[0] < 610 and 300 < pos[1] < 340


def game_intro(screen):
    intro = True
    title = pygame.image.load(r"..\Resources\img\basic\title.png")
    while (intro):

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (is_over_start_button(pos)):
                    intro = False
                if (is_over_quit_button(pos)):
                    pygame.quit()
                    quit()

        screen.blit(title, (250, 0))

        font = pygame.font.SysFont('ComicSans', 60)
        text1 = font.render("Start", 1, (0, 0, 0))
        text2 = font.render("Quit", 1, (0, 0, 0))

        pygame.draw.rect(screen, (120, 230, 120), (290, 300, 100, 40))
        screen.blit(text1, (290, 300))

        pygame.draw.rect(screen, (230, 0, 50), (510, 300, 100, 40))
        screen.blit(text2, (510, 300))
        pygame.display.update()


def main():
    pygame.init()

    pygame.mixer.init()

    pygame.mixer.music.load(
        r"..\Resources\sound\theme.wav")
    baron_shoot_sound = pygame.mixer.Sound(
        r"..\Resources\sound\baron_shoot.wav")
    pygame.mixer.music.play(-1)

    screen_size = (920, 520)
    screen = pygame.display.set_mode(screen_size)

    game_intro(screen)
    object_list = LevelLoader("../Resources/test").load_level()
    first_level = Level(object_list)
    manfred = Hero(first_level)
    first_level.hero = manfred

    baron_r_img = pygame.image.load(r"..\Resources\img\basic\baron_r.png")
    baron_l_img = pygame.image.load(r"..\Resources\img\basic\baron_l.png")
    baron_l_squat_img = pygame.image.load(
        r"..\Resources\img\basic\baron_l_squat.png")
    baron_r_squat_img = pygame.image.load(
        r"..\Resources\img\basic\baron_r_squat.png")
    platform_img = pygame.image.load(r"..\Resources\img\basic\platform.png")
    bridge_img = pygame.image.load(r"..\Resources\img\basic\bridge.png")
    foe_flag_img = pygame.image.load(r"..\Resources\img\basic\foe_flag.png")
    baron_flag_img = pygame.image.load(r"..\Resources\img\basic\baron_flag.png")
    bullet_img = pygame.image.load(r"..\Resources\img\basic\patron.png")
    foe_img = pygame.image.load(r"..\Resources\img\basic\foe.png")
    heart_img = pygame.image.load(r"..\Resources\img\basic\heart.png")
    tower_img = pygame.image.load(r"..\Resources\img\basic\tower.png")

    ax = 0
    while (True):

        ay = 0
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP):
                ax = 0
            if (event.type == pygame.QUIT):
                sys.exit(0)
            elif (event.type == pygame.KEYDOWN):

                if (event.key == pygame.K_RIGHT and not manfred.squat):
                    ax = TMP_HERO_HORIZONTAL_STEP
                    manfred.right_direction()

                if (event.key == pygame.K_LEFT and not manfred.squat):
                    ax = -TMP_HERO_HORIZONTAL_STEP
                    manfred.left_direction()

                if (event.key == pygame.K_UP):
                    if (manfred.squat):
                        manfred.change_squat_state()
                    else:
                        ay = -TMP_JUMP_HEIGHT
                        manfred.jumping = True
                if (event.key == pygame.K_DOWN and not manfred.jumping):
                    manfred.change_squat_state()
                if (event.key == pygame.K_SPACE and not manfred.squat):
                    baron_shoot_sound.play()
                    manfred.shoot()
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                if (event.key == pygame.K_0):
                    manfred.die()

        screen.fill((0, 0, 0))

        for object in first_level.objects:
            if (isinstance(object, Platform)):
                img = platform_img
            elif (isinstance(object, Flag)):
                if (not object.captured):
                    img = foe_flag_img
                else:
                    img = baron_flag_img
            elif (isinstance(object, Foe)):
                img = foe_img
            elif (isinstance(object, Tower)):
                img = tower_img
            elif (isinstance(object, Bridge)):
                img = bridge_img
            screen.blit(img, (
            object.position_on_screen(int(manfred.position.x)) * 4 + 40,
            int(object.position.y) * 4 - 20))

        for bullet in first_level.bullets_list:
            screen.blit(bullet_img, (
            int(bullet.position_on_screen(manfred.position.x) * 4 + 40),
            int(bullet.position.y) * 4 - 20))

        first_level.shoot_towers()
        first_level.move_bullets()

        manfred.accelerate(ax, ay)
        manfred.update()

        if (manfred.position.y >= 210):
            manfred.die()

        baron_pos = (160, int(manfred.position.y) * 4 - 20)

        if (manfred.is_in_right_direction()):
            if (manfred.squat):
                screen.blit(baron_r_squat_img, baron_pos)
            else:
                screen.blit(baron_r_img, baron_pos)
        else:
            if (manfred.squat):
                screen.blit(baron_l_squat_img, baron_pos)
            else:
                screen.blit(baron_l_img, baron_pos)

        times = manfred.health
        while (times > 0):
            screen.blit(heart_img, (times * 45, 40))
            times -= 1
        print(len(first_level.tower_list))
        # print(manfred.position)
        pygame.display.flip()
        time.sleep(0.08)


if (__name__ == "__main__"):
    main()
