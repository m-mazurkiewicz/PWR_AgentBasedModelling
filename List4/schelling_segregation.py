# from List4.agent import Agent
import sys
import os
from os.path import dirname
sys.path.append(dirname(__file__))
from agent import Agent, AgentPeriodic
import matplotlib.pyplot as plt
from copy import deepcopy as copy
import numpy as np
from tqdm import tqdm, trange


class Grid:

    agent = Agent

    def __init__(self, num_of_type_0=250, num_of_type_1=250, num_neighbors_type_0=8, num_neighbors_type_1=8,
                 staying_threshold_0=.5, staying_threshold_1=.5, num_of_rows=100, num_of_columns=100):
        self.iteration_counter = 0
        self.num_of_type_0 = num_of_type_0
        self.num_of_type_1 = num_of_type_1
        self.num_neighbors_type_0 = num_neighbors_type_0
        self.num_neighbors_type_1 = num_neighbors_type_1
        self.staying_threshold_0 = staying_threshold_0
        self.staying_threshold_1 = staying_threshold_1
        self.num_of_rows = num_of_rows
        self.num_of_columns = num_of_columns
        self.empty_spots = self.create_table_of_empty_spots()
        self.agent.grid_dimensions = (self.num_of_columns, self.num_of_rows)
        # self.agent.num_of_rows = self.num_of_rows
        # self.agent.num_of_columns = self.num_of_columns
        self.agents = [self.agent(0, self.num_neighbors_type_0, self.staying_threshold_0, self.empty_spots) for i in range(self.num_of_type_0)]
        self.agents.extend(self.agent(1, self.num_neighbors_type_1, self.staying_threshold_1, self.empty_spots) for i in range(self.num_of_type_1))
        self.history = []

    def create_table_of_empty_spots(self):
        empty_spots = []
        for i in range(self.num_of_rows):
            for j in range(self.num_of_columns):
                empty_spots.append((i, j))
        return empty_spots

    def run_algorithm(self, max_number_of_iterations=100, plot_n_print = False):
        # ==  Loop until none wishes to move == #
        if plot_n_print:
            self.plot_distribution(self.agents, self.iteration_counter)
        while True and self.iteration_counter < max_number_of_iterations:
            self.history.append(copy(self.agents))
            if plot_n_print:
                print('Entering loop ', self.iteration_counter)
            # plot_distribution(grid.agents, count)
            self.iteration_counter += 1
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
            self.plot_distribution(self.agents, self.iteration_counter)
            print('Converged, terminating.')

    def calculate_similar_neighbour_index(self, agents_list = None):
        similar_neighbour_index = 0
        if agents_list:
            for agent in agents_list:
                similar_neighbour_index += agent.fraction_of_neighbours_of_the_same_type(agents_list)
            return similar_neighbour_index / len(agents_list)
        else:
            for agent in self.agents:
                similar_neighbour_index += agent.fraction_of_neighbours_of_the_same_type(self.agents)
            return similar_neighbour_index / len(self.agents)

    def plot(self, file_name = None):
        length_of_simulation = self.iteration_counter#len(self.history)
        fig = plt.figure(figsize=(12,8), dpi = 300)
        fig.suptitle(
            f'Blue - ({self.num_of_type_0}; {self.num_neighbors_type_0}; {round(self.staying_threshold_0,2)}) Red - ({self.num_of_type_1}; {self.num_neighbors_type_1}; {round(self.staying_threshold_1,2)}) {self.num_of_rows}x{self.num_of_columns} grid', y=.03, fontsize=14)
        plt.subplot(231)
        self.plot_distribution(self.history[0], 0)
        plt.subplot(232)
        self.plot_distribution(self.history[int(np.floor(length_of_simulation/5))], int(np.floor(length_of_simulation/5)))
        plt.subplot(233)
        self.plot_distribution(self.history[2*int(np.floor(length_of_simulation/5))], 2*int(np.floor(length_of_simulation/5)))
        plt.subplot(234)
        self.plot_distribution(self.history[3*int(np.floor(length_of_simulation/5))], 3*int(np.floor(length_of_simulation/5)))
        plt.subplot(235)
        self.plot_distribution(self.history[4*int(np.floor(length_of_simulation/5))], 4*int(np.floor(length_of_simulation/5)))
        plt.subplot(236)
        self.plot_distribution(self.history[length_of_simulation], length_of_simulation-1)
        if file_name:
            plt.savefig(file_name+'.png')
        else:
            plt.show()
        plt.close(fig)

    def save_agents_to_file(self, file_name):
        with open(file_name+'.csv', 'w', encoding='UTF-8') as f:
            f.write('x,y,type\n')
            for agent in self.agents:
                f.write(str(agent.location[0])+','+str(agent.location[1])+','+str(agent.type)+'\n')

    def plot_distribution(self, agents, cycle_num):
        "Plot the distribution of agents after cycle_num rounds of the loop."
        # == Obtain locations of each type == #
        agents_0 = [agent.location for agent in agents if agent.type == 0]
        agents_1 = [agent.location for agent in agents if agent.type == 1]
        plot_args = {'markersize': 6, 'alpha': 0.6}
        # plt.facecolor('azure')
        plt.plot(*zip(*agents_0), 'o', markerfacecolor='blue',  **plot_args)
        plt.plot(*zip(*agents_1), 'o', markerfacecolor='red', **plot_args)
        plt.xlim(-0.5, self.num_of_columns+0.5)
        plt.ylim(-0.5, self.num_of_rows+0.5)
        plt.title('Cycle {0:.0f}, {1:.4f}'.format(cycle_num,self.calculate_similar_neighbour_index(agents)))
        plt.axis('off')


