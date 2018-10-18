from List1.my_version.model import ForestFire
import numpy as np

def find_percolation_threshold(height, width):
    for density in np.linspace(.01, 1, 99, endpoint=False):
        forest = ForestFire(height, width, density)
        forest.burn_forest()
        if forest.check_if_second_edge_is_reached():
            return density