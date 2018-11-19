# from List4.agent import Agent
import sys
from os.path import dirname
sys.path.append(dirname(__file__))
from agent import Agent
import matplotlib.pyplot as plt
from copy import deepcopy as copy
import numpy as np


class Grid:
    def __init__(self, num_of_type_0=250, num_of_type_1=250, num_neighbors_type_0=10, num_neighbors_type_1=10,
                 staying_threshold_0=.5, staying_threshold_1=.5, num_of_rows=100, num_of_columns=100):
        self.num_of_type_0 = num_of_type_0
        self.num_of_type_1 = num_of_type_1
        self.num_neighbors_type_0 = num_neighbors_type_0
        self.num_neighbors_type_1 = num_neighbors_type_1
        self.staying_threshold_0 = staying_threshold_0
        self.staying_threshold_1 = staying_threshold_1
        self.num_of_rows = num_of_rows
        self.num_of_columns = num_of_columns
        self.empty_spots = self.create_table_of_empty_spots(self.num_of_rows, self.num_of_columns)
        self.agents = [Agent(0, self.num_neighbors_type_0, self.staying_threshold_0, self.empty_spots) for i in range(self.num_of_type_0)]
        self.agents.extend(Agent(1, self.num_neighbors_type_1, self.staying_threshold_1, self.empty_spots) for i in range(self.num_of_type_1))
        self.history = []

    def create_table_of_empty_spots(self, num_of_rows, num_of_columns):
        empty_spots = []
        for i in range(num_of_rows):
            for j in range(num_of_columns):
                empty_spots.append((i, j))
        return empty_spots

    def run_algorithm(self, max_number_of_iterations=100, plot_n_print = False):
        count = 1
        # ==  Loop until none wishes to move == #
        if plot_n_print:
            self.plot_distribution(self.agents, count)
        while True and count < max_number_of_iterations:
            self.history.append(copy(self.agents))
            if plot_n_print:
                print('Entering loop ', count)
            # plot_distribution(grid.agents, count)
            count += 1
            no_one_moved = True
            for agent in self.agents:
                old_location = agent.location
                agent.update(self.agents)
                if agent.location != old_location:
                    no_one_moved = False
            if no_one_moved:
                break
        self.history.append(copy(self.agents))
        if plot_n_print:
            self.plot_distribution(self.agents, count)
            print('Converged, terminating.')

    def calculate_similar_neighbour_index(self):
        similar_neighbour_index = 0
        for agent in self.agents:
            similar_neighbour_index += agent.fraction_of_neighbours_of_the_same_type(self.agents)
        return similar_neighbour_index / len(self.agents)

    def plot(self, file_name = None):
        length_of_simulation = len(self.history)
        plt.figure(figsize=(12,8), dpi = 300)
        plt.subplot(231)
        self.plot_distribution(self.history[0], 1)
        plt.subplot(232)
        self.plot_distribution(self.history[int(np.floor(length_of_simulation/5))], int(np.floor(length_of_simulation/5))+1)
        plt.subplot(233)
        self.plot_distribution(self.history[2*int(np.floor(length_of_simulation/5))], 2*int(np.floor(length_of_simulation/5))+1)
        plt.subplot(234)
        self.plot_distribution(self.history[3*int(np.floor(length_of_simulation/5))], 3*int(np.floor(length_of_simulation/5))+1)
        plt.subplot(235)
        self.plot_distribution(self.history[4*int(np.floor(length_of_simulation/5))], 4*int(np.floor(length_of_simulation/5))+1)
        plt.subplot(236)
        self.plot_distribution(self.history[length_of_simulation-1], length_of_simulation)
        if file_name:
            plt.savefig(file_name+'.png')
        else:
            plt.show()
        plt.close()

    def plot_distribution(self, agents, cycle_num):
        "Plot the distribution of agents after cycle_num rounds of the loop."
        # == Obtain locations of each type == #
        agents_0 = [agent.location for agent in agents if agent.type == 0]
        agents_1 = [agent.location for agent in agents if agent.type == 1]
        # fig, ax = plt.subplots(figsize=(8, 8))
        plot_args = {'markersize': 6, 'alpha': 0.6}
        # plt.facecolor('azure')
        plt.plot(*zip(*agents_0), 'o', markerfacecolor='orange',  **plot_args)
        plt.plot(*zip(*agents_1), 'o', markerfacecolor='green', **plot_args)
        plt.xlim(-0.5, self.num_of_columns+0.5)
        plt.ylim(-0.5, self.num_of_rows+0.5)
        plt.title(f'Cycle {cycle_num-1}')
        plt.axis('off')
        # plt.show()


if __name__ == '__main__':
    num_of_type_0 = 250
    num_of_type_1 = 250
    num_neighbors_0 = 10
    num_neighbors_1 = 15
    staying_threshold_0 = .5
    staying_threshold_1 = 2 / 3
    max_number_of_iterations = 100

    grid = Grid(num_of_type_0, num_of_type_1, num_neighbors_0, num_neighbors_1, staying_threshold_0, staying_threshold_1)
    grid.run_algorithm(max_number_of_iterations, plot_n_print=False)
    print(grid.calculate_similar_neighbour_index())
    grid.plot()