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

    def acceleration(self):
        for car in self.cars:
            car.speed = min(car.speed + 1, self.max_speed)

    def slowing_down(self):
        for location, car in enumerate(self.cells):
            if isinstance(car, Car):
                for i in range(1, car.speed + 1):
                    if isinstance(self.cells[(location + i) % self.number_of_cells], Car):
                        car.speed = i - 1
                        break


if __name__ == '__main__':
    r = Road(5000, 0.4, 0.5)
    # print([car.speed for car in r.cells if car!=0])
    r.acceleration()
    r.slowing_down()
