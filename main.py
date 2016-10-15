from map import the_map
from generators import generate_terrain, generate_clouds, generate_tubes

generate_terrain(the_map)
generate_clouds(the_map)
generate_tubes(the_map)
the_map.export(r'/Users/mputilov/Library/Application Support/LOVE/mari0/mappacks/custom_mappack_1/1-1.txt')
