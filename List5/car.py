import numpy as np


class Car:
    def __init__(self,location,max_speed):
        self.location = location
        self.max_speed = max_speed
        self.speed = np.random.randint(0,self.max_speed+1)