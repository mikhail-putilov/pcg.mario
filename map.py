from itertools import repeat
from configuration import map_width, map_height


class Map(object):
    def __init__(self):
        self.width = map_width
        self.height = map_height
        self.background = 1
        self.map = []
        # fill background
        for i in range(map_height):
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
        initial_height = 10
        for y, cloud_row in enumerate(cloud):
            for x, cloud_val in enumerate(cloud_row):
                self.map[y + initial_height][x + start_x] = cloud_val


the_map = Map()
