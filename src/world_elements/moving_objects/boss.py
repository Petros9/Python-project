import basic as bs
from world_elements.moving_objects.character import Character
from settings_and_data.models_and_sounds import *


class Boss(Character):
    def __init__(self, img, x, y, level):
        super().__init__(img, bs.Point(x, y), level)
        self.boss_health = 5
        self.boss_direct = bs.Direction.RIGHT
        self.immortality_timer = 0
        self.reload_timer = 0

    def jump(self):
        # Acceleration is chosen, so that boss movement is smooth.
        acceleration = 100
        if (self.boss_direct == bs.Direction.RIGHT):
            self.boss_direct = bs.Direction.LEFT
            ax = -acceleration
        else:
            self.boss_direct = bs.Direction.RIGHT
            ax = acceleration
        self.change_image()
        ay = -2 * acceleration
        self.accelerate(ax, ay)

    def take_hit(self):
        self.boss_health -= 1
        self.immortality_timer = IMMORTALITY_TIME
        if(self.boss_direct == bs.Direction.RIGHT):
            self.image = ModelsAndSounds.COMPANION_R_DAM
        else:
            self.image = ModelsAndSounds.COMPANION_L_DAM

    def change_image(self):
        if(self.boss_direct == bs.Direction.RIGHT):
            self.image = ModelsAndSounds.COMPANION_R_JUMPING
        else:
            self.image = ModelsAndSounds.COMPANION_L_JUMPING


