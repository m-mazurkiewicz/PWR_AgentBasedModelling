import random
import numpy as np
import pylab


class GameOfLife:
    def __init__(self, height=100, width=100, initial_density=0.2):
        self.height = height
        self.width = width
        self.initial_density = initial_density
        self.grid = np.zeros((width, height))

        for x in range(self.width):
            for y in range(self.height):
                if random.random() < self.initial_density:
                    self.grid[x][y] = 1

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

    #helping method
    def print(self):
        pylab.pcolormesh(self.grid)
        pylab.show()
        # for x in range(self.width):
        #     for y in range(self.height):
        #         print(self.grid[x][y], end=' ')
        #     print('\n')


if __name__ == '__main__':
    game = GameOfLife(10, 10, .2)
    game.play(5)