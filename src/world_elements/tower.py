from settings import *
from static_object import StaticObject


class Tower(StaticObject):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.reload_timer = 0
        self.bullets = TOWER_BULLETS_PER_BURST
