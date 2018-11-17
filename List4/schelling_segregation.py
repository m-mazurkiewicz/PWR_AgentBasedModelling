import numpy as np
import random
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
from copy import deepcopy as copy


class ShellingSegregation:
    def __init__(self, number_of_blue_agents, number_of_red_agents, staying_threshold, number_of_neighbours, number_of_rows=100, number_of_columns=100):
        self.number_of_blue_agents = number_of_blue_agents
        self.number_of_red_agents = number_of_red_agents
        self.staying_threshold = staying_threshold
        self.number_of_neighbours = number_of_neighbours
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        #self.grid = np.array(self.number_of_blue_agents * [1] + self.number_of_red_agents * [2] + (self.number_of_rows * self.number_of_columns - self.number_of_red_agents - self.number_of_blue_agents) * [0])
        #np.random.shuffle(self.grid)
        #self.grid = self.grid.reshape(self.number_of_rows, self.number_of_columns)

        self.empty = np.arange(self.number_of_rows * self.number_of_columns)
        self.blue = random.sample(set(self.empty), self.number_of_blue_agents)
        self.empty = [empty for empty in self.empty if empty not in self.blue]
        self.red = random.sample(set(self.empty), self.number_of_red_agents)
        self.empty = [empty for empty in self.empty if empty not in self.red]

        self.occupied_fields = dict()
        for i in self.blue + self.red:
            self.occupied_fields[i] = [i // self.number_of_columns, i % self.number_of_columns]
        self.neigh = NearestNeighbors(self.number_of_neighbours)

    def find_neighbours_of_agent(self, x, y):
        list_of_occupied_fields = list(self.occupied_fields.values())
        self.neigh.fit(list_of_occupied_fields)
        neighbours_indices = self.neigh.kneighbors([[x, y]])
        neighbours = []
        for i in neighbours_indices[1].tolist()[0]:
            neighbours.append(list_of_occupied_fields[i])
        return neighbours

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
        old_index = x * self.number_of_columns + y
        if old_index in self.blue:
            agents_type = 'blue'
        else:
            agents_type = 'red'
        list_of_agent_neighbours = self.find_neighbours_of_agent(x, y)
        if self.find_number_of_neighbours_of_the_same_type(agents_type, self.make_agents_indices_from_coordinates(list_of_agent_neighbours)) / len(list_of_agent_neighbours) < self.staying_threshold:
            self.empty.append(old_index)
            new_index = random.sample(self.empty, 1)[0]
            del self.occupied_fields[old_index]
            self.occupied_fields[new_index] = [new_index // self.number_of_columns, new_index % self.number_of_columns]
            if agents_type == 'blue':
                self.blue.remove(old_index)
                self.blue.append(new_index)
            else:
                self.red.remove(old_index)
                self.red.append(new_index)
            self.agents_willing_to_move = True

    def whole_process(self):
        self.agents_willing_to_move = True
        self.history_ = []
        self.history_alt_ = []
        number_of_cycles = 0
        while self.agents_willing_to_move:
            blue_coordinates = []
            red_coordinates = []
            for index in self.blue:
                blue_coordinates.append(copy(self.occupied_fields[index]))
            for index in self.red:
                red_coordinates.append(copy(self.occupied_fields[index]))
            self.history_alt_.append((blue_coordinates,red_coordinates))
            self.history_.append((copy(self.blue), copy(self.red), copy(self.occupied_fields)))
            self.agents_willing_to_move = False
            for coordinates in list(self.occupied_fields.values()): #we can't loop over dict that is changing during iteration. This approach works, but I'm not completely sure if it fulfills lists assumptions
                self.single_step(coordinates[0], coordinates[1])
                #self.single_step(self.occupied_fields[key][0], self.occupied_fields[key][1])
            number_of_cycles += 1
        self.history_.append((copy(self.blue), copy(self.red), copy(self.occupied_fields)))
        print(number_of_cycles)

    def segregation_index(self):
        similar_neighbour_index = 0
        for coordinates in self.occupied_fields.values():
            agents_index = coordinates[0] * self.number_of_columns + coordinates[1]
            if agents_index in self.blue:
                agents_type = 'blue'
            else:
                agents_type = 'red'
            list_of_agent_neighbours = self.find_neighbours_of_agent(coordinates[0], coordinates[1])
            similar_neighbour_index += self.find_number_of_neighbours_of_the_same_type(agents_type, self.make_agents_indices_from_coordinates(list_of_agent_neighbours)) / len(list_of_agent_neighbours)
        return similar_neighbour_index / len(self.occupied_fields.values())

    def plot(self):
        length_of_simulation = len(self.history_)
        plt.figure(figsize=(6,4))
        plt.subplot(231)
        self.plot_history(self.history_[0])
        plt.title('1')
        # plt.subplot(232)
        # self.plot_history(self.history_[int(np.floor(length_of_simulation/5))])
        # plt.title(str(int(np.floor(length_of_simulation/5))))
        # plt.subplot(233)
        # self.plot_history(self.history_[2*int(np.floor(length_of_simulation/5))])
        # plt.title(str(2*int(np.floor(length_of_simulation/5))))
        # plt.subplot(234)
        # self.plot_history(self.history_[3*int(np.floor(length_of_simulation/5))])
        # plt.title(str(3*int(np.floor(length_of_simulation/5))))
        # plt.subplot(235)
        # self.plot_history(self.history_[4*int(np.floor(length_of_simulation/5))])
        # plt.title(str(4*int(np.floor(length_of_simulation/5))))
        plt.subplot(236)
        self.plot_history(self.history_[-1])
        plt.title(str(length_of_simulation))
        plt.show()
        plt.close()

    def plot_alt(self):
        length_of_simulation = len(self.history_)
        plt.figure(figsize=(6,4))
        plt.subplot(231)
        self.plot_history_alt(self.history_[0])
        plt.title('1')
        # plt.subplot(232)
        # self.plot_history(self.history_[int(np.floor(length_of_simulation/5))])
        # plt.title(str(int(np.floor(length_of_simulation/5))))
        # plt.subplot(233)
        # self.plot_history(self.history_[2*int(np.floor(length_of_simulation/5))])
        # plt.title(str(2*int(np.floor(length_of_simulation/5))))
        # plt.subplot(234)
        # self.plot_history(self.history_[3*int(np.floor(length_of_simulation/5))])
        # plt.title(str(3*int(np.floor(length_of_simulation/5))))
        # plt.subplot(235)
        # self.plot_history(self.history_[4*int(np.floor(length_of_simulation/5))])
        # plt.title(str(4*int(np.floor(length_of_simulation/5))))
        plt.subplot(236)
        self.plot_history_alt(self.history_[-1])
        plt.title(str(length_of_simulation))
        plt.show()
        plt.close()

    def plot_history(self,history):
        blue, red, coordinates_dictionary = history
        blue_coordinates = []
        red_coordinates = []
        for index in blue:
            blue_coordinates.append(coordinates_dictionary[index])
        for index in red:
            red_coordinates.append(coordinates_dictionary[index])
        plt.scatter(*zip(*blue_coordinates), c = 'b')
        plt.scatter(*zip(*red_coordinates), c = 'r')
        plt.axis('off')

    def plot_history_alt(self,history):
        blue_coordinates, red_coordinates = history
        plt.scatter(*zip(*blue_coordinates), c = 'b')
        plt.scatter(*zip(*red_coordinates), c = 'r')
        plt.axis('off')



if __name__ == '__main__':
    test = ShellingSegregation(300, 200, .8, 4, 100, 100)
    test.whole_process()
    test.plot_alt()
    # print(test.segregation_index())
    # print(len(test.blue))
    # print(len(test.red))