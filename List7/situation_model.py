from numpy.random import choice, random
from numpy import absolute, sum, mean, linspace, arange, diff
from matplotlib import pyplot as plt
from scipy.stats import linregress
from copy import deepcopy
from tqdm import tqdm
import statsmodels.api as sm
import os


class SituationGraph:
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.spins = self.initialise_spins()
        self.historical_concentrations = []

    def initialise_spins(self):
        d = dict()
        for i in range(self.num_agents):
            d[i] = 1
        return d

    def simulate(self, num_steps, independence, replace=False, flexibility=.5, no_of_neighbours=4):
        for i in range(num_steps):
            node = self.select_random_node()
            if random() <= (1 - independence):
                neighbors = choice(list(set(range(self.num_agents)).difference([node])), no_of_neighbours, replace=replace)
                neighbors_spins = [self.spins[node] for node in neighbors]
                if sum(neighbors_spins[0]==neighbors_spins) == no_of_neighbours:
                    self.spins[node] = neighbors_spins[0]
            else:
                self.spins[node] = absolute(self.spins[node]-(random() <= (1 - flexibility)))

    def select_random_node(self):
        return choice(list(self.spins.keys()))

    def concentration(self):
        return mean(list(self.spins.values()))


def task(file_name, num_iterations=10000, num_MC=1000, flexibilieties_list=(0.2, 0.3, 0.4, 0.5), independence_delta=0.05):
    fig, ax = plt.subplots(figsize=[6.4*2, 4.8*2], dpi=300)
    for flexibility in tqdm(flexibilieties_list):
        independence_results = []
        for independence in arange(0, 1 + independence_delta, independence_delta):
            results = []
            for _ in range(num_MC):
                graph = SituationGraph(100)
                graph.simulate(num_steps=num_iterations, independence=independence, flexibility=flexibility)
                results.append(graph.concentration())
            independence_results.append(mean(results))
        line, = ax.plot(arange(0, 1 + independence_delta, independence_delta), independence_results, '.')
        line.set_label('f={}'.format(flexibility))
        ax.legend()
    ax.set_xlabel('Independence')
    ax.set_ylabel('Concentration')
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/{}.png'.format(file_name))


if __name__ == '__main__':
    task('task')
    # num_iterations = 10000
    # independence = 0.2
    # flexibility = 0.2
    # graph = SituationGraph(100)
    # # graph.simulate(5000, 0.1, replace=False, flexibility=0.5, no_of_neighbours=4)
    # graph.simulate(num_iterations, independence, flexibility=flexibility)
