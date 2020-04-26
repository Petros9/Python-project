from src.basic.point import Point


class Platform():
    def __init__(self, x, y):
        self.position = Point(x, y)

    def __repr__(self):
        return "Platform" + str(self.position.tuple())

    def position_on_screen(self, hero_position):
        return self.position.x - hero_position + 30
