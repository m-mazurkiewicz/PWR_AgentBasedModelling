import numpy as np
import math
from List5.car import Car
from copy import deepcopy as copy


class Road:
    def __init__(self, number_of_cells, density_of_cars, slowing_down_probability, max_speed=5):
        self.number_of_cells = number_of_cells
        self.number_of_cars = math.ceil(self.number_of_cells * density_of_cars)
        self.p = slowing_down_probability
        self.max_speed = max_speed
        self.cells = [0 for _ in range(self.number_of_cells)]
        self.cars = [Car(self.max_speed) for _ in range(self.number_of_cars)]
        for key, location in enumerate(
                np.random.choice(range(self.number_of_cells), self.number_of_cars, replace=False)):
            self.cells[location] = self.cars[key]

    def _acceleration(self):
        for car in self.cars:
            car.speed = min(car.speed + 1, self.max_speed)

    def _slowing_down(self):
        for location, car in enumerate(self.cells):
            if isinstance(car, Car):
                for i in range(1, car.speed + 1):
                    if isinstance(self.cells[(location + i) % self.number_of_cells], Car):
                        car.speed = i - 1
                        break

    def _randomization(self):
        moving_cars = [car for car in self.cars if car.speed > 0]
        for car in [moving_cars[i] for i in np.where(np.random.rand(len(moving_cars)) <= self.p)[0]]:
            car.speed -= 1

    def _move_forward(self):
        new_cells = [0 for _ in range(self.number_of_cells)]
        for location, car in enumerate(self.cells):
            if isinstance(car, Car):
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


if __name__ == '__main__':
    r = Road(50, 0.2, 0.1)
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
    r.simulate(50)