import random

from map import Map


def generate_terrain(the_map: Map):
    iterations = random.randint(4, 6)
    list_of_random_points = [] #[(0, 1), (30, 5), (50, 7), (55, 2), (90, 4), (99, 1)]
    for i in range(iterations):
        x = random.randint(3, 96)
        while x in [tup[0] for tup in list_of_random_points]:
            x = random.randint(3, 96)
        y = random.randint(2, 7)
        list_of_random_points.append((x, y))
    list_of_random_points.append((0, 1))
    list_of_random_points.append((99, 1))
    list_of_random_points = sorted(list_of_random_points, key=lambda tup: tup[0])
    for left_point, right_point in zip(list_of_random_points[:-1], list_of_random_points[1:]):
        the_map.line(left_point, right_point, the_map.ground, fill_down=True)

    random_pitfalls_xs = [31, 50]
    for pitfall_x in random_pitfalls_xs:
        the_map.make_pitfall(pitfall_x)


def generate_clouds(the_map: Map):
    iterations = random.randint(10, 20)
    random_cloud_xs = []
    for i in range(iterations):
        x = random.randint(0, 100)
        number_of_try = 0
        while {x, x + 1, x + 2}.intersection(random_cloud_xs) and number_of_try != 10:
            x = random.randint(0, 100)
            number_of_try += 1
        if number_of_try == 10:
            break
        random_cloud_xs.append(x)

    for cloud_x in random_cloud_xs:
        the_map.place_cloud(cloud_x, type='red')


def generate_tubes(the_map: Map):
    iterations = random.randint(5, 20)
    random_tube_xs = []
    for i in range(iterations):
        x = random.randint(4, 100)
        number_of_try = 0
        while {x, x + 1}.intersection(random_tube_xs) and number_of_try != 10:
            x = random.randint(4, 100)
            number_of_try += 1
        if number_of_try == 10:
            break
        random_tube_xs.append(x)

    for random_tube_x in random_tube_xs:
        the_map.place_tube(random_tube_x)


def generate_question_blocks(the_map: Map):
    iterations = random.randint(5, 10)
    random_question_xs = []
    for i in range(iterations):
        x = random.randint(4, 100)
        number_of_try = 0
        while {x, x + 1, x+2, x+3}.intersection(random_question_xs) and number_of_try != 10:
            x = random.randint(4, 100)
            number_of_try += 1
        if number_of_try == 10:
            break
        random_question_xs.append(x)

    for random_question_x in random_question_xs:
        the_map.place_question_block(random_question_x)


def generate_cave(the_map: Map):
    random_cave_xss = [(random.randint(40,50), random.randint(5, 10))]
    for random_cave_x1, random_cave_x2 in random_cave_xss:
        the_map.place_cave(random_cave_x1, random_cave_x2)


def generate_bushes(the_map: Map):
    iterations = random.randint(5, 10)
    random_bushes_xs = []
    for i in range(iterations):
        x = random.randint(4, 100)
        number_of_try = 0
        while {x, x + 1, x + 2, x + 3}.intersection(random_bushes_xs) and number_of_try != 10:
            x = random.randint(4, 100)
            number_of_try += 1
        if number_of_try == 10:
            break
        random_bushes_xs.append(x)
    for random_bush_x in random_bushes_xs:
        the_map.place_bush(random_bush_x)


def generate_eminems(the_map: Map):
    iterations = random.randint(20, 30)
    random_bushes_xs = []
    for i in range(iterations):
        x = random.randint(10, 100)
        number_of_try = 0
        while x in random_bushes_xs and number_of_try != 10:
            x = random.randint(10, 100)
            number_of_try += 1
        if number_of_try == 10:
            break
        random_bushes_xs.append(x)
    for random_bush_x in random_bushes_xs:
        the_map.generate_eminem(random_bush_x)