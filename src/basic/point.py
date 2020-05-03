
class Point:
    """ Point on a 2D plane, also a vector.

    Attributes:
        x:
        y:
    """

    EPSILON = 1.e-10

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, coordinates: tuple):
        return Point(coordinates[0], coordinates[1])

    def __eq__(self, other):
        if (isinstance(self.x, int) and isinstance(self.y, int) and
                isinstance(other.x, int) and isinstance(other.y, int)):
            return self.x == other.x and self.y == other.y

        return abs(self.x - other.x) < self.EPSILON and \
            abs(self.y - other.y) < self.EPSILON

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        return self + other

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other)

    def __isub__(self, other):
        return self - other

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if (other == 0):
            raise ArithmeticError("Vector division by 0.")
        return Point(self.x / other, self.y / other)

    def __repr__(self):
        return f"<Point({self.x}, {self.y})>"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def something_on_y_axis(self, other, new_y):
        self.y += new_y
        if (self == other):
            return 0
        else:
            return new_y

    def something_on_x_axis(self, other, new_x):
        self.x += new_x
        if (self == other):
            return 0
        else:
            return new_x

    def is_same_level(self, other):
        return self.y == other.y

    def tuple(self):
        return self.x, self.y

    def round(self):
        return Point(int(self.x), int(self.y))

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
