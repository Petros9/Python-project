import pygame

from settings_and_data.settings import *


class StaticObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE

    def update(self, dx):
        """ update the position on screen after hero move

        The default option is that screen chases the hero in his way to the
        right. The static objects should move along with the screen to make
        an illusion of camera tracing a player.

        Args:
            dx: The displacement of x axis position.

        """

        self.rect.x += dx

    def on_screen(self):
        return (-CELL_SIZE < self.rect.x < SCREEN_WIDTH and
                -CELL_SIZE < self.rect.y < SCREEN_HEIGHT)
