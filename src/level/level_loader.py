from collections import defaultdict

import pygame

from settings_and_data.settings import *
import world_elements as we
from level.level import Level


class LevelLoader:
    """ Class handles input of level.

    Attributes:
        object_images(dict): Dictionary with keys being names of some level
                             objects f.e. 'foe' and images assigned to them.

    """

    PLATFORM_SYMBOL = '#'
    FLAG_SYMBOL = '$'
    FOE_SYMBOL = '*'
    TOWER_SYMBOL = '^'
    BOSS_SYMBOL = '@'
    BRIDGE_SYMBOL = '&'

    def __init__(self, object_images):
        self.object_images = object_images

    def load_level(self, pathname):
        """ Load level from a file.

        Args:
            pathname: Path to a file.

        Returns:
            Level: The Level object filled with contents of a level
                encrypted in file, whose name is self.filename.
        """

        level = Level(all_platforms=None, floors=None,
                      walls=None, corners=None,
                      foes=pygame.sprite.Group(),
                      towers=pygame.sprite.Group(),
                      bridges=pygame.sprite.Group(),
                      flags=pygame.sprite.Group(),
                      bosses=pygame.sprite.Group())

        platforms = []
        platform_is_at = defaultdict(lambda: False)

        try:
            with open(pathname, 'r') as f:
                for i, line in enumerate(f):
                    for j in range(len(line)):

                        if (line[j] == LevelLoader.PLATFORM_SYMBOL):
                            platforms += [
                                we.Platform(self.object_images['platform'],
                                            0.5 * j, i)]
                            platform_is_at[(platforms[-1].rect.x,
                                            platforms[-1].rect.y)] = True
                        if (line[j] == LevelLoader.FLAG_SYMBOL):
                            level.flags.add(
                                [we.Flag(self.object_images['flag'],
                                         0.5 * j, i)])
                        if (line[j] == LevelLoader.FOE_SYMBOL):
                            level.foes.add(
                                [we.Foe(self.object_images['foe'], 0.5 * j, i,
                                        level)])
                        if (line[j] == LevelLoader.TOWER_SYMBOL):
                            level.towers.add(
                                [we.Tower(self.object_images['tower'],
                                          0.5 * j, i)])

                        if (line[j] == LevelLoader.BOSS_SYMBOL):
                            level.bosses.add([we.Boss(
                                self.object_images['boss'],
                                0.5 * j, i, level)])

                        if (line[j] == LevelLoader.BRIDGE_SYMBOL):
                            bridge = we.Bridge(self.object_images['bridge'],
                                               0.5 * j, i)
                            level.bridges.add([bridge])

                            # Bridges are (for some time only) behaving like
                            # floor platform - treat them as one.
                            platform_is_at[(bridge.rect.x,
                                            bridge.rect.y)] = True
        except IOError as er:
            print(f"I/O error in loading level: " + er.strerror)

        # Platforms classification
        level.walls = pygame.sprite.Group(filter(lambda p: (
                LevelLoader.has_vertical_neighbors(platform_is_at, p) and
                not LevelLoader.has_horizontal_neighbors(platform_is_at, p)
        ), platforms))

        level.floors = pygame.sprite.Group(filter(lambda p: (
                not LevelLoader.has_vertical_neighbors(platform_is_at, p) and
                LevelLoader.has_horizontal_neighbors(platform_is_at, p)
        ), platforms))
        level.corners = pygame.sprite.Group(filter(lambda p: (
                LevelLoader.has_horizontal_neighbors(platform_is_at, p) and
                LevelLoader.has_vertical_neighbors(platform_is_at, p)
        ), platforms))
        level.all_platforms = pygame.sprite.Group(platforms)

        return level

    @staticmethod
    def has_vertical_neighbors(platform_is_at, plat):
        return (platform_is_at[(plat.rect.x, plat.rect.y - CELL_SIZE)] or
                platform_is_at[(plat.rect.x, plat.rect.y + CELL_SIZE)])

    @staticmethod
    def has_horizontal_neighbors(platform_is_at, plat):
        return (platform_is_at[(plat.rect.x - CELL_SIZE, plat.rect.y)] or
                platform_is_at[(plat.rect.x + CELL_SIZE, plat.rect.y)])
