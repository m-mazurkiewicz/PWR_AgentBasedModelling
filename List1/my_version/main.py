from List1.my_version.model import ForestFire
from List1.my_version.percolation import find_percolation_threshold, calculate_threshold_for_different_densities, print_thresholds
# from List1.my_version.test import Solution


def main():
    # model = ForestFire(10, 10, .5)
    # #model.print()
    # model.burn_forest()
    # model.print()
    # print('\n')
    # #model.hohesh_kopelman()
    # model.hoshen_kapelman_alghoritm()
    # model.print()
    #print(model.labels)
    #print(model.biggest_cluster())
    # model.animate_and_simulate('elo')
    # model.print()
    #hoshen_kapelman_alghoritm(model)
    # claster = Solution(model.grid)
    # result = claster.largestIsland()
    # print(result)
    # claster.print()
    print_thresholds(calculate_threshold_for_different_densities())
    #print(calculate_threshold_for_different_densities())

if __name__ == '__main__':
    main()
