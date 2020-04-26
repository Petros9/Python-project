from world_elements.platform import Platform
from world_elements.flag import Flag
from world_elements.foe import Foe
from world_elements.tower import Tower
from world_elements.bridge import Bridge


class LevelLoader:
    def __init__(self, filename):
        self.filename = filename

    def load_level(self):
        level_objects = []

        def set_position(x, y):
            return (5 * y + 5, 10 * x + 5)

        try:
            with open(self.filename, 'r') as f:
                for i, line in enumerate(f):
                    for j in range(len(line)):
                        if (line[j] == '#'):
                            level_objects += [Platform(*set_position(i, j))]
                        if (line[j] == '$'):
                            level_objects += [Flag(*set_position(i, j))]
                        if (line[j] == '*'):
                            level_objects += [Foe(*set_position(i, j))]
                        if (line[j] == '^'):
                            level_objects += [Tower(*set_position(i, j))]
                        if (line[j] == '&'):
                            level_objects += [Bridge(*set_position(i, j))]

        except IOError as er:
            print(f"I/O error: {er.strerror}")

        return level_objects
