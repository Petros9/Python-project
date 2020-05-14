import pygame

from basic import Point
from character import Character
import basic as bs
from models import Models
from settings import *
from settings import HORIZONTAL_ACCELERATION, IMMORTALITY_TIME, FOE_BULLETS_PER_BURST, CELL_SIZE, FOE_RANGE


class Boss(Character):
    def __init__(self, img, x, y, level):
        super().__init__(img, bs.Point(x, y), level)
        self.boss_health = 5
        self.boss_direct = bs.Direction.LEFT
        self.immortality_timer = 0
        self.reload_timer = 0
        self.bullets = FOE_BULLETS_PER_BURST

    def jump(self):
        if(self.boss_direct == bs.Direction.RIGHT):
            self.boss_direct = bs.Direction.LEFT
            ax = -HORIZONTAL_ACCELERATION
        else:
            self.boss_direct = bs.Direction.RIGHT
            ax = HORIZONTAL_ACCELERATION

        ay = -2*JUMP_ACCELERATION
        self.accelerate(ax, ay)
        self.update()

    def take_hit(self):
        self.boss_health -= 1
        self.immortality_timer = IMMORTALITY_TIME

