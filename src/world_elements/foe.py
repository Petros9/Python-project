import pygame

from basic import Point
from character import Character
import basic as bs
from models import Models
from settings import HORIZONTAL_ACCELERATION, IMMORTALITY_TIME, FOE_BULLETS_PER_BURST, CELL_SIZE, FOE_RANGE


class Foe(Character):
    def __init__(self, img, x, y, level):
        super().__init__(img, bs.Point(x, y), level)
        self.foe_health = 3
        self.foe_direct = bs.Direction.LEFT
        self.immortality_timer = 0
        self.reload_timer = 0
        self.bullets = FOE_BULLETS_PER_BURST
        self.landed = False

    def take_hit(self):
        self.foe_health -= 1
        self.immortality_timer = IMMORTALITY_TIME
        if(self.foe_direct == bs.Direction.LEFT):
            self.image = Models.FOE_L_DAM_IMG
        else:
            self.image = Models.FOE_R_DAM_IMG

    def shoot(self):
        if (self.foe_direct == bs.Direction.RIGHT):
            bullet_position = Point(self.rect.x + 18, self.rect.y)
            bullet_velocity = Point(15, 0)
            self.world.shoot(bullet_position, bullet_velocity)
        else:
            bullet_position = Point(self.rect.x - 18, self.rect.y)
            bullet_velocity = Point(-15, 0)
            self.world.shoot(bullet_position, bullet_velocity)

    def change_image(self):
        if(self.foe_direct == bs.Direction.RIGHT):
            self.image = Models.FOE_R_IMG
        else:
            self.image = Models.FOE_L_IMG

    def reaches(self, hero_position):
        if(abs(hero_position.y - self.position.y) > CELL_SIZE*3/4):
            return False
        else:
            if(self.foe_direct == bs.Direction.LEFT):
                return FOE_RANGE > self.position.x - hero_position.x > 0
            else:
                return 0 < hero_position.x - self.position.x < FOE_RANGE

    def reverse_direction(self):
        if(self.foe_direct == bs.Direction.RIGHT):
            self.foe_direct = bs.Direction.LEFT
        else:
            self.foe_direct = bs.Direction.RIGHT

    def update(self):

        old_position = self.position
        if(self.foe_direct == bs.Direction.LEFT):
            x_direction = -1

        else:
            x_direction = 1
        self.accelerate(x_direction*HORIZONTAL_ACCELERATION/2, 0)

        super().update()

        if (self.ground_detector.is_on_ground() and not self.landed):
            self.landed = True

        if (old_position == self.position):
            self.reverse_direction()

        if(self.landed and self.position.y != old_position.y):
            self.position = old_position
            self.velocity.x = 0
            self.velocity.y = 0
            self.reverse_direction()

