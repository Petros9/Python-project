import pygame

import world_elements as we
from basic.point import Point
from settings_and_data.models_and_sounds import ModelsAndSounds
from settings_and_data.settings import *


class Level:
    """ Level and its whole functionality.
    """

    def __init__(self, all_platforms, floors, walls, corners, foes, towers,
                 bridges, flags, bosses, heroes=None, spawn=None):
        self.spawn = spawn if (spawn) else we.Spawn()
        self.all_platforms = all_platforms
        self.floors = floors
        self.walls = walls
        self.corners = corners
        self.foes = foes
        self.towers = towers
        self.bridges = bridges
        self.flags = flags
        self.heroes = heroes if (heroes) else pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bosses = bosses
        self.end_game = False

    def shoot(self, start_position, velocity):
        ModelsAndSounds.FOE_SHOOT_SOUND.play()
        self.bullets.add(we.Bullet(ModelsAndSounds.BULLET_IMG, start_position,
                                   velocity))

    def move_bullets(self):
        self.bullets.update()

        for hero in self.heroes:
            bullets_colliding = pygame.sprite.spritecollide(hero,
                                                            self.bullets,
                                                            False)
            for bullet in bullets_colliding:
                if (hero.squat and
                        bullet.rect.y < hero.position.y + 0.3 * CELL_SIZE):
                    continue
                self.bullets.remove(bullet)
                hero.take_hit()

            if (hero.health == 0):
                hero.die()

        for foe in self.foes:
            if (pygame.sprite.spritecollide(foe, self.bullets, True)):
                foe.take_hit()

            if (foe.foe_health == 0):
                self.foes.remove(foe)

        for boss in self.bosses:
            if (pygame.sprite.spritecollide(boss, self.bullets, True)):
                boss.take_hit()
            if (boss.boss_health == 0):
                self.bosses.remove(boss)
                self.end_game = True

        def inside_screen_area(current_bullet):
            return (2 * SCREEN_WIDTH > current_bullet.rect.x > -SCREEN_WIDTH or
                    2 * SCREEN_HEIGHT > current_bullet.rect.y > -SCREEN_HEIGHT)

        self.bullets = pygame.sprite.Group(filter(inside_screen_area,
                                                  self.bullets))

    def move_foes(self):
        for hero in self.heroes:
            if (pygame.sprite.spritecollide(hero, self.foes, False)):
                hero.take_hit()
            if (hero.health == 0):
                hero.die()

        for foe in self.foes:
            if (foe.immortality_timer > 0):
                foe.immortality_timer -= 1
            else:
                foe.change_image()
            if (foe.reload_timer == 0):
                if (foe.bullets == 0):
                    foe.reload_timer = FOE_RELOAD_TIME
                    foe.bullets = FOE_BULLETS_PER_BURST
                else:
                    for hero in self.heroes:
                        if (foe.reaches(hero.position)):
                            foe.shoot()
                            foe.bullets -= 1
                            foe.reload_timer = FOE_TIME_BETWEEN_BULLETS_IN_BURST  # noqa
            else:
                foe.reload_timer -= 1

    def shoot_towers(self):
        for tower in self.towers:
            if (tower.reload_timer == 0):
                if (tower.bullets == 0):
                    tower.reload_timer = TOWER_RELOAD_TIME
                    tower.bullets = TOWER_BULLETS_PER_BURST
                else:
                    self.shoot(Point(tower.rect.x + 15, tower.rect.y + 30),
                               Point(0, 3))
                    tower.bullets -= 1
                    tower.reload_timer = TOWER_TIME_BETWEEN_BULLETS_IN_BURST
            else:
                tower.reload_timer -= 1

    def move_boss(self):
        for hero in self.heroes:
            if (pygame.sprite.spritecollide(hero, self.bosses, False)):
                hero.take_hit()
            if (hero.health == 0):
                hero.die()
        for boss in self.bosses:
            print(boss.boss_health)
            print(boss.position.y)
            if (not 500 > boss.position.y > 0):
                self.bosses.remove(boss)
                self.end_game = True

            if (boss.immortality_timer > 0):
                boss.immortality_timer -= 1
            else:
                boss.change_image()
            if (boss.ground_detector.is_on_ground()):
                boss.jump()
            if (boss.reload_timer == 0):
                boss.reload_timer = TOWER_RELOAD_TIME
                self.shoot(Point(boss.rect.x + 15, boss.rect.y + 50),
                           Point(0, 30))
                boss.reload_timer = 2
            else:
                boss.reload_timer -= 1

    def follow_hero(self, dx):
        """ Move objects to make the camera follow the hero.
        """

        self.all_platforms.update(dx)
        self.flags.update(dx)
        self.bridges.update(dx)
        self.towers.update(dx)

        for bullet in self.bullets:
            bullet.rect.x += dx

        for hero in self.heroes:
            hero.position += Point(dx, 0)

        for foe in self.foes:
            foe.position += Point(dx, 0)

    def update_bridges_statuses(self):
        bridges_alive = []

        for bridge in self.bridges:
            if (bridge.timer > 0):
                bridge.timer -= 1
            if (bridge.timer != 0):
                bridges_alive += [bridge]

        self.bridges = pygame.sprite.Group(bridges_alive)
