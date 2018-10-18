from List1.my_version.model import ForestFire, average_size_as_a_function_of_density, plot_avg_size_of_biggest_cluster
from List1.my_version.percolation import find_percolation_threshold, calculate_threshold_for_different_densities, plot_thresholds
# from List1.my_version.test import Solution
from List1.my_version.hoshen_kapelman import hoshen_kapelman_alghoritm


def main():
    plot_thresholds(calculate_threshold_for_different_densities(width=20, height=20))
    print(calculate_threshold_for_different_densities())

    list = average_size_as_a_function_of_density()
    plot_avg_size_of_biggest_cluster(list)
    print(list)


if __name__ == '__main__':
    main()
