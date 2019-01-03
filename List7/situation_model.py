from networkx import Graph, complete_graph
from numpy.random import choice, random
from numpy import mean, absolute, sum


class SituationGraph:
    def __init__(self, graph: Graph):
        self.network = graph
        self.spins = self.initialise_spins(graph.number_of_nodes(),-1)

    @staticmethod
    def initialise_spins(size, spin):
        d = dict()
        for i in range(size):
            d[i] = spin
        return d

    def simulate(self,num_steps, replace=False, flexibility=.5, no_of_neighbours=4):
        for i in range(num_steps):
            node = self.select_random_node()
            if random() < flexibility:
                neighbors = choice(list(self.network.neighbors(node)), no_of_neighbours, replace=replace)
                if absolute(sum([self.spins[x] for x in neighbors])) > 0:
                    self.spins[node] = 1
                elif absolute(sum([self.spins[x] for x in neighbors])) < 0:
                    self.spins[node] = -1
            else:
                self.spins[node] *= (-1)

            # if absolute(sum([self.spins[x] for x in neighbors])) == no_of_neighbours:
            #     self.spins[node] = self.spins[neighbors[0]]
            # else:
            #     if random()<epsilon:
            #         self.spins[node] *= (-1)
            # self.magnetisation.append(mean(list(self.spins.values())))

    def select_random_node(self):
        random_node = choice(list(self.network.nodes()))
        return random_node


if __name__ == '__main__':
    graph = SituationGraph(complete_graph(100))
    graph.simulate(100)
