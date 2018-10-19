from List1.my_version.model import ForestFire, average_size_as_a_function_of_density, plot_avg_size_of_biggest_cluster
from List1.my_version.percolation import find_percolation_threshold, calculate_threshold_for_different_densities, plot_thresholds
from List1.my_version.hoshen_kapelman import hoshen_kapelman_alghoritm


def main():
    model = ForestFire()
    model.animate_and_simulate('simulation_100_by_100_wind')

    # plot_thresholds(calculate_threshold_for_different_densities(width=100, height=100))
    # print(calculate_threshold_for_different_densities())
    #
    # list_of_averages = average_size_as_a_function_of_density()
    # plot_avg_size_of_biggest_cluster(list_of_averages)
    # print(list_of_averages)


if __name__ == '__main__':
    main()
