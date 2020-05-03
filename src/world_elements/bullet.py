import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, img, start_position, velocity):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = start_position.x
        self.rect.y = start_position.y
        self.velocity = velocity

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
