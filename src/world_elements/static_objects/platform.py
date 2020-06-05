from world_elements.static_objects.static_object import StaticObject
from basic import Point


class Platform(StaticObject):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)

    def __repr__(self):
        return "Platform" + str(Point(self.rect.x, self.rect.y).tuple())
