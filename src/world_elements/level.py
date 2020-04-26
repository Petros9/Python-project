import random

from world_elements.hero import Hero
from world_elements.foe import Foe
from world_elements.flag import Flag
from world_elements.bullet import Bullet
from world_elements.platform import Platform
from world_elements.tower import Tower


class Level:
    def __init__(self, objects):
        self.hero = Hero(self)
        self.tower_list = []  # '' wiezyczki beda strzelaly w dol co jakiś czas
        self.objects = objects
        self.level_objects = {}
        self.foes_list = []
        self.place_objects(objects)
        self.bullets_list = []

    # '' przesuwanie sie wrgow czyszczenie wrogow itd
    # '' trzeba zrobić, by wrogowie nie spadali z platform

    def object_at(self, point):
        if ((point.x, point.y) in self.level_objects):
            map_object = self.level_objects.get((point.x, point.y))

            if (isinstance(map_object, Flag)):
                if (not map_object.captured):
                    self.hero.spawn.change_spawn(point.x, point.y)
                    map_object.capture()
                return None
            elif (isinstance(map_object, Foe)):
                self.hero.take_hit()
            return map_object
        else:
            return None

    def place_objects(self, objects):
        for object in objects:
            self.level_objects[(object.position.x,
                                object.position.y)] = object
            self.foes_list = list(
                filter(lambda object: isinstance(object, Foe), objects))
            self.tower_list = list(
                filter(lambda object: isinstance(object, Tower), objects))

    def shoot(self, x, y, x_direction, y_direction):
        bullet = Bullet(x, y, x_direction, y_direction)
        self.level_objects[(bullet.position.x, bullet.position.y)] = bullet
        self.bullets_list += [bullet]

    def move_bullets(self):
        for bullet in self.bullets_list:
            bullet.move()
            if (bullet.position.__eq__(self.hero.position)):

                if (not self.hero.squat):
                    self.hero.take_hit()
                    self.bullets_list.remove(bullet)
            else:
                map_object = self.object_at(bullet.position)

                if (isinstance(map_object, Foe)):
                    map_object.take_hit()
                    self.bullets_list.remove(bullet)

                elif (isinstance(map_object, Platform)):
                    self.bullets_list.remove(bullet)

    def shoot_towers(self):
        random.seed()
        for tower in self.tower_list:
            if (random.randint(0, 20) % 11 == 0):
                self.shoot(tower.position.x, tower.position.y + 5, 0, 3)

    def move_foes(self):
        for foe in self.foes_list:
            foe.move()
