from character import Character
import basic as bs


class Foe(Character):
    def __init__(self, img, x, y, level):
        super().__init__(img, bs.Point(x, y), level)
        self.foe_health = 3
        self.foe_direct = bs.Direction.LEFT

    def take_hit(self):
        self.foe_health -= 10
