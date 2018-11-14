import numpy as np


class ShellingSegregation:
    def __init__(self, number_of_blue_agents, number_of_red_agents, number_of_rows=100, number_of_columns=100):
        self.number_of_blue_agents = number_of_blue_agents
        self.number_of_red_agents = number_of_red_agents
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.grid = np.array(self.number_of_blue_agents * [1] + self.number_of_red_agents * [2] + (self.number_of_rows * self.number_of_columns - self.number_of_red_agents - self.number_of_blue_agents) * [0])
        np.random.shuffle(self.grid)
        self.grid = self.grid.reshape(self.number_of_rows, self.number_of_columns)

    def print(self):
        for i in range(self.number_of_rows):
            for j in range(self.number_of_rows):
                print(self.grid[i][j], end=' ')
            print('\n')


if __name__ == '__main__':
    test = ShellingSegregation(50,15,20,20)
    test.print()