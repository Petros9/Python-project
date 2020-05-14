import pygame

from basic import Point
from character import Character
import basic as bs
from models import Models
from animations.foe_moving_animation import models_list
from settings import HORIZONTAL_ACCELERATION, IMMORTALITY_TIME, FOE_BULLETS_PER_BURST, CELL_SIZE, FOE_RANGE


class Boss(Character):
    def __init__(self, img, x, y, level):
        super().__init__(img, bs.Point(x, y), level)
        self.boss_health = 5
        self.boss_direct = bs.Direction.LEFT
        self.immortality_timer = 0
        self.reload_timer = 0
        self.bullets = FOE_BULLETS_PER_BURST
        self.landed = False
