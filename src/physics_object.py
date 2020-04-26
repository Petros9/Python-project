from src.basic.point import Point

GRAVITY = 1

# The value of air resistance is set, so that going through platform is
# impossible. Do not change it!
AIR_RESISTANCE = 5
FRICTION = 0.8
MOVEMENT_RESISTANCE_X = 1.5
MOVEMENT_RESISTANCE_y = 1
UNIT = 10


class PhysicsObject:
    """
    Class physics object implements basics of motion and collision detection.
    Attributes:
        position:
        velocity:
        world:
    """

    def __init__(self, position, velocity=None, world=None):
        self.position = position
        self.velocity = Point(0, 0) if (velocity is None) else velocity
        self.world = world if (world is not None) else None
        self.jumping = False

    def accelerate(self, ax, ay):
        """ Method changes the velocity of the object.
        Args:
            ax: Acceleration in the direction of the x axis.
            ay: Acceleration in the direction of the y axis.
        """

        # If jumping button is clicked in the air(object is not standing
        # on a platform) nothing should happen.
        floor_level = center(self.position + Point(0, 10))
        if (self.world.object_at(floor_level) is None and ay < 0):
            print("TRIED AIR JUMP")
            ay = 0

        # In the formula for the position there is 0.5 * a * t^2
        # For the sake of model simplicity it is just included in the velocity.
        self.velocity += 0.5 * Point(MOVEMENT_RESISTANCE_X * ax,
                                     MOVEMENT_RESISTANCE_y * ay)

        # check if a velocity does not exceed an air resistance
        #    velocity_magnitude = self.velocity.magnitude()
        #    if (0.5 * velocity_magnitude > AIR_RESISTANCE):
        #        self.velocity /= velocity_magnitude
        #        self.velocity *= AIR_RESISTANCE

        #       #### Alternative version (it is probably better) ####
        #
        x_direction = 1 if (self.velocity.x >= 0) else -1
        y_direction = 1 if (self.velocity.y >= 0) else -1
        if (abs(self.velocity.x) > AIR_RESISTANCE):
            self.velocity.x = MOVEMENT_RESISTANCE_X * x_direction
        if (abs(self.velocity.y) > AIR_RESISTANCE):
            self.velocity.y = AIR_RESISTANCE * y_direction

    def move(self):
        """ Method changes the position of the object.
        Method uses the velocity and the current position of an object
        to determine the position of an object after the unit time.
        It changes the value of the attribute position to the new positions
        value and also in case of collision sets velocity along the appropriate
        axes to 0.
        """

        vec = Point(self.position.x, self.position.y - 0.3 * UNIT)
        vec = center(vec)
        map_object = self.world.object_at(vec)
        if (self.velocity.y < 0 and map_object is None):
            pass

        self.position += self.velocity

        # collision with walls sideways
        direction = 1 if (self.velocity.x > 0) else -1
        vec = Point(self.position.x + direction * 0.3 * UNIT, self.position.y)
        vec = center(vec)
        map_object = self.world.object_at(vec)
        if (self.velocity.x and map_object is not None):
            print("BLOCKADE " + "RIGHT" if (direction == 1) else "LEFT")
            self.position.x = map_object.position.x - direction * UNIT
            self.velocity.x = 0

        # collision check with the floor
        # +5 to assure the detection of the floor below
        # (y axis is upside down in most of graphing libraries)
        vec = Point(self.position.x, self.position.y + 0.3 * UNIT)
        vec = center(vec)

        map_object = self.world.object_at(vec)

        if (self.velocity.y and map_object is not None):
            print(f"FLOOR {self.position} --> {map_object.position}")
            self.position.y = map_object.position.y - UNIT
            self.velocity.y = 0
            self.jumping = False

        self.position.x = int(self.position.x)
        self.position.y = int(self.position.y)

    def update(self):
        """ Method updates physical status of the object.
        It uses moves and acceleration methods to move the object and apply
        gravity to it. The friction is also handled here.
        """

        # Turn on gravity only if object does not stand on a platform to make
        # an illusion of a free fall. (This prevents the object from jiggling
        # at the level of the floor and trying to accelerate through it)
        floor_level = center(self.position + Point(0, 5))
        if (self.world.object_at(floor_level) is None):
            self.accelerate(0, GRAVITY)

        # Turn on friction only if object is standing on a platform
        else:
            self.velocity.x *= FRICTION

        self.move()

    def assign_world(self, world):
        """ Every physics object needs to be in some world.
        Args:
            world: World to be a assigned to the object.
        """

        self.world = world


def center(vector):
    """ Fits vector to the center of the closest neighbouring grid cell.
    Args:
        vector: Vector stored in Point object format
    Returns:
        A centered vector - the one with the coordinates fitted to the
        center of the grind (half of the UNIT value) e.g. when unit is 10
        the grid has a centers coordinates ending with 5.
        (0,10)  (10,10)
            (5,5) - the center point of the grid cell from (0,0) to (10,10).
        (0,0)    (10,0)
    """

    # round to the tens digit.
    vector = UNIT * Point(int(vector.x / UNIT), int(vector.y / UNIT))
    vector += 0.5 * Point(UNIT, UNIT)
    return vector
