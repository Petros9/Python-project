from world_elements.static_objects.static_object import StaticObject


class Flag(StaticObject):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.active = False
        self.captured = False
