import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

class Bass():
    def __init__(self,network:nx.Graph, p, q):
        self.network = network
        self.p = p
        self.q = q
        self.awareness = {node:False for node in self.network.nodes()}
        self.historical_awareness = [0]

    def full_awareness(self):
        return len(self.awareness.values()) == sum(self.awareness.values())

    def average_awareness(self):
        return np.mean(list(self.awareness.values()))

    def activation_probability(self,node):
        neighbours = [self.awareness[neighbour] for neighbour in self.network.neighbors(node)]
        return self.p + self.q * sum(neighbours)/len(neighbours) - (self.p * self.q * sum(neighbours)/len(neighbours))

    def simulate(self):
        while not self.full_awareness():
            for node in self.network.nodes():
                if not self.awareness[node]:
                    if self.activation_probability(node) >= np.random.rand():
                        self.awareness[node] = True
            self.historical_awareness.append(self.average_awareness())

def bass_function(t,p,q):
    return (1-np.exp(np.multiply(-(p+q),t)))/(1+q/p*np.exp(np.multiply(-(p+q),t)))

if __name__ == '__main__':
    network = nx.barabasi_albert_graph(100, 3)
    # network = nx.complete_graph(1000)
    p = 0.03
    q = 0.38
    model = Bass(network, p, q)
    model.simulate()
    plt.plot(model.historical_awareness, '*')
    plt.plot(bass_function(list(range(len(model.historical_awareness))), p, q), 'r*')
    plt.show()

