from List4.agent import Agent
import matplotlib.pyplot as plt


class Grid:
    def __init__(self, num_of_type_0=250, num_of_type_1=250, num_neighbors_type_0=10, num_neighbors_type_1=10,
                 staying_threshold_0=.5, staying_threshold_1=.5, num_of_rows=100, num_of_columns=100):
        self.num_of_type_0 = num_of_type_0
        self.num_of_type_1 = num_of_type_1
        self.num_neighbors_type_0 = num_neighbors_type_0
        self.num_neighbors_type_1 = num_neighbors_type_1
        self.staying_threshold_0 = staying_threshold_0
        self.staying_threshold_1 = staying_threshold_1
        self.num_of_rows = num_of_rows
        self.num_of_columns = num_of_columns
        self.empty_spots = self.create_table_of_empty_spots(self.num_of_rows, self.num_of_columns)
        self.agents = [Agent(0, self.num_neighbors_type_0, self.staying_threshold_0, self.empty_spots) for i in range(self.num_of_type_0)]
        self.agents.extend(Agent(1, self.num_neighbors_type_1, self.staying_threshold_1, self.empty_spots) for i in range(self.num_of_type_1))

    def create_table_of_empty_spots(self, num_of_rows, num_of_columns):
        empty_spots = []
        for i in range(num_of_rows):
            for j in range(num_of_columns):
                empty_spots.append((i, j))
        return empty_spots

    def run_algorithm(self, max_number_of_iterations=100):
        count = 1
        # ==  Loop until none wishes to move == #
        plot_distribution(self.agents, count)
        while True and count < max_number_of_iterations:
            print('Entering loop ', count)
            # plot_distribution(grid.agents, count)
            count += 1
            no_one_moved = True
            for agent in self.agents:
                old_location = agent.location
                agent.update(self.agents)
                if agent.location != old_location:
                    no_one_moved = False
            if no_one_moved:
                break
        plot_distribution(self.agents, count)
        print('Converged, terminating.')

    def calculate_similar_neighbour_index(self):
        similar_neighbour_index = 0
        for agent in self.agents:
            similar_neighbour_index += agent.fraction_of_neighbours_of_the_same_type(self.agents)
        return similar_neighbour_index / len(self.agents)


def plot_distribution(agents, cycle_num):
    "Plot the distribution of agents after cycle_num rounds of the loop."
    x_values_0, y_values_0 = [], []
    x_values_1, y_values_1 = [], []
    # == Obtain locations of each type == #
    for agent in agents:
        x, y = agent.location
        if agent.type == 0:
            x_values_0.append(x)
            y_values_0.append(y)
        else:
            x_values_1.append(x)
            y_values_1.append(y)
    fig, ax = plt.subplots(figsize=(8, 8))
    plot_args = {'markersize': 8, 'alpha': 0.6}
    ax.set_facecolor('azure')
    ax.plot(x_values_0, y_values_0, 'o', markerfacecolor='orange',  **plot_args)
    ax.plot(x_values_1, y_values_1, 'o', markerfacecolor='green', **plot_args)
    ax.set_title(f'Cycle {cycle_num-1}')
    plt.show()


if __name__ == '__main__':
    num_of_type_0 = 250
    num_of_type_1 = 250
    num_neighbors_0 = 10
    num_neighbors_1 = 15
    staying_threshold_0 = .5
    staying_threshold_1 = 2 / 3
    max_number_of_iterations = 100

    grid = Grid(num_of_type_0, num_of_type_1, num_neighbors_0, num_neighbors_1, staying_threshold_0, staying_threshold_1)
    grid.run_algorithm(max_number_of_iterations)
    print(grid.calculate_similar_neighbour_index())