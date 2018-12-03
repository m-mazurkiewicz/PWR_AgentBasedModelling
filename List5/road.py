import numpy as np
import math
from List5.car import Car
from copy import deepcopy as copy
from matplotlib import animation
import matplotlib.pyplot as plt


class Road:
    def __init__(self, number_of_cells, density_of_cars, slowing_down_probability, max_speed=5):
        self.number_of_cells = number_of_cells
        self.number_of_cars = math.ceil(self.number_of_cells * density_of_cars)
        self.p = slowing_down_probability
        self.max_speed = max_speed
        self.cells = [None for _ in range(self.number_of_cells)]
        self.cars = [Car(self.max_speed) for _ in range(self.number_of_cars)]
        for key, location in enumerate(np.random.choice(range(self.number_of_cells), self.number_of_cars, replace=False)):
            self.cells[location] = self.cars[key]

    def _acceleration(self):
        for car in self.cars:
            car.speed = min(car.speed + 1, self.max_speed)

    def _slowing_down(self):
        for location, car in enumerate(self.cells):
            if car is not None:
                for i in range(1, car.speed + 1):
                    if self.cells[(location + i) % self.number_of_cells] is not None:
                        car.speed = i - 1
                        break

    def _randomization(self):
        moving_cars = [car for car in self.cars if car.speed > 0]
        for car in [moving_cars[i] for i in np.where(np.random.rand(len(moving_cars)) <= self.p)[0]]:
            car.speed -= 1

    def _move_forward(self):
        new_cells = [None for _ in range(self.number_of_cells)]
        for location, car in enumerate(self.cells):
            if car is not None:
                new_cells[(location+car.speed) % self.number_of_cells] = car
        self.cells = new_cells

    def single_iteration(self):
        self._acceleration()
        self._slowing_down()
        self._randomization()
        self._move_forward()

    def _locations_of_cars(self, with_velocity=False):
        if with_velocity:
            return [(self.cells.index(car),car.speed) for car in self.cars]
        else:
            return [self.cells.index(car) for car in self.cars]

    def _velocities_of_cars(self):
        return [car.speed for car in self.cars]

    def average_velocity(self):
        return np.mean(self._velocities_of_cars())

    def simulate(self,number_of_iterations):
        for _ in range(number_of_iterations):
            self.single_iteration()
            # print(self.average_velocity())

    def visualize_system_evolution(self, file_path_and_name, number_of_iterations, duration=15):
        image_magick = animation.writers['imagemagick']
        fps = np.ceil(20 / float(duration))
        writer = image_magick(fps=fps)
        fig = plt.figure()
        ax = plt.gca()
        plt.axis('off')
        road_in_time = [[0] * self.number_of_cells] * number_of_iterations
        ax.imshow(road_in_time)
        with writer.saving(fig, file_path_and_name + ".gif", 100):
            writer.grab_frame()
            for i in range(number_of_iterations):
                self.single_iteration()
                road_in_time[i] = [1 if i in self._locations_of_cars() else 0 for i in range(self.number_of_cells)]
                print(self._locations_of_cars())
                ax.imshow(road_in_time)
                writer.grab_frame()


if __name__ == '__main__':
    r = Road(50, 0.3, 0.1)
    # print(r._locations_of_cars(True))
    # print(r.average_velocity())
    # # r._acceleration()
    # # print([(r.cells.index(car),car.speed) for car in r.cars])
    # # r._slowing_down()
    # # print([(r.cells.index(car),car.speed) for car in r.cars])
    # # r._randomization()
    # # # print([(r.cells.index(car),car.speed) for car in r.cars])
    # # r._move_forward()
    # r.single_iteration()
    # print(r._locations_of_cars(True))
    # print(r.average_velocity())
    #r.simulate(50)
    #print(r._locations_of_cars())
    r.visualize_system_evolution('test.gif', 50)