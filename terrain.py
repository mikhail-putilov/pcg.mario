from map import Map


def generate_terrain(the_map: Map):
    list_of_random_points = [(0, 1), (30, 5), (50, 7), (55, 2), (90, 4), (99, 1)]
    for left_point, right_point in zip(list_of_random_points[:-1], list_of_random_points[1:]):
        the_map.line(left_point, right_point, 2, fill_down=True)

    random_pitfalls_x = [31, 50]
    for pitfall_x in random_pitfalls_x:
        the_map.make_pitfall(pitfall_x)
