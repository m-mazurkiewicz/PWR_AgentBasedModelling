import os
import numpy as np
import math
from List5.car import Car
from copy import deepcopy #as copy
import copy
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

    def visualize_system_evolution(self, file_name, number_of_iterations, duration=15):
        image_magick = animation.writers['imagemagick']
        fps = np.ceil(20 / float(duration))
        writer = image_magick(fps=fps)
        fig = plt.figure()
        ax = plt.gca()
        plt.axis('off')
        road_in_time = [[0] * self.number_of_cells] * number_of_iterations
        ax.imshow(road_in_time)
        os.makedirs('figures', exist_ok=True)
        with writer.saving(fig, 'figures/' + file_name + ".gif", 100):
            writer.grab_frame()
            for i in range(number_of_iterations):
                self.single_iteration()
                road_in_time[i] = [1 if i in self._locations_of_cars() else 0 for i in range(self.number_of_cells)]
                ax.imshow(road_in_time)
                writer.grab_frame()


class RoadWith2Lines(Road):
    def __init__(self, number_of_cells_in_single_line, density_of_cars_right_line, slowing_down_probability, max_speed=5):
        self.number_of_cells_in_single_line = number_of_cells_in_single_line
        self.number_of_cars = math.ceil(self.number_of_cells_in_single_line * density_of_cars_right_line * 1.5)
        self.p = slowing_down_probability
        self.max_speed = max_speed
        self.cells_right_line = [None] * self.number_of_cells_in_single_line
        self.cells_left_line = [None] * self.number_of_cells_in_single_line
        self.cars = [Car(self.max_speed) for _ in range(self.number_of_cars)]
        for key, location in enumerate(np.random.choice(range(self.number_of_cells_in_single_line), int(self.number_of_cars * 2/3), replace=False)):
            self.cells_right_line[location] = self.cars[key]
        for key, location in enumerate(np.random.choice(range(self.number_of_cells_in_single_line), int(self.number_of_cars * 1/3), replace=False)):
            self.cells_left_line[location] = self.cars[key + int(self.number_of_cars * 2/3)]

    def _slowing_down(self):
        self.new_left_line = copy.copy(self.cells_left_line)
        self.new_right_line = copy.copy(self.cells_right_line)
        for location, car in enumerate(self.cells_left_line):
            if car is not None:
                if not self.try_to_change_line(location, car, 'left'):
                    for i in range(1, car.speed + 1):
                        if self.cells_left_line[(location + i) % self.number_of_cells_in_single_line] is not None:
                            car.speed = i - 1
                            break
        for location, car in enumerate(self.cells_right_line):
            if car is not None:
                    for i in range(1, car.speed + 1):
                        if self.cells_right_line[(location + i) % self.number_of_cells_in_single_line] is not None:
                            if not self.try_to_change_line(location, car, 'right'):
                                car.speed = i - 1
                                break

    def try_to_change_line(self, location, car, line):
        if line == 'left':
            if self.new_right_line[location - 6 + car.speed : location].count(None) == 6 - car.speed:
                if self.new_right_line[location : location + car.speed + 1].count(None) == car.speed + 1:
                    self.new_right_line[location] = car
                    self.new_left_line[location] = None
                    return True
        else:
            if self.new_left_line[location - 6 + car.speed : location].count(None) == 6 - car.speed:
                if self.new_left_line[location : location + car.speed + 1].count(None) == car.speed + 1:
                    self.new_left_line[location] = car
                    self.new_right_line[location] = None
                    return True
        return False

    def _move_forward(self):
        new_cells = [None for _ in range(self.number_of_cells_in_single_line)]
        for location, car in enumerate(self.new_left_line):
            if car is not None:
                new_cells[(location + car.speed) % self.number_of_cells_in_single_line] = car
        self.cells_left_line = new_cells
        new_cells = [None for _ in range(self.number_of_cells_in_single_line)]
        for location, car in enumerate(self.new_right_line):
            if car is not None:
                new_cells[(location + car.speed) % self.number_of_cells_in_single_line] = car
        self.cells_right_line = new_cells

    def _locations_of_cars(self, line=None):
        if line is 'right':
            return [self.cells_right_line.index(car) for car in self.cars if car in self.cells_right_line]
        elif line is 'left':
            return [self.cells_left_line.index(car) for car in self.cars if car in self.cells_left_line]
        else:
            return [self.cells.index(car) for car in self.cars]

    def visualize_system_evolution(self, file_name, number_of_iterations, duration=15):
        image_magick = animation.writers['imagemagick']
        fps = np.ceil(20 / float(duration))
        writer1 = image_magick(fps=fps)
        writer2 = image_magick(fps=fps)
        fig = plt.figure()
        ax = plt.gca()
        plt.axis('off')
        fig2 = plt.figure()
        ax2 = plt.gca()
        plt.axis('off')
        left_line_in_time = [[0] * self.number_of_cells_in_single_line] * number_of_iterations
        right_line_in_time = [[0] * self.number_of_cells_in_single_line] * number_of_iterations
        ax.imshow(left_line_in_time)
        ax2.imshow(right_line_in_time)
        os.makedirs('figures', exist_ok=True)
        with writer1.saving(fig, 'figures/' + file_name + "_left.gif", 100):
            with writer2.saving(fig2, 'figures/' + file_name + "_right.gif", 100):
                writer1.grab_frame()
                writer2.grab_frame()
                for i in range(number_of_iterations):
                    self.single_iteration()
                    left_line_in_time[i] = [1 if i in self._locations_of_cars('left') else 0 for i in range(self.number_of_cells_in_single_line)]
                    right_line_in_time[i] = [1 if i in self._locations_of_cars('right') else 0 for i in
                                            range(self.number_of_cells_in_single_line)]
                    ax.imshow(left_line_in_time)
                    writer1.grab_frame()
                    ax2.imshow(right_line_in_time)
                    writer2.grab_frame()

    def _velocities_of_cars(self, line=None):
        if line is 'right':
            return [car.speed for car in self.cars if car in self.cells_right_line]
        elif line is 'left':
            return [car.speed for car in self.cars if car in self.cells_left_line]
        else:
            return [car.speed for car in self.cars]

    def average_velocity(self, line=None):
        return np.mean(self._velocities_of_cars(line))


