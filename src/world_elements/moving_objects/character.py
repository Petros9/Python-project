import pygame

import basic as bs
from settings_and_data.settings import *


class Character(pygame.sprite.Sprite):
    """
    Class character implements basics of motion and collision detection
    for characters in the game.

    Attributes:
        position(Point obj):
        velocity(Point obj):
        world(Level obj):

    """

    def __init__(self, img, position, world, velocity=None):
        super().__init__()
        self.image = img
        self.position = position * CELL_SIZE
        self.rect = pygame.sprite.Rect(position.x, position.y,
                                       0.5 * CELL_SIZE, CELL_SIZE)
        self.acceleration = bs.Point(0, 0)
        self.velocity = bs.Point(0, 0) if (velocity is None) else velocity
        self.world = world if (world is not None) else None
        self.jumping = False
        self.ground_detector = GroundDetector(
            self.position + bs.Point(0, CELL_SIZE), self.world)
        self.direction = bs.Direction.RIGHT

    def accelerate(self, ax, ay):
        """ Change the velocity of the object.

        Args:
            ax: Acceleration in the direction of the x axis.
            ay: Acceleration in the direction of the y axis.

        """

        # Do not let jump, if not on a solid ground.
        if (not self.ground_detector.is_on_ground() and ay < 0):
            ay = 0

        # Actual acceleration.
        self.acceleration += bs.Point(ax / INERTIA_X, ay / INERTIA_Y)
        self.velocity += self.acceleration

        # Speed limit in each direction.
        x_direction = 1 if (self.velocity.x > 0) else -1
        y_direction = 1 if (self.velocity.y > 0) else -1
        if (abs(self.velocity.x) > SPEED_LIMIT):
            self.velocity.x = SPEED_LIMIT * x_direction
        if (abs(self.velocity.y) > SPEED_LIMIT):
            self.velocity.y = SPEED_LIMIT * y_direction

        # Set directions
        if (self.velocity.x > 0):
            self.direction = bs.Direction.RIGHT
        elif (self.velocity.x < 0):
            self.direction = bs.Direction.LEFT

    def move(self):
        """ Change the position of the object.

        Method uses the velocity and the current position of an object
        to determine the position of an object after the unit time.
        It changes the value of the attribute position to the new positions
        value and also in case of collision sets velocity along the appropriate
        axes to 0.

        """

        # Move.
        old_position = self.position
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)
        self.ground_detector.update(self.rect)

        # Handle collisions.
        # Complexity is constant, because the character is allowed to
        # have only 8 neighboring sprites being platform or bridge.
        # In practise there is up to 3 (or 4) collisions possible.
        collisions = (
                pygame.sprite.spritecollide(self, self.world.floors, False) +
                pygame.sprite.spritecollide(self, self.world.corners, False) +
                pygame.sprite.spritecollide(self, self.world.bridges, False)
        )
        
        ground_collisions = self.ground_detector.ground_sprites()

        for collision in collisions:
            if (collision in ground_collisions and
                    old_position.y + CELL_SIZE <= collision.rect.top):
                self.rect.bottom = collision.rect.top
                self.velocity.y = 0

        # Check collisions with walls - horizontal ones
        collisions = (
                pygame.sprite.spritecollide(self, self.world.walls, False) +
                pygame.sprite.spritecollide(self, self.world.corners, False)
        )

        for collision in collisions:
            if (collision.rect.centerx > self.rect.centerx):
                self.rect.right = collision.rect.left
                self.velocity.x = 0
            else:
                self.rect.left = collision.rect.right
                self.velocity.x = 0

        # Update position after collisions.
        self.position.x = self.rect.x
        self.position.y = self.rect.y
        self.ground_detector.update(self.rect)

        # Clear the acceleration to avoid jiggling on the floor (it simulates
        # reaction force of the ground)- the 'update' method will take care
        # of gravity.
        self.acceleration = bs.Point(0, 0)

    def update(self):
        """ Update physical status of the object.

        It uses moves and acceleration methods to move the object and apply
        gravity to it. The friction and air resistance is also handled here.

        """

        self.accelerate(0, GRAVITY)
        if (not self.ground_detector.is_on_ground()):
            self.velocity.x *= AIR_RESISTANCE
        else:
            self.velocity.x *= FRICTION

        # Updating physics object attributes
        self.move()

    def adjust_visual(self):
        """ Adjust a character rect to the position image should be drawn.

        A character image is CELL_SIZE x CELL_SIZE size, but its visual
        presentation suggests, that it occupies only half of this square.
        Therefore, the rect representing a character should occupy only the
        half of the square image. To make drawing proper,
        the translation of a rect attribute to the left is performed after
        the update (the best moment to adjust is right before drawing a
        character). The relative misplacement of the rect attribute
        to the position is taken care of in the next update, when rect
        values are assigned according to the real position value stored in
        attribute position.
        """

        if (self.direction is bs.Direction.LEFT):
            self.rect.x -= 0.5 * CELL_SIZE


class GroundDetector(pygame.sprite.Sprite):
    """ It is an object, whose only function is to detect ground.

    It is placed one y position below a Character. Its main functionality
    is to say if the jump is possible and help detect collisions with the
    ground.

    """

    def __init__(self, position, world):
        super().__init__()
        self.world = world
        self.image = pygame.Surface((0.5 * CELL_SIZE, 2))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y + CELL_SIZE

    def is_on_ground(self):
        """ Returns true if corresponding Character is on a platform.

        Returns:
            bool: True if ground collision was detected.

        """
        return bool(self.ground_sprites())

    def ground_sprites(self):
        """ Sprites colliding with the GD.
        
        Returns:
            list: All sprites, with which GroundDetector collides.
        """
        return (pygame.sprite.spritecollide(self, self.world.floors, False) +
                pygame.sprite.spritecollide(self, self.world.corners, False) +
                pygame.sprite.spritecollide(self, self.world.bridges, False))

    def update(self, rect):
        self.rect.x = rect.x
        self.rect.y = rect.y + CELL_SIZE
