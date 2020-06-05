import basic as bs
import animations as ani
from basic import Point
from world_elements.moving_objects.character import Character
from settings_and_data.models_and_sounds import ModelsAndSounds
from settings_and_data.settings import *


class Foe(Character):
    def __init__(self, img, x, y, level):
        super().__init__(img, bs.Point(x, y), level)
        self.foe_health = 3
        self.immortality_timer = 0
        self.reload_timer = 0
        self.bullets = FOE_BULLETS_PER_BURST
        self.current_animation_model = 0

    def next_animation_model(self):
        self.current_animation_model += 1
        self.current_animation_model %= 22

    def take_hit(self):
        self.foe_health -= 1
        self.immortality_timer = IMMORTALITY_TIME
        if (self.direction == bs.Direction.LEFT):
            self.image = ModelsAndSounds.FOE_L_DAM_IMG
        else:
            self.image = ModelsAndSounds.FOE_R_DAM_IMG

    def shoot(self):
        if (self.direction == bs.Direction.RIGHT):
            bullet_position = Point(self.rect.x + 18, self.rect.y)
            bullet_velocity = Point(15, 0)
            self.world.shoot(bullet_position, bullet_velocity)
        else:
            bullet_position = Point(self.rect.x - 18, self.rect.y)
            bullet_velocity = Point(-15, 0)
            self.world.shoot(bullet_position, bullet_velocity)

    def change_image(self):

        self.image = ani.MovingAnimations.FOE_MOVING_ANIMATION[
            (self.direction,
             self.current_animation_model)]
        self.next_animation_model()

    def reaches(self, hero_position):
        if (abs(hero_position.y - self.position.y) > CELL_SIZE * 3 / 4):
            return False
        else:
            if (self.direction == bs.Direction.LEFT):
                return FOE_RANGE > self.position.x - hero_position.x > 0
            else:
                return 0 < hero_position.x - self.position.x < FOE_RANGE

    def reverse_direction(self):
        if (self.direction == bs.Direction.RIGHT):
            self.direction = bs.Direction.LEFT
        else:
            self.direction = bs.Direction.RIGHT

    def update(self):

        old_position = self.position
        if (self.direction == bs.Direction.LEFT):
            x_direction = -1

        else:
            x_direction = 1
        self.accelerate(x_direction * HORIZONTAL_ACCELERATION / 2, 0)

        super().update()

        if (old_position == self.position):
            self.reverse_direction()

        if (self.position.y != old_position.y):
            self.position = old_position
            self.velocity.x = 0
            self.velocity.y = 0
            self.reverse_direction()
