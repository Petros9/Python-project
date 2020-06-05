from basic import Point
import world_elements as we
from world_elements.moving_objects.character import Character
import basic as bs
from settings_and_data.settings import *


class Hero(Character):
    def __init__(self, level, img):
        self.level = level
        super().__init__(img, self.level.spawn.position, world=level)
        self.health = HERO_HEALTH
        self.squat = False
        self.level.heroes.add(self)
        self.immortality_timer = 0
        self.jumping = True
        self.current_animation_model = 0

    def take_hit(self):
        if (self.immortality_timer == 0):
            self.immortality_timer = IMMORTALITY_TIME
            self.health -= 1

    def next_animation_model(self):
        self.current_animation_model += 1
        self.current_animation_model %= 22

    def shoot(self):
        # Values of the adjustment of the CELL_SIZE are chosen, so that
        # shooting looks plausible - that is the only determinant.
        if (self.direction is bs.Direction.RIGHT):
            bullet_position = Point(self.rect.x + 0.8 * CELL_SIZE,
                                    self.rect.y + 0.25 * CELL_SIZE)
            bullet_velocity = Point(0.375 * CELL_SIZE, 0)
        else:
            bullet_position = Point(self.rect.x,
                                    self.rect.y + 0.25 * CELL_SIZE)
            bullet_velocity = Point(-0.375 * CELL_SIZE, 0)
        self.level.shoot(bullet_position, bullet_velocity)

    def die(self):
        self.health = HERO_HEALTH
        self.position = self.level.spawn.position * CELL_SIZE
        self.velocity = bs.Point(0, 0)
        self.acceleration = bs.Point(0, 0)
        self.immortality_timer = IMMORTALITY_TIME

    def dig(self):
        # Make dig only if it is guaranteed to not fall off the screen
        if (self.position.y < SCREEN_HEIGHT - 2 * CELL_SIZE):
            self.rect.y += CELL_SIZE / 2
            self.position.y += CELL_SIZE / 2

    def update(self):
        # Check if character is not beyond screen
        old_position = bs.Point.from_tuple(self.position.tuple())
        super().update()

        if (self.ground_detector.is_on_ground()):
            self.jumping = False
        else:
            self.jumping = True

        if (old_position.y == self.position.y):
            bridges = filter(lambda p: isinstance(p, we.Bridge),
                             self.ground_detector.ground_sprites())

            for bridge in bridges:
                if (bridge.timer < 0):
                    bridge.timer = BRIDGE_DESTRUCTION_TIME

        if (self.immortality_timer > 0):
            self.immortality_timer -= 1
        # Check if hero is not going off the screen.
        if (self.rect.x < 0):
            self.rect.x = 0
            self.position.x = 0
            self.acceleration.x = 0

        if (self.rect.y > SCREEN_HEIGHT):
            self.die()

        return self.position - old_position
