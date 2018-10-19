import random
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.animation as animation
import queue
from collections import Counter
from List1.my_version.hoshen_kapelman import hoshen_kapelman_alghoritm


class ForestFire:
    def __init__(self, height=100, width=100, density=0.65):
        self.height = height
        self.width = width
        self.density = density
        self.grid = []
        self.burning_trees = queue.Queue()
        self.to_be_burn = queue.Queue()
        self.labels = []
        self.burned_trees = []

        for x in range(height):
            row = []
            for y in range(width):
                tree = 0
                if random.random() < self.density:
                    tree = 1
                    if x==0:
                        tree = 2
                        self.burning_trees.put((x,y))
                row.append(tree)
            self.grid.append(row)

    #helping method
    def print(self):
        for x in range(self.height):
            for y in range(self.width):
                print(self.grid[x][y], end=' ')
            print('\n')

    def burn_neighbors(self, tree):
        x = tree[0]
        y = tree[1]
        self.grid[x][y] = 3
        neighbors = []
        for i in [-1, 0, 1, 2]:        #to add wind we may just add another numbers here
            for j in [-1, 0, 1, 2]:
                if (x + i >=0) & (x + i < self.height) & (y + j >=0) & (y + j < self.height):
                    neighbors.append((x+i, y+j))
        #for more complex wind models we can do sth like that:
        # for i, j in [(1,2), (2,3)]: #and here put tuples with exact directions
        #     if (x + i >= 0) & (x + i < self.height) & (y + j >= 0) & (y + j < self.height):
        #         neighbors.append(self.grid[x + i][y + j])
        for x,y in neighbors:
            if self.grid[x][y] == 1:
                self.grid[x][y] = 2
                self.to_be_burn.put((x,y))

    def single_step(self):
        for i in range(self.burning_trees.qsize()):
            self.burn_neighbors(self.burning_trees.get())
        while not self.to_be_burn.empty():
            self.burning_trees.put(self.to_be_burn.get())

    def burn_forest(self):
        while not self.burning_trees.empty():
            self.single_step()

    def check_if_second_edge_is_reached(self):
        for i in range(self.width):
            if self.grid[self.height - 1][i] == 3:
                return True
        return False

    def animate_and_simulate(self, file_path_and_name, duration = 15):
        image_magick = animation.writers['imagemagick']
        fps = np.ceil(20/ float(duration))
        writer = image_magick(fps=fps)
        fig = plt.figure()
        ax = plt.gca()
        plt.axis('off')
        cmap = mpl.colors.ListedColormap(['white', 'green', 'red', 'black'])
        ax.imshow(self.grid, cmap=cmap)
        with writer.saving(fig, file_path_and_name+".gif", 100):
            while not self.burning_trees.empty():
                self.single_step()
                ax.imshow(self.grid, cmap=cmap)
                writer.grab_frame()

    def average_size_of_the_biggest_cluster(self):
        average_size = 0
        number_of_iterations = 0
        while not self.burning_trees.empty():
            self.single_step()
            average_size += hoshen_kapelman_alghoritm(self)
            number_of_iterations += 1
        return average_size/number_of_iterations


def average_size_as_a_function_of_density(lowest_density=.2, highest_density=.9, number_of_densities_to_check=80, width=100, height=100):
    list_of_sizes = dict()
    for density in np.linspace(lowest_density, highest_density, number_of_densities_to_check, endpoint=False):
        model = ForestFire(width, height, density)
        list_of_sizes[density] = model.average_size_of_the_biggest_cluster()
    return list_of_sizes

def plot_avg_size_of_biggest_cluster(dict_of_averages):
    x, y = zip(*dict_of_averages.items())
    plt.plot(x, y)
    plt.savefig('biggest_cluster.png')
    plt.show()