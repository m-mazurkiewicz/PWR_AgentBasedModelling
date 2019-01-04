from numpy.random import choice, random
from numpy import absolute, sum


class SituationGraph:
    def __init__(self, num_agents):
        self.spins = self.initialise_spins(num_agents)

    @staticmethod
    def initialise_spins(size):
        d = dict()
        for i in range(size):
            d[i] = 1
        return d

    def simulate(self, num_steps, independence, replace=False, flexibility=.5, no_of_neighbours=4):
        for i in range(num_steps):
            node = self.select_random_node()
            if random() <= (1 - independence):
                neighbors_spins = choice(list(self.spins.values()), no_of_neighbours, replace=replace)
                if absolute(sum(neighbors_spins)) == no_of_neighbours:
                    self.spins[node] = neighbors_spins[0]
            else:
                self.spins[node] *= (random() <= (1 - flexibility)) * 2 - 1

    def select_random_node(self):
        return choice(list(self.spins.keys()))


if __name__ == '__main__':
    graph = SituationGraph(100)
    graph.simulate(100, .5)
