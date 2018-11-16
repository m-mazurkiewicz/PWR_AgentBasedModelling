import numpy as np
import random
from sklearn.neighbors import NearestNeighbors


class ShellingSegregation:
    def __init__(self, number_of_blue_agents, number_of_red_agents, moving_threshold, number_of_neighbours, number_of_rows=100, number_of_columns=100):
        self.number_of_blue_agents = number_of_blue_agents
        self.number_of_red_agents = number_of_red_agents
        self.staying_threshold = moving_threshold
        self.number_of_neighbours = number_of_neighbours
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        #self.grid = np.array(self.number_of_blue_agents * [1] + self.number_of_red_agents * [2] + (self.number_of_rows * self.number_of_columns - self.number_of_red_agents - self.number_of_blue_agents) * [0])
        #np.random.shuffle(self.grid)
        #self.grid = self.grid.reshape(self.number_of_rows, self.number_of_columns)

        self.empty = np.arange(self.number_of_rows * self.number_of_columns)
        self.blue = random.sample(self.empty, self.number_of_blue_agents)
        self.red = random.sample(self.empty, self.number_of_red_agents)
        self.empty = [empty for empty in self.empty if empty not in self.blue + self.red]

        self.occupied_fields = dict()
        for i in self.blue + self.red:
            self.occupied_fields[i] = [i//self.number_of_columns, i%self.number_of_columns]
        self.neigh = NearestNeighbors(self.number_of_neighbours)

    def find_neighbours_of_agent(self, x, y):
        self.neigh.fit(list(self.occupied_fields.values()))
        return list(self.neigh.kneighbors([x, y]))

    def make_agents_indices_from_coordinates(self, list_of_coordinates):
        list_of_indices = []
        for coordinates in list_of_coordinates:
            list_of_indices.append(coordinates[0] * self.number_of_columns + coordinates[1])
        return list_of_indices

    def find_number_of_neighbours_of_the_same_type(self, agents_type, list_of_indices):
        if agents_type == 'blue':
            return sum(x in list_of_indices for x in self.blue)
        else:
            return sum(x in list_of_indices for x in self.red)

    def single_step(self, x, y):
        agents_type
        list_of_agent_neighbours = self.find_neighbours_of_agent(x, y)
        if self.find_number_of_neighbours_of_the_same_type(agents_type, self.make_agents_indices_from_coordinates(list_of_agent_neighbours)) / len(list_of_agent_neighbours) < self.staying_threshold:
            old_index = x * self.number_of_columns + y
            self.empty.append(old_index)
            new_index = random.sample(self.empty, 1)
            del self.occupied_fields[old_index]
            self.occupied_fields[new_index] = [new_index//self.number_of_columns, new_index%self.number_of_columns]
            if agents_type == 'blue':
                self.blue.remove(old_index)
                self.blue.append(new_index)
            else:
                self.red.remove(old_index)
                self.red.append(new_index)







if __name__ == '__main__':
    test = ShellingSegregation(50,15,20,20)
    test.print()