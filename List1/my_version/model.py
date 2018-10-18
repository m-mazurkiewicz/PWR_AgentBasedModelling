import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import queue
from collections import Counter

class ForestFire:
    def __init__(self, height=100, width=100, density=0.65):
        self.height = height
        self.width = width
        self.density = density
        self.grid = []
        self.burning_trees = queue.Queue()
        self.to_be_burn = queue.Queue()
        self.labels = []
        self.burned_trees = []

        for x in range(height):
            row = []
            for y in range(width):
                tree = 0
                if random.random() < self.density:
                    tree = 1
                    if x==0:
                        tree = 2
                        self.burning_trees.put((x,y))
                row.append(tree)
            self.grid.append(row)

    def print(self):
        for x in range(self.height):
            for y in range(self.width):
                print(self.grid[x][y], end=' ')
            print('\n')

    def burn_neighbors(self, tree):
        x = tree[0]
        y = tree[1]
        self.grid[x][y] = 3
        neighbors = []
        for i in [-1, 0, 1]:        #to add wind we may just add another numbers here
            for j in [-1, 0, 1]:
                if (x + i >=0) & (x + i < self.height) & (y + j >=0) & (y + j < self.height):
                    neighbors.append((x+i, y+j))
        #for more complex wind models we can do sth like that:
        # for i, j in [(1,2), (2,3)]: #and here put tuples with exact directions
        #     if (x + i >= 0) & (x + i < self.height) & (y + j >= 0) & (y + j < self.height):
        #         neighbors.append(self.grid[x + i][y + j])
        for x,y in neighbors:
            if self.grid[x][y] == 1:
                self.grid[x][y] = 2
                self.to_be_burn.put((x,y))

    def single_step(self):
        for i in range(self.burning_trees.qsize()):
            self.burn_neighbors(self.burning_trees.get())
        while not self.to_be_burn.empty():
            self.burning_trees.put(self.to_be_burn.get())

    def burn_forest(self):
        while not self.burning_trees.empty():
            self.single_step()

    def check_if_second_edge_is_reached(self):
        for i in range(self.width):
            if self.grid[self.height - 1][i] == 3:
                return True
        return False

    def animate_and_simulate(self, file_path_and_name, duration = 15):
        #pos = nx.spring_layout(self.graph, scale=1.5)
        image_magick = animation.writers['imagemagick']
        fps = np.ceil(20/ float(duration))
        writer = image_magick(fps=fps)

        fig = plt.figure()
        ax = plt.gca()
        plt.axis('off')
        #nx.draw_networkx(self.graph, pos=pos, ax=ax, with_labels=False, node_size=10)
        ax.imshow(self.grid)

        with writer.saving(fig, file_path_and_name+".gif", 100):
            while not self.burning_trees.empty():
                self.single_step()
                ax.imshow(self.grid)
                writer.grab_frame()
            #for i in self.coordinates:

            #nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=[i], node_size=50, node_color='g')
            #plt.title('time ' + str(t) + ', node ' + str(i))


    def hoshen_kapelman_alghoritm(self):
        burnt_trees_test = list(self.grid)
        for x in range(self.height):
            for y in range(self.width):
                if burnt_trees_test[x][y]==3:
                    burnt_trees_test[x][y]=-1
                else:
                    burnt_trees_test[x][y]=0
        largest_label = 0
        for i in range(self.width*self.height):
            self.labels.append(i)
        for x in range(self.height):
            for y in range(self.width):
                if burnt_trees_test[x][y] == -1:
                    top = ((x - 1 >= 0) and (burnt_trees_test[x - 1][y] != 0))
                    left = ((y - 1 >= 0) and (burnt_trees_test[x][y - 1] != 0))
                    if left==False and top==False:
                       largest_label+=1
                       burnt_trees_test[x][y]=largest_label
                    elif left == True and top == False:
                        burnt_trees_test[x][y] = self.find(burnt_trees_test[x][y-1])
                    elif left == False and top == True:
                        burnt_trees_test[x][y] = self.find(burnt_trees_test[x-1][y])
                    else:
                        self.union(burnt_trees_test[x][y-1], burnt_trees_test[x-1][y])
                        burnt_trees_test[x][y] = self.find(burnt_trees_test[x][y-1])
        for i in range(self.width):
            for j in range(self.height):
                a = burnt_trees_test[i][j]
                while a != self.labels[a]:
                    a = self.labels[a]
                burnt_trees_test[i][j] = a
        d = dict()
        for i in range(self.width):
            d = Counter(burnt_trees_test[i]) + Counter(d)
        del d[0]
        print(max(d.values()))


    def find(self, x):
        y = x
        while not self.labels[y] == y:
            y = self.labels[y]
        while not self.labels[x] == x:
            z = self.labels[x]
            self.labels[x] = y
            x = z
        return y

    def union(self, first_field, second_field):
        self.labels[self.find(first_field)] = self.find(second_field)