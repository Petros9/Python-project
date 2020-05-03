import basic as bs


class Spawn:
    """ Spawn for heroes.

    Attributes:
        position (Point): Position of spawn relative to the current frame.
    """
    def __init__(self, x=1, y=1):
        # Default is (1, 1), because physics objects like heroes scale the
        # vectors by themselves to match the grid.
        self.position = bs.Point(x, y)
