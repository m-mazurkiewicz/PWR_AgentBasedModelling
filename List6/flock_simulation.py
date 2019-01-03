import os
from numpy import random, ceil
from boid import Boid
from obstacle import Obstacle
from matplotlib import pyplot as plt
from matplotlib import patches, animation
from tqdm import trange
import vector
import matplotlib as mpl


class Flock:
    def __init__(self, max_velocity=50, x_range=1000, y_range=1000):
        self.range = (x_range, y_range)
        Boid.bounds = self.range
        Boid.max_velocity = max_velocity
        self.num_boids = 0
        self.boids = []
        self.obstacles = []

    def init_random_boids(self, num_boids, boid_size=0):
        self.num_boids += num_boids
        positions_list = []
        while len(positions_list)<num_boids:
            position = (random.uniform(0, self.range[0]), random.uniform(0, self.range[1]))
            flag = True
            for obstacle in self.obstacles:
                if obstacle.x[0] < position[0] < obstacle.x[1] and obstacle.y[0] < position[1] < obstacle.y[1]:
                    flag=False
                    break
            if flag:
                positions_list.append(position)
        self.boids += [Boid(
            position=positions_list[key],
            velocity=(random.uniform(-Boid.max_velocity, Boid.max_velocity),
                      random.uniform(-Boid.max_velocity, Boid.max_velocity)),
            color=(random.random(), random.random(), random.random()), size = boid_size)
                    for key,_ in enumerate(range(self.num_boids))]

    def add_boid(self, position=(100.0, 100.0),
                 velocity=(0.0, 0.0),
                 size=0,
                 color=(1.0, 1.0, 1.0)):
        self.boids.append(Boid(position,velocity,size,color))
        self.num_boids += 1

    def add_obstacle(self, position=(100, 100), size=30.0, color=(1.0, 0.0, 0.0)):
        self.obstacles.append(Obstacle(position, size, color))

    def update(self,dt):
        for boid in self.boids:
            boid.update(dt, self.boids, self.obstacles)

    def simulate(self, delta_time, num_iterations):
        for _ in range(num_iterations):
            self.update(delta_time)

    def plot_flock_simple(self):
        x_coordinates, y_coordinates = zip(*[boid.position for boid in self.boids])
        plt.plot(x_coordinates,y_coordinates, "*")
        ax = plt.gca()
        for obj in self.obstacles:
            plt.plot(*zip(*[(obj.x[0],obj.y[0]),(obj.x[0],obj.y[1]),(obj.x[1],obj.y[0]),(obj.x[1],obj.y[1])]), 'ro')
            ax.add_patch(patches.Rectangle((obj.position[0] - obj.size, obj.position[1] - obj.size),
                                           2 * obj.size, 2 * obj.size, color='r'))
        plt.xlim((0,self.range[0]))
        plt.ylim((0,self.range[1]))
        plt.show()
        #return plt

    def simulate_and_plot(self, delta_time, number_of_iterations, file_name='', duration=15):
        image_magick = animation.writers['imagemagick']
        fps = ceil(number_of_iterations / float(duration))
        writer = image_magick(fps=fps)
        fig = plt.figure(figsize=(10,10))
        ax = plt.gca()
        plt.xlim((0, self.range[0]))
        plt.ylim((0, self.range[1]))
        plt.axis('off')
        for boid in self.boids:
            plt.scatter(boid.position[0], boid.position[1],
                        marker=(3, 0, int(vector.angle_between_plot(boid.velocity, (0, 1)))), color=boid.color)
        for obj in self.obstacles:
            # plt.plot(*zip(*[(obj.x[0],obj.y[0]),(obj.x[0],obj.y[1]),(obj.x[1],obj.y[0]),(obj.x[1],obj.y[1])]), 'ro')
            ax.add_patch(patches.Rectangle((obj.position[0] - obj.size, obj.position[1] - obj.size),
                                           2 * obj.size, 2 * obj.size, color='r'))
        ax.annotate('0', xy=(1, 0), xycoords='axes fraction', fontsize=16,
                    horizontalalignment='right', verticalalignment='bottom',color='grey')
        os.makedirs('figures', exist_ok=True)
        with writer.saving(fig, 'figures/' + str(self.range[0]) + '_' + str(self.range[1]) + '_' + str(len(self.boids)) +
                              '_' + file_name + ".gif", 100):
            writer.grab_frame()
            for i in trange(number_of_iterations):
                plt.cla()
                plt.xlim((0, self.range[0]))
                plt.ylim((0, self.range[1]))
                plt.axis('off')
                self.update(delta_time)
                for boid in self.boids:
                    plt.scatter(boid.position[0], boid.position[1], marker = (3, 0, int(vector.angle_between_plot(boid.velocity, (0,1)))), color=boid.color)
                for obj in self.obstacles:
                    # plt.plot(
                    #     *zip(*[(obj.x[0], obj.y[0]), (obj.x[0], obj.y[1]), (obj.x[1], obj.y[0]), (obj.x[1], obj.y[1])]),
                    #     'ro')
                    ax.add_patch(patches.Rectangle((obj.position[0] - obj.size, obj.position[1] - obj.size),
                                                   2 * obj.size, 2 * obj.size, color='r'))
                ax.annotate(str(i+1), xy=(1, 0), xycoords='axes fraction', fontsize=16,
                            horizontalalignment='right', verticalalignment='bottom',color='grey')
                writer.grab_frame()

if __name__ == '__main__':
    f = Flock(x_range=1000, y_range=1000, max_velocity=50)
    # f.add_obstacle(position=[500,500],size=100)
    # f.add_obstacle(position=[100, 100], size=20)
    # f.add_obstacle(position=[900, 900], size=40)
    for pos in range(100, 1100, 200):
        for pos1 in range(100, 1100, 200):
            f.add_obstacle(position=[pos,pos1], size=10)
    # f.add_obstacle(position=[500,500],size=200)
    # for pos in range(100, 1100, 200):
    #     f.add_obstacle(position=[pos,pos], size=10)
    f.init_random_boids(num_boids=100)
    # f.plot_flock_simple()
    # f.simulate(0.5,20)
    # f.plot_flock_simple()
    # f.simulate_and_plot(.5, 20)
    f.simulate_and_plot(.1, 1000, file_name='3', duration=80)

