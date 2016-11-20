import random
from itertools import repeat

from configuration import map_width, map_height


class Map(object):
    def __init__(self):
        self.width = map_width
        self.height = map_height
        self.background = 1
        self.ground = 2
        self.question_block = 8
        self.map = []
        self.coin = 6 + 22 * 5
        # fill background
        for i in range(self.height):
            self.map.append(list(repeat(self.background, self.width)))

    def set_point(self, x, y, value):
        if x < 0 or x >= self.width:
            raise Exception('x value is illegal')
        if y < 0 or y >= self.height:
            raise Exception('y value is illegal')
        self.map[y][x] = value

    def line(self, point0: (int, int), point1: (int, int), color: int, fill_down=False):
        x0, y0 = point0
        x1, y1 = point1

        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = int(x1 - x0)
        dy = int(y1 - y0)
        derror = float(abs(dy / float(dx)))
        error = float(0)
        y = int(y0)
        for x in range(x0, x1 + 1):
            if steep:
                self.set_point(y, x, color)
                if fill_down:
                    for row in range(x):
                        self.set_point(y, row, color)
            else:
                self.set_point(x, y, color)
                if fill_down:
                    for row in range(y):
                        self.set_point(x, row, color)

            error += derror

            if error > .5:
                y += 1 if y1 > y0 else -1
                error -= 1.

    def export(self, filename):
        with open(filename, mode="w") as f:
            exported = []
            for line in reversed(self.map):
                exported.append(','.join([str(x) for x in line]))
            f.write(','.join(exported) + ';background=1;spriteset=1;music=2;timelimit=400\n')

    def make_pitfall(self, start_x):
        width_of_pitfall = 5
        for x in range(start_x, start_x + width_of_pitfall):
            for y in range(self.height):
                if self.map[y][x] != self.background:
                    self.map[y][x] = self.background
                else:
                    continue

    def place_cloud(self, start_x, type='blue'):
        if type == 'blue':
            cloud = [
                [11 + 44, 12 + 44, 13 + 44],
                [11 + 22, 12 + 22, 13 + 22]
            ]
        elif type == 'red':
            cloud = [
                [8 + 44, 9 + 44, 10 + 44],
                [8 + 22, 9 + 22, 10 + 22]
            ]
        else:
            raise Exception('only red or blue are supported')
        initial_height = random.choice([10, 11, 12])
        for y, cloud_row in enumerate(cloud):
            for x, cloud_val in enumerate(cloud_row):
                self.map[y + initial_height][x + start_x] = cloud_val

    def place_tube(self, tube_x):
        tube_top = [16, 17]
        tube_body = [16 + 22, 17 + 22]
        height_counter = 0
        max_height = 4
        for y in range(self.height):
            llhs = self.map[y][tube_x - 1]
            lhs = self.map[y][tube_x]
            rhs = self.map[y][tube_x + 1]
            if not self.is_collider(llhs) or not self.is_collider(lhs):
                height_counter += 1
                self.map[y][tube_x] = tube_body[0]
            if not self.is_collider(rhs):
                self.map[y][tube_x + 1] = tube_body[1]
            if height_counter == max_height:
                self.map[y][tube_x] = tube_top[0]
                self.map[y][tube_x + 1] = tube_top[1]
                return

    def place_question_block(self, question_x):
        max_height = 5
        height_counter = 0
        for y in range(self.height):
            if not self.is_collider(self.map[y][question_x]):
                height_counter += 1
            if height_counter == max_height:
                if self.is_collider(self.map[y - 1][question_x + 1]) or self.is_collider(
                        self.map[y - 1][question_x - 1]):
                    return
                self.map[y][question_x] = self.question_block
                return

    @staticmethod
    def is_collider(value):
        return value in \
               [2, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                1 + 22, 7 + 22, 14 + 22, 15 + 22, 16 + 22, 17 + 22, 18 + 22, 19 + 22, 20 + 22, 21 + 22, 22 + 22]

    def place_cave(self, cave_x1, cave_x2):
        number_of_rooms = 1
        width = abs(cave_x2 - cave_x1)
        way_up_x = int((cave_x1 + cave_x2) / 2)
        way_up_y = None
        for y in range(self.height):
            if not self.is_collider(self.map[y][way_up_x]):
                way_up_y = y - 1
                break
        # dig
        min_depth = 2
        current_depth = 0
        cave_starts_y = None
        for y in range(way_up_y, 0, -1):
            current_depth += 1
            if self.is_cave_placeable(cave_x1, cave_x2, y) and current_depth >= min_depth:
                cave_starts_y = y
                for x in range(cave_x1, cave_x2 + 1):
                    self.map[y][x] = self.coin

        for y in range(way_up_y, cave_starts_y, -1):
            self.map[y][way_up_x] = self.coin

    def is_cave_placeable(self, cave_x1, cave_x2, y):
        for x in range(cave_x1, cave_x2 + 1):
            if not self.is_collider(self.map[y - 1][x]):
                return False
            if not self.is_collider(self.map[y][x]):
                return False
            if not self.is_collider(self.map[y + 1][x]):
                return False
        return True

    def place_bush(self, bush_x):
        bush = [4, 5, 6]
        current_x = bush_x
        for current_x in range(current_x, current_x + 10):
            ground_y = self.choose_ground_y(current_x)
            if not (self.map[ground_y][current_x] == self.background and self.map[ground_y][
                    current_x + 1] == self.background and self.map[ground_y][current_x + 2] == self.background):
                continue
            for i in range(3):
                self.map[ground_y][current_x + i] = bush[i]
            return

    def choose_ground_y(self, x):
        for y in range(self.height):
            if not self.is_collider(self.map[y][x]) and not self.is_bush(self.map[y][x]):
                return y
        return None

    def is_bush(self, param):
        return param in [4, 5, 6]

    def generate_eminem(self, random_eminem_x):
        if self.map[self.height-1][random_eminem_x] == 1:
            self.map[self.height-1][random_eminem_x] = random.choice(["1-5", "1-6"])
            print("eminem!")


the_map = Map()
