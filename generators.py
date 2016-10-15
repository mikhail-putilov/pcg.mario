from map import Map


def generate_terrain(the_map: Map):
    list_of_random_points = [(0, 1), (30, 5), (50, 7), (55, 2), (90, 4), (99, 1)]
    for left_point, right_point in zip(list_of_random_points[:-1], list_of_random_points[1:]):
        the_map.line(left_point, right_point, the_map.ground, fill_down=True)

    random_pitfalls_xs = [31, 50]
    for pitfall_x in random_pitfalls_xs:
        the_map.make_pitfall(pitfall_x)


def generate_clouds(the_map: Map):
    random_cloud_xs = [31, 50, 100, 0]
    for cloud_x in random_cloud_xs:
        the_map.place_cloud(cloud_x, type='red')


def generate_tubes(the_map: Map):
    random_tube_xs = [60, 3]
    for random_tube_x in random_tube_xs:
        the_map.place_tube(random_tube_x)