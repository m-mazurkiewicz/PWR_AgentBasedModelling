import random
import numpy as np
import pylab
from matplotlib import animation
import matplotlib.pyplot as plt


class GameOfLife:
    def __init__(self, height=100, width=100, initial_density=0.2, file_name=''):
        if len(file_name) == 0:
            self.height = height
            self.width = width
            self.initial_density = initial_density
            self.grid = np.zeros((width, height))

            for x in range(self.width):
                for y in range(self.height):
                    if random.random() < self.initial_density:
                        self.grid[x][y] = 1
        else:
            self.grid = read_grid_from_file(file_name)
            self.width = len(self.grid[0])
            self.height = len(self.grid)

    def count_living_neighbours(self, cell):
        x = cell[0]
        y = cell[1]
        living_neighbors = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (x + i >=0) and (x + i < self.width) and (y + j >=0) and (y + j < self.height) and (x+i != x or y+j != y):
                    if self.grid[x + i][y + j] == 1:
                        living_neighbors += 1
        return living_neighbors

    def one_step(self):
        new_grid = np.zeros_like(self.grid)
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] == 1:
                    if self.count_living_neighbours((x, y)) in (2, 3):
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0
                else:
                    if self.count_living_neighbours((x, y)) == 3:
                        new_grid[x][y] = 1
        self.grid = new_grid

    def play(self, number_of_iterations):
        for i in range(number_of_iterations):
            self.one_step()

    def animate_and_simulate(self, file_path_and_name, number_of_iterations, duration = 15):
        image_magick = animation.writers['imagemagick']
        fps = np.ceil(20/ float(duration))
        writer = image_magick(fps=fps)
        fig = plt.figure()
        ax = plt.gca()
        plt.axis('off')
        #cmap = mpl.colors.ListedColormap(['white', 'green', 'red', 'black'])
        ax.imshow(self.grid)#, cmap=cmap)
        with writer.saving(fig, file_path_and_name+".gif", 100):
            for i in range(number_of_iterations):
                self.one_step()
                ax.imshow(self.grid)#, cmap=cmap)
                writer.grab_frame()

    #helping method
    def print(self):
        pylab.pcolormesh(self.grid)
        pylab.show()
        # for x in range(self.width):
        #     for y in range(self.height):
        #         print(self.grid[x][y], end=' ')
        #     print('\n')


def read_grid_from_file(filename):
    grid = []
    with open(filename, 'r') as file:
    #     data = file.readlines()
    # for line in data:
    #     grid.append(line.split())
    # return grid
        lines_list = file.readlines()
    for line in reversed(lines_list):
        grid.append([int(val) for val in line.split()])
    return grid
    # for x in range(len(grid)):
    #     for y in range(len(grid[0])):
    #         print(grid[x][y], end=' ')
    #     print('\n')


if __name__ == '__main__':
    # game = GameOfLife(100, 100, .2)
    # game.animate_and_simulate('first_animation', 100)
    #game.play(5)
    #read_grid_from_file('input.txt')
    game = GameOfLife(file_name='input.txt')
    game.print()