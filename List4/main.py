import sys
import os
from os.path import dirname
sys.path.append(dirname(__file__))
# from List4.schelling_segregation import Grid
from schelling_segregation import Grid

num_of_type_0 = int(sys.argv[1])
num_of_type_1 = int(sys.argv[2])
num_neighbors_0 = int(sys.argv[3])
num_neighbors_1 = int(sys.argv[4])
staying_threshold_0 = float(sys.argv[5])
staying_threshold_1 = float(sys.argv[6])
max_number_of_iterations = int(sys.argv[7])
file_name = sys.argv[8]

grid = Grid(num_of_type_0, num_of_type_1, num_neighbors_0, num_neighbors_1, staying_threshold_0, staying_threshold_1)
grid.run_algorithm(max_number_of_iterations, plot_n_print=False)
os.makedirs('figures', exist_ok=True)
grid.plot('figures/'+file_name)