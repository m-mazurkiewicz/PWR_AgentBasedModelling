import random
import numpy as np


class GameOfLife:
    def __init__(self, height=100, width=100, density=0.2):
        self.height = height
        self.width = width
        self.density = density
        self.grid = np.zeros((width, height))
        # self.burning_trees = queue.Queue()
        # self.to_be_burn = queue.Queue()
        # self.labels = []
        # self.burned_trees = []

        for x in range(self.width):
            for y in range(self.height):
                if random.random() < self.density:
                    self.grid[x][y] = 1

    def count_living_neighbours(self, cell):
        x = cell[0]
        y = cell[1]
        living_neighbors = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (x + i >=0) and (x + i < self.width) and (y + j >=0) and (y + j < self.height) and i != 0 and j != 0:
                    if self.grid[x + i][y + j] == 1:
                        living_neighbors += 1
        return living_neighbors

    #helping method
    def print(self):
        for x in range(self.width):
            for y in range(self.height):
                print(self.grid[x][y], end=' ')
            print('\n')
