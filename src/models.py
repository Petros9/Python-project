import pygame

from settings import *


class Models:
    try:
        BARON_R_IMG = pygame.image.load(IMAGE_PATH + "baron_r.png")
        BARON_L_IMG = pygame.image.load(IMAGE_PATH + "baron_l.png")
        BARON_L_SQUAT_IMG = pygame.image.load(IMAGE_PATH + "baron_l_squat.png")
        BARON_R_SQUAT_IMG = pygame.image.load(IMAGE_PATH + "baron_r_squat.png")
        BARON_R_DAM_IMG = pygame.image.load(IMAGE_PATH+"baron_dam_r.png")
        BARON_L_DAM_IMG = pygame.image.load(IMAGE_PATH+"baron_dam_l.png")
        BARON_L_JUMPING_IMG = pygame.image.load(IMAGE_PATH + "baron_l_jumping.png")
        BARON_R_JUMPING_IMG = pygame.image.load(IMAGE_PATH + "baron_r_jumping.png")
        BARON_L_DAM_JUMPING_IMG = pygame.image.load(IMAGE_PATH + "baron_dam_l_jumping.png")
        BARON_R_DAM_JUMPING_IMG = pygame.image.load(IMAGE_PATH + "baron_dam_r_jumping.png")
        BARON_R_BRAKING_IMG = pygame.image.load(IMAGE_PATH + "baron_r_braking.png")
        BARON_L_BRAKING_IMG = pygame.image.load(IMAGE_PATH + "baron_l_braking.png")
        BARON_R_DAM_BRAKING_IMG = pygame.image.load(IMAGE_PATH + "baron_dam_r_braking.png")
        BARON_L_DAM_BRAKING_IMG = pygame.image.load(IMAGE_PATH + "baron_dam_l_braking.png")

        PLATFORM_IMG = pygame.image.load(IMAGE_PATH + "platform.png")
        BRIDGE_IMG = pygame.image.load(IMAGE_PATH + "bridge.png")
        FOE_FLAG_IMG = pygame.image.load(IMAGE_PATH + "foe_flag.png")
        BARON_FLAG_IMG = pygame.image.load(IMAGE_PATH + "baron_flag.png")
        BULLET_IMG = pygame.image.load(IMAGE_PATH + "bullet.png")
        FOE_R_IMG = pygame.image.load(IMAGE_PATH + "foe_r.png")
        FOE_L_IMG = pygame.image.load(IMAGE_PATH + "foe_l.png")
        FOE_R_DAM_IMG = pygame.image.load(IMAGE_PATH + "foe_dam_r.png")
        FOE_L_DAM_IMG = pygame.image.load(IMAGE_PATH + "foe_dam_l.png")
        HEART_IMG = pygame.image.load(IMAGE_PATH + "heart.png")
        TOWER_IMG = pygame.image.load(IMAGE_PATH + "tower.png")

    except IOError as er:
        print("I/O error in loading models: " + er.strerror)
