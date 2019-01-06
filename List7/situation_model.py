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

    # def simulate(self, num_steps, independence, replace=False, flexibility=.5, no_of_neighbours=4):
    #     i = 0
    #     fig, ax = plt.subplots()
    #     fig1, ax1 = plt.subplots()
    #     fig2, ax2 = plt.subplots()
    #     fig4, ax4 = plt.subplots()
    #     zeros_counter = 0
    #     slopes = []
    #     while i < num_steps:# and zeros_counter != 1:
    #         node = self.select_random_node()
    #         if random() <= (1 - independence):
    #             neighbors_spins = choice(list(self.spins.values()), no_of_neighbours, replace=replace)
    #             if absolute(sum(neighbors_spins)) == no_of_neighbours:
    #                 self.spins[node] = neighbors_spins[0]
    #         else:
    #             self.spins[node] = absolute(self.spins[node] - (random() <= (1 - flexibility)))
    #         self.historical_concentrations.append(mean(list(self.spins.values())))
    #         if i>1000:
    #             ax4.plot(i,mean(self.historical_concentrations),'*')
    #         i += 1
    #         if i > 1000 and i % 100 == 0:
    #             X = sm.add_constant(range(i))
    #             mod_wls = sm.WLS(self.historical_concentrations, X, weights=range(1, i + 1))
    #             res_wls = mod_wls.fit()
    #             slopes.append(res_wls.params[1])
    #             ax1.plot(i, res_wls.params[1], 'o')
    #             ax2.plot(i, res_wls.params[0], 'o')
    #             if absolute(res_wls.params[1]) <= 1 ** (-6):
    #                 zeros_counter += 1
    #         ax.plot(i, mean(list(self.spins.values())), 'o')
    #     fig3, ax3 = plt.subplots()
    #     ax3.plot(diff(slopes),'o')
    #     plt.show()
    #     print(zeros_counter)

    # def simulate(self, num_steps, independence, replace=False, flexibility=.5, no_of_neighbours=4):
    #     plt.figure()
    #     for i in range(num_steps):
    #         node = self.select_random_node()
    #         if random() <= (1 - independence):
    #             neighbors_spins = choice(list(self.spins.values()), no_of_neighbours, replace=replace)
    #             if absolute(sum(neighbors_spins)) == no_of_neighbours:
    #                 self.spins[node] = neighbors_spins[0]
    #         else:
    #             self.spins[node] = absolute(self.spins[node]-(random() <= (1 - flexibility)))
    #         self.historical_concentrations.append(mean(list(self.spins.values())))
    #         plt.plot(i,self.concentration(),'o')
    #         plt.plot(i,self.historical_concentrations[-1],'*')
    #     plt.show()

    # def simulate(self, epsilon, independence, replace=False, flexibility=.5, no_of_neighbours=4):
    #     plt.figure()
    #     slope = -1000
    #     previous_slope = -2000
    #     i = 0
    #     while absolute(slope-previous_slope) >= epsilon:
    #         node = self.select_random_node()
    #         if random() <= (1 - independence):
    #             neighbors_spins = choice(list(self.spins.values()), no_of_neighbours, replace=replace)
    #             if absolute(sum(neighbors_spins)) == no_of_neighbours:
    #                 self.spins[node] = neighbors_spins[0]
    #         else:
    #             self.spins[node] = absolute(self.spins[node]-(random() <= (1 - flexibility)))
    #         self.historical_concentrations.append(mean(list(self.spins.values())))
    #         if i>2:
    #             previous_slope = deepcopy(slope)
    #             slope, intercept, r_value, p_value, std_err = linregress(range(i+1), self.historical_concentrations)
    #             plt.plot(i,slope,'o')
    #             # plt.plot(i,self.historical_concentrations[i],'*')
    #         i+=1
    #     plt.show()

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
                graph.simulate(num_iterations, independence, flexibility)
                results.append(graph.concentration())
            independence_results.append(mean(results))
        line, = ax.plot(arange(0, 1 + independence_delta, independence_delta), independence_results, '.')
        line.set_label('f={}'.format(flexibility))
        ax.legend()
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/{}.png'.format(file_name))


if __name__ == '__main__':
    task('task')
    # graph = SituationGraph(100)
    # graph.simulate(5000, 0.1, replace=False, flexibility=0.5, no_of_neighbours=4)