class GridPeriodic(Grid):
    agent = AgentPeriodic

    def plot(self, file_name = None):
        length_of_simulation = len(self.history)
        fig = plt.figure(figsize=(12,8), dpi = 300)
        fig.suptitle(
            f'Blue - ({self.num_of_type_0}; {self.num_neighbors_type_0}; {round(self.staying_threshold_0,2)}) Red - ({self.num_of_type_1}; {self.num_neighbors_type_1}; {round(self.staying_threshold_1,2)}) {self.num_of_rows}x{self.num_of_columns} periodic grid', y=.03, fontsize=14)
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
        plt.close(fig)


def to_do_3(file_name, mc_simulations = 10, left_limit = 250, right_limit = 4000):
    results = []
    population_range = np.arange(left_limit, right_limit+250, 250)
    for population in tqdm(population_range):
        single_mc_results = []
        for _ in range(mc_simulations):
            g = GridPeriodic(num_of_type_0=population, num_of_type_1=population)
            g.run_algorithm()
            single_mc_results.append(g.iteration_counter)
        results.append(single_mc_results)
    # print(np.apply_along_axis(np.mean, 1, np.array(results)))
    results_array = np.array(results)
    plt.errorbar(population_range, np.apply_along_axis(np.mean, 1, results_array), yerr=np.apply_along_axis(np.std, 1, results_array))
    plt.xlabel('Size of populations')
    plt.ylabel('Number of iterations')
    plt.title('Average number of iterations for {0} Monte Carlo simulations'.format(mc_simulations))
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/{0}_{1}.png'.format(file_name, mc_simulations), dpi=300)


def to_do_4(file_name, mc_simulations = 10, num_steps = 50):
    results = []
    j_range = np.linspace(0.1, 0.9, num_steps, endpoint=True)
    for j in tqdm(j_range):
        single_mc_results = []
        for _ in range(mc_simulations):
            g = GridPeriodic(staying_threshold_0=j, staying_threshold_1=j)
            g.run_algorithm(max_number_of_iterations=1000)
            single_mc_results.append(g.calculate_similar_neighbour_index())
        results.append(single_mc_results)
    # print(np.apply_along_axis(np.mean, 1, np.array(results)))
    results_array = np.array(results)
    plt.errorbar(j_range, np.apply_along_axis(np.mean, 1, results_array), yerr=np.apply_along_axis(np.std, 1, results_array))
    plt.xlabel('Value of j_t')
    plt.ylabel('Segregation index')
    plt.title('Average segregation index for {0} Monte Carlo simulations'.format(mc_simulations))
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/{0}_{1}.png'.format(file_name, mc_simulations), dpi=300)
    # plt.show()


def to_do_5(file_name, mc_simulations = 10):
    results = []
    m_range = (np.hstack((0,np.cumsum(np.arange(2,6))))+np.ones(5, dtype=int))*8
    for m in tqdm(m_range):
        single_mc_results = []
        for _ in range(mc_simulations):
            g = GridPeriodic(num_neighbors_type_0=m, num_neighbors_type_1=m)
            g.run_algorithm()
            single_mc_results.append(g.calculate_similar_neighbour_index())
        results.append(single_mc_results)
    results_array = np.array(results)
    plt.errorbar(m_range, np.apply_along_axis(np.mean, 1, results_array), yerr=np.apply_along_axis(np.std, 1, results_array))
    plt.xlabel('Value of m_t')
    plt.ylabel('Segregation index')
    plt.title('Average segregation index for {0} Monte Carlo simulations'.format(mc_simulations))
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/{0}_{1}.png'.format(file_name, mc_simulations), dpi=300)


if __name__ == '__main__':
    # num_of_type_0 = 250
    # num_of_type_1 = 250
    # num_neighbors_0 = 10
    # num_neighbors_1 = 15
    # staying_threshold_0 = .5
    # staying_threshold_1 = 2 / 3
    # max_number_of_iterations = 100
    # number_of_rows = 100
    # number_of_columns = 100
    #
    # grid = Grid(num_of_type_0, num_of_type_1, num_neighbors_0, num_neighbors_1, staying_threshold_0, staying_threshold_1, number_of_rows, number_of_columns)
    # # grid = GridPeriodic(num_of_type_0, num_of_type_1, num_neighbors_0, num_neighbors_1, staying_threshold_0, staying_threshold_1, number_of_rows, number_of_columns)
    # grid.run_algorithm(max_number_of_iterations, plot_n_print=False)
    # print(grid.calculate_similar_neighbour_index())
    # grid.plot()

    to_do_3(file_name='average_number_iterations_250_grid', mc_simulations=2)
    # to_do_4(file_name='average_segregation_index_j_1000limit')
    # to_do_5(file_name='average_segregation_index_m', mc_simulations=100)