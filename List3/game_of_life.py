import random
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt


class GameOfLife:
    def __init__(self, height=100, width=100, initial_density=0.2, file_name='', padding=0):
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
            self.grid = read_grid_from_conway_file(file_name)
            #self.grid = read_grid_from_file(file_name)
            self.height = len(self.grid[0])
            self.width = len(self.grid)
        if padding > 0:
            self.add_padding(padding)

    def add_padding(self, padding):
        extended_grid = np.zeros((padding, 2*padding + len(self.grid[0])), int).tolist()
        for i in range(len(self.grid)):
            extended_grid.append(padding * [0] + self.grid[i] + padding * [0])
        extended_grid.extend(np.zeros((padding, 2*padding + len(self.grid[0])), int).tolist())
        self.grid = extended_grid
        self.height = len(self.grid[0])
        self.width = len(self.grid)

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

    def animate_and_simulate(self, file_path_and_name, number_of_iterations, duration=15):
        image_magick = animation.writers['imagemagick']
        fps = np.ceil(20 / float(duration))
        writer = image_magick(fps=fps)
        fig = plt.figure()
        ax = plt.gca()
        plt.axis('off')
        # cmap = mpl.colors.ListedColormap(['white', 'green', 'red', 'black'])
        ax.imshow(self.grid)#, cmap=cmap)
        with writer.saving(fig, file_path_and_name+".gif", 100):
            writer.grab_frame()
            for i in range(number_of_iterations):
                self.one_step()
                ax.imshow(self.grid)#, cmap=cmap)
                writer.grab_frame()

    # helping method
    def print(self):
        ax = plt.gca()
        ax.imshow(self.grid)
        plt.show()


def read_grid_from_file(filename):
    with open(filename, 'r') as file:
        lines_list = file.readlines()
    grid = [[int(val) for val in line.split()] for line in lines_list]
    return grid


def read_grid_from_conway_file(filename):
    with open(filename, 'r') as file:
        lines_list = file.readlines()
    grid =[]
    longest_line = 0
    for line in lines_list:
        to_append = []
        line_length = 0
        for val in list(line):
            to_append.append(1 if val == 'O' else 0)
            line_length += 1
        del to_append[-1]
        grid.append(to_append)
        longest_line = max(longest_line, line_length - 1)
    grid[-1].append(1)
    for i in range(len(grid)):
        if len(grid[i]) < longest_line:
            for j in range(len(grid[i]), longest_line):
                grid[i].append(0)
    return grid

if __name__ == '__main__':
    # game = GameOfLife(50, 50, .2)
    # game.print()
    # game.animate_and_simulate('first_animation', 50)
    game = GameOfLife(file_name='1stInput.txt', padding=2)
    game.animate_and_simulate('animation_on_input_grid', 20)
    # input = read_grid_from_conway_file('1stInput.txt')
    # print(input)