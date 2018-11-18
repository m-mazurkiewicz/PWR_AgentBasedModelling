from List4.Agent import Agent
import matplotlib.pyplot as plt


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
    num_neighbors = 10      # Number of agents regarded as neighbors
    require_same_type = 5   # Want at least this many neighbors to be same type

    # == Create a list of agents == #
    agents = [Agent(0, num_neighbors, require_same_type) for i in range(num_of_type_0)]
    agents.extend(Agent(1, num_neighbors, require_same_type) for i in range(num_of_type_1))

    count = 1
    # ==  Loop until none wishes to move == #
    while True:
        print('Entering loop ', count)
        plot_distribution(agents, count)
        count += 1
        no_one_moved = True
        for agent in agents:
            old_location = agent.location
            agent.update(agents)
            if agent.location != old_location:
                no_one_moved = False
        if no_one_moved:
            break

    print('Converged, terminating.')