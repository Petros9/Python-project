from character import Character
import basic as bs
from settings import *


class Hero(Character):
    def __init__(self, level, img):
        self.level = level
        super().__init__(img, self.level.spawn.position, world=level)
        self.health = HERO_HEALTH
        self.squat = False
        self.level.heroes.add(self)
        self.immortality_timer = 0

    def take_hit(self):
        if (self.immortality_timer == 0):
            self.immortality_timer = IMMORTALITY_TIME
            self.health -= 1

    def change_squat_state(self):
        self.squat = not self.squat

    def shoot(self):
        if (self.direction == bs.Direction.RIGHT):
            self.level.shoot(self.position.x + 6, self.position.y, 3, 0)
        else:
            self.level.shoot(self.position.x - 6, self.position.y, -3, 0)

    def die(self):
        self.health = HERO_HEALTH
        self.position = self.level.spawn.position * CELL_SIZE
        self.velocity = bs.Point(0, 0)
        self.acceleration = bs.Point(0, 0)

    def update(self):
        # Check if character is not beyond screen
        old_position = bs.Point.from_tuple(self.position.tuple())
        super().update()

        # Check if hero is not going out of the level terrain.
        if (self.rect.x < 0):
            self.rect.x = 0
            self.position.x = 0
            self.acceleration.x = 0

        if (self.rect.y > SCREEN_HEIGHT):
            self.die()

        return self.position - old_position
