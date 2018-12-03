import numpy as np
import math
from List5.car import Car


class Road:
    def __init__(self, number_of_cells, density_of_cars, slowing_down_probability, max_speed = 5):
        self.number_of_cels = number_of_cells
        self.number_of_cars = math.ceil(self.number_of_cels*density_of_cars)
        self.p = slowing_down_probability
        self.max_speed = max_speed
        self.cars = [Car(location,self.max_speed) for location in np.random.choice(range(self.number_of_cels),self.number_of_cars,replace=False)]
        self.locations = [car.location for car in self.cars]

    def acceleration(self):
        for car in self.cars:
            car.speed = max(car.speed+1,self.max_speed)


if __name__ == '__main__':
    r = Road(50,0.5,0.5)
    r.acceleration()