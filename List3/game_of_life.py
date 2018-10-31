import random
import numpy as np


class GameOfLife:
    def __init__(self, height=100, width=100, density=0.65):
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
