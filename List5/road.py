import numpy as np
from List5.car import Car


class Road:
    def __init__(self, number_of_cells, density_of_cars, slowing_down_probability, max_speed = 5):
        self.number_of_cels = number_of_cells
        self.number_of_cars = np.ceil(self.number_of_cels*density_of_cars)
        self.p = slowing_down_probability
        self.max_speed = max_speed
        self.cars = [Car(location,self.max_speed) for location in np.random.choice(range(self.number_of_cels),self.number_of_cars,replace=False)]