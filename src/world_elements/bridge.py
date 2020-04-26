from basic.point import Point


class Bridge:
    def __init__(self, x, y):
        self.position = Point(x, y)

    def position_on_screen(self, hero_position):
        return self.position.x - hero_position + 30
