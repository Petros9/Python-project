from basic.point import Point
from physics_object import PhysicsObject


# będą dwa rodzaje flag, cesaskie i
class Flag(PhysicsObject):
    def __init__(self, x, y):
        super().__init__(Point(x, y))
        self.position = Point(x, y)
        self.active = False
        self.captured = False

    def place_flag(self, x, y):
        self.position = Point(x, y)

    def capture(self):
        self.captured = True

    def position_on_screen(self, hero_position):
        return self.position.x - hero_position + 30