""" Simple settings """

import os


# Screen settings
SCREEN_WIDTH = 920
SCREEN_HEIGHT = 520
CELL_SIZE = 40


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREEN = (120, 230, 120)
RED = (230, 0, 50)
BLUE = (0, 100, 200)
BACKGROUND_COLOR = BLACK


# Movement settings
GRAVITY = 3
SPEED_LIMIT = 30  # Speed limit for each axis independently
FRICTION = 0.9
AIR_RESISTANCE = 0.9
INERTIA_X = 2
INERTIA_Y = 1
JUMP_ACCELERATION = 15
HORIZONTAL_ACCELERATION = 1


# Make a valid path to the appropriate resources directories for operating
# system in use. Paths are relative to a src directory.
SEP = os.path.sep
SOUND_PATH = SEP.join(['..', 'Resources', 'sound']) + SEP
IMAGE_PATH = SEP.join(['..', 'Resources', 'img', 'basic']) + SEP
LEVELS_PATH = SEP.join(['..', 'Resources', 'levels']) + SEP

BARON_RIGHT_ANIMATION_PATH = SEP.join(['..', 'Resources', 'img',
                                       'baron_animation', 'right']) + SEP
BARON_LEFT_ANIMATION_PATH = SEP.join(['..', 'Resources', 'img',
                                      'baron_animation', 'left']) + SEP

FOE_RIGHT_ANIMATION_PATH = SEP.join(['..', 'Resources', 'img',
                                     'foe_animation', 'right']) + SEP
FOE_LEFT_ANIMATION_PATH = SEP.join(['..', 'Resources', 'img',
                                    'foe_animation', 'left']) + SEP
# Towers
TOWER_BULLETS_PER_BURST = 3
TOWER_TIME_BETWEEN_BULLETS_IN_BURST = 7
TOWER_RELOAD_TIME = 65

# Hero
IMMORTALITY_TIME = 20
HERO_HEALTH = 3

# Foe
FOE_HEALTH = 3
FOE_BULLETS_PER_BURST = 3
FOE_TIME_BETWEEN_BULLETS_IN_BURST = 5
FOE_RELOAD_TIME = 20
FOE_RANGE = 600

# Bridge
BRIDGE_DESTRUCTION_TIME = 5

# FPS
FPS = 22

DEBUG = False
