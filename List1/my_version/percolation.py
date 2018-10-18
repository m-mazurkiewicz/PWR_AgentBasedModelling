from List1.my_version.model import ForestFire
import numpy as np
import matplotlib.pyplot as plt

def find_percolation_threshold(height, width, density=.5):
    probability=0
    for i in range(100):
        forest = ForestFire(height, width, density)
        forest.burn_forest()
        if forest.check_if_second_edge_is_reached():
            probability +=1
    return probability/100

def calculate_threshold_for_different_densities(lowest_density=.2, highest_density=.7, number_of_densities_to_check=50):
    list_of_thresholds=dict()
    for density in np.linspace(lowest_density, highest_density, number_of_densities_to_check, endpoint=False):
        list_of_thresholds[density]=find_percolation_threshold(20, 20, density)
    return list_of_thresholds

def print_thresholds(dict_of_thresholds):
    x, y = zip(*dict_of_thresholds.items())
    plt.plot(x, y)
    plt.show()