def plot_average_velocities(file_name, number_of_cells, densities, slowing_down_probability, max_speed=5,
                            no_of_simulations_per_single_road=50, no_of_MC_steps=100, two_lines=False):
    if two_lines:
        average_speed_per_simulation =[]
        average_speed_per_simulation_left =[]
        average_speed_per_simulation_right =[]
        for density_of_cars in densities:
            average_speeds = []
            average_speeds_left = []
            average_speeds_right = []
            for _ in range(no_of_MC_steps):
                road = RoadWith2Lines(number_of_cells, density_of_cars, slowing_down_probability, max_speed)
                road.simulate(no_of_simulations_per_single_road)
                average_speeds.append(road.average_velocity())
                average_speeds_left.append(road.average_velocity('left'))
                average_speeds_right.append(road.average_velocity('right'))
            average_speed_per_simulation.append(average_speeds)
            average_speed_per_simulation_left.append(average_speeds_left)
            average_speed_per_simulation_right.append(average_speeds_right)
        os.makedirs('figures', exist_ok=True)
        results_array = np.array(average_speed_per_simulation)
        results_array_left = np.array(average_speed_per_simulation_left)
        results_array_right = np.array(average_speed_per_simulation_right)
        average = plt.errorbar(densities, np.apply_along_axis(np.mean, 1, results_array), yerr=np.apply_along_axis(np.std, 1, results_array))
        right = plt.errorbar(densities, np.apply_along_axis(np.mean, 1, results_array_right), yerr=np.apply_along_axis(np.std, 1, results_array_right))
        left = plt.errorbar(densities, np.apply_along_axis(np.mean, 1, results_array_left), yerr=np.apply_along_axis(np.std, 1, results_array_left))
        lgnd = plt.legend((average, left, right), ('Average velocity','Average velocity on right line','Average velocity on left line'))
        plt.xlabel('Cars density')
        plt.ylabel('Average speed')
        plt.title('Average speed for simulation with {0} cells \n running for {1} iterations each ({2} MC simulations \n '
                  'p={3})'.format(number_of_cells,no_of_simulations_per_single_road,no_of_MC_steps,
                                  slowing_down_probability))
        plt.savefig('figures/{0}_{1}_{2}_{3}_p={4}.png'.format(file_name,number_of_cells,no_of_simulations_per_single_road,no_of_MC_steps,slowing_down_probability))
        plt.close()
    else:
        average_speed_per_simulation =[]
        for density_of_cars in densities:
            average_speeds = []
            for _ in range(no_of_MC_steps):
                road = Road(number_of_cells, density_of_cars, slowing_down_probability, max_speed)
                road.simulate(no_of_simulations_per_single_road)
                average_speeds.append(road.average_velocity())
            average_speed_per_simulation.append(average_speeds)
        os.makedirs('figures', exist_ok=True)
        results_array = np.array(average_speed_per_simulation)
        plt.errorbar(densities, np.apply_along_axis(np.mean, 1, results_array), yerr=np.apply_along_axis(np.std, 1, results_array))
        plt.xlabel('Cars density')
        plt.ylabel('Average speed')
        plt.title('Average speed for simulation with {0} cells \n running for {1} iterations each ({2} MC simulations \n '
                  'p={3})'.format(number_of_cells,no_of_simulations_per_single_road,no_of_MC_steps,
                                  slowing_down_probability))
        plt.savefig('figures/{0}_{1}_{2}_{3}_p={4}.png'.format(file_name,number_of_cells,no_of_simulations_per_single_road,no_of_MC_steps,slowing_down_probability))
        plt.close()


if __name__ == '__main__':
    r = RoadWith2Lines(60, 0.3, 0.2)
    r.visualize_system_evolution('test_visualization_2_lines', 40)
    # print([r.cells_left_line[i].speed if r.cells_left_line[i] is not None else None for i in range(int(r.number_of_cells_in_single_line))])
    # print([r.cells_right_line[i].speed if r.cells_right_line[i] is not None else None for i in range(int(r.number_of_cells_in_single_line))])
    # r._acceleration()
    # r._slowing_down()
    # print([r.new_left_line[i].speed if r.new_left_line[i] is not None else None for i in
    #        range(int(r.number_of_cells_in_single_line))])
    # print([r.new_right_line[i].speed if r.new_right_line[i] is not None else None for i in
    #        range(int(r.number_of_cells_in_single_line))])
    # print(r.average_velocity())
    # print(r.average_velocity('right'))
    # print(r.average_velocity('left'))
    # r._slowing_down()
    # r._randomization()
    # r._move_forward()
    # print([r.cells_left_line[i].speed if r.cells_left_line[i] is not None else None for i in
    #        range(int(r.number_of_cells_in_single_line))])
    # print([r.cells_right_line[i].speed if r.cells_right_line[i] is not None else None for i in range(int(r.number_of_cells_in_single_line))])
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
    # plot_average_velocities(200, [.05, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7], .3)
    # print(1)
    # plot_average_velocities(200, [.05, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7], .1)
    # print(1)
    # plot_average_velocities(200, [.05, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7], .5)
    # print(1)
    # plot_average_velocities(200, [.05, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7], .7)
    # r = Road(200, .1, .3)
    # r.visualize_system_evolution('evolution_rho=01', 100)
    # print(1)
    # r = Road(200, .2, .3)
    # r.visualize_system_evolution('evolution_rho=02', 100)
    # r = Road(200, .6, .3)
    # r.visualize_system_evolution('evolution_rho=06', 100)
    #r.visualize_system_evolution('test3', 50)
    for p in [.1, .2, .3, .4, .5, .6, .7]:
        plot_average_velocities('task_2_one_line',200, [.05,.1, .15,.2,.25, .3,.35, .4,.45, .5,.55, .6,.65, .7], p)
    # plot_average_velocities('two_lines_test',100, [.05,.1, .15,.2,.25, .3,.35, .4,.45, .5,.55, .6,.65, .7], 0.3, two_lines=True)
    # for p in [.1, .2, .3, .4, .5, .6, .7]:
    #     plot_average_velocities('task_2',200, [.05,.1, .15,.2,.25, .3,.35, .4,.45, .5,.55, .6,.65, .7], p)
    # plot_average_velocities('two_lines_test',200, [.05,.1, .15,.2,.25, .3,.35, .4,.45, .5,.55, .6,.65, .7], 0.3, two_lines=True)