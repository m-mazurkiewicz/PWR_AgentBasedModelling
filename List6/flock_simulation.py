from List6.boid import Boid
from collections import defaultdict
from functools import partial
from itertools import count
from numpy import random
from sklearn.metrics import pairwise_distances as distance
import numpy as np
from matplotlib import pyplot as plt


class Flock:
    def __init__(self, num_boids, boid_size, max_velocity=50, x_range=1000, y_range=1000):
        self.range = (x_range, y_range)
        Boid.bounds = self.range
        Boid.max_velocity = max_velocity
        self.num_boids = num_boids
        self.init_random_boids(boid_size)

    def init_random_boids(self, boid_size):
        self.boids_dict_inverse_ = defaultdict(partial(next, count(0)))
        _ = [
            self.boids_dict_inverse_[Boid(position=(random.uniform(0, self.range[0]), random.uniform(0, self.range[1])),
                                          velocity=random.uniform(Boid.max_velocity), angle=random.rand() * 360 - 180,
                                          size=boid_size, color=(random.rand(), random.rand(), random.rand()))]
            for _ in range(self.num_boids)]
        self.boids_dict_ = {v: k for k, v in self.boids_dict_inverse_.items()}

    # def distance_matrix(self):
    #     boids_positions = np.array([self.boids_dict_[key].position for key in range(self.num_boids)])
    #     return distance(boids_positions, metric='euclidean', n_jobs=3)

    def plot_flock_simple(self):
        x_coordinates, y_coordinates = zip(*[self.boids_dict_[key].position for key in range(self.num_boids)])
        plt.plot(x_coordinates,y_coordinates, "*")
        plt.show()

    def single_iteration(self):
        pass



if __name__ == '__main__':
    f = Flock(num_boids=5, boid_size=3)
    for boid in range(f.num_boids):
        neighbors = f.boids_dict_[boid].nearby_boids(f.boids_dict_)
        print(f.boids_dict_[boid].average_neighbours_velocity(neighbors))
