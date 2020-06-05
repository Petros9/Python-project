from world_elements.static_objects.static_object import StaticObject


class Bridge(StaticObject):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)

        # Set timer value to -1 -- in first contact with hero, the timer will
        # be set to some counting time, after which it will be destroyed.
        self.timer = -1
