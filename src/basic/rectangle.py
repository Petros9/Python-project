from basic.point import Point


class Rectangle:
    """
    """

    def __init__(self, lower_left, upper_right):
        self.lower_left = lower_left
        self.upper_right = upper_right

    def __contains__(self, item):
        if (item is not type(Point)):
            return False
        return (self.lower_left.x <= item.x <= self.upper_right.x and
                self.lower_left.y <= item.y <= self.upper_right.y)
