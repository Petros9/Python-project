from basic.direction import Direction
from physics_object import PhysicsObject
from world_elements.spawn import Spawn


class Hero(PhysicsObject):
    def __init__(self, level):
        self.spawn = Spawn()
        super().__init__(self.spawn.position)
        self.position = self.spawn.position
        self.health = 3
        self.direct = Direction.RIGHT
        self.level = level
        self.assign_world(level)
        self.squat = False

    def left_direction(self):
        self.direct = Direction.LEFT

    def right_direction(self):
        self.direct = Direction.RIGHT

    def is_in_right_direction(self):
        return self.direct == Direction.RIGHT

    def take_hit(self):
        self.health -= 1

    def change_squat_state(self):
        self.squat = not self.squat

    def shoot(self):
        if(self.is_in_right_direction()):
            self.level.shoot(self.position.x+6, self.position.y, 3, 0)
        else:
            self.level.shoot(self.position.x-6, self.position.y, -3, 0)

    def die(self):
        self.health = 3
        self.position = self.spawn.position

