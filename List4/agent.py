from random import seed, randint
from math import sqrt

# seed(10)  # for reproducible random numbers


class Agent:

    def __init__(self, type, num_neighbors, staying_threshold, empty_spots):
        self.type = type
        self.num_neighbors = num_neighbors
        self.staying_threshold = staying_threshold
        self.empty_spots = empty_spots
        self.draw_location()

    def draw_location(self):
        self.location = randint(0, 100), randint(0, 100)
        while self.location not in self.empty_spots:
            self.location = randint(0, 100), randint(0, 100)
        self.empty_spots.remove(self.location)

    def get_distance(self, other):
        "Computes euclidean distance between self and other agent."
        a = (self.location[0] - other.location[0])**2
        b = (self.location[1] - other.location[1])**2
        return sqrt(a + b)

    def fraction_of_neighbours_of_the_same_type(self, agents):
        "True if sufficient number of nearest neighbors are of the same type."
        distances = []
        # distances is a list of pairs (d, agent), where d is distance from
        # agent to self
        for agent in agents:
            if self != agent:
                distance = self.get_distance(agent)
                distances.append((distance, agent))
        # == Sort from smallest to largest, according to distance == #
        distances = sorted(distances, key=lambda x: x[0])
        #distances.sort()
        # == Extract the neighboring agents == #
        neighbors = [agent for d, agent in distances[:self.num_neighbors]]
        # == Count how many neighbors have the same type as self == #
        num_same_type = sum(self.type == agent.type for agent in neighbors)
        return num_same_type / self.num_neighbors

    def update(self, agents):
        "If not happy, then randomly choose new locations until happy."
        #while not self.happy(agents):
        if self.fraction_of_neighbours_of_the_same_type(agents) < self.staying_threshold:
            self.empty_spots.append(self.location)
            self.draw_location()