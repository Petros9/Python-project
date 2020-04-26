from basic.point import Point
from physics_object import PhysicsObject

BULLET_SPEED = 5


class Bullet(PhysicsObject):
    # '' pusty docstring
    """
    """

    def __init__(self, x=1, y=1, speed=3, y_direction=0):
        super().__init__(Point(x, y))
        self.speed = speed
        self.y_direction = y_direction

    def move(self):
        self.position += Point(self.speed, self.y_direction)

    def position_on_screen(self, hero_position):
        return self.position.x - hero_position + 30
