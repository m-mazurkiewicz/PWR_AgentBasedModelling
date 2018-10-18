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
        self.labels_cnt = []

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





    # def print(self):
    #     np.random.seed(19680801)
    #     data = np.random.random((50, 50, 50))
    #
    #     fig, ax = plt.subplots()
    #
    #     for i in range(len(data)):
    #         ax.cla()
    #         ax.imshow(data[i])
    #         ax.set_title("frame {}".format(i))
    #         # Note that using time.sleep does *not* work here!
    #         plt.pause(0.1)

    def animate_and_simulate(self, filePathAndName, duration = 15):
        #pos = nx.spring_layout(self.graph, scale=1.5)
        ImageMagick = animation.writers['imagemagick']
        fps = np.ceil(10/ float(duration))
        writer = ImageMagick(fps=fps)

        fig = plt.figure()
        ax = plt.gca()
        plt.axis('off')
        #nx.draw_networkx(self.graph, pos=pos, ax=ax, with_labels=False, node_size=10)
        ax.imshow(self.grid)

        t = 0
        with writer.saving(fig, filePathAndName+".gif", 100):
            while not self.burning_trees.empty():
                self.single_step()
                ax.imshow(self.grid)
                writer.grab_frame()
            #for i in self.coordinates:

            #nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=[i], node_size=50, node_color='g')
            #plt.title('time ' + str(t) + ', node ' + str(i))

            t += 1




    def hoshen_kapelman_alghoritm(self):
        burnt_trees_test = list(self.grid)
        for x in range(self.height):
            for y in range(self.width):
                if burnt_trees_test[x][y]==3:
                    burnt_trees_test[x][y]=-1
                else:
                    burnt_trees_test[x][y]=0
        largest_label = 0
        #union = UnionFind(ForestFire.height, ForestFire.width)
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
                        #union.labels[union.get_coor((x, y))] = union.find(union.get_coor((x - 1, y)))
                    elif left == False and top == True:
                        #union.labels[union.get_coor((x, y))] = union.find(union.get_coor((x, y - 1)))
                        burnt_trees_test[x][y] = self.find(burnt_trees_test[x-1][y])
                    else:
                        #union.union(union.get_coor((x - 1, y)), union.get_coor((x, y - 1)))
                        self.union(burnt_trees_test[x][y-1], burnt_trees_test[x-1][y])
                        #union.labels[union.get_coor((x, y))] = union.find(union.get_coor((x - 1, y)))
                        burnt_trees_test[x][y] = self.find(burnt_trees_test[x][y-1])

        d = dict()

        for i in range(self.width):
            d = Counter(burnt_trees_test[i]) + Counter(d)

        print(d)
        del d[0]
        print(d)
        print(max(d.values()))

        for i in range(self.width):
            for j in range(self.height):
                a = burnt_trees_test[i][j]
                while a != self.labels[a]:
                    a = self.labels[a]
                burnt_trees_test[i][j] = a

       # Counter(burnt_trees_test)
        # for x in range(self.height):
        #     for y in range(self.width):
        #         print(burnt_trees_test[x][y], end=' ')
        #     print('\n')


    # def find(self, x):
    #     x = self.get_coor(x)
    #     y = x
    #     while not self.labels[y] == y:
    #         y = self.labels[y]
    #     while not self.labels[x] == x:
    #         z = self.labels[x]
    #         self.labels[x] = y
    #         x = z
    #     return y
    #
    # def union(self, first_field, second_field):
    #     self.labels[self.find(first_field)] = self.find(second_field)
    #
    # def get_coor(self, p):
    #     i, j = p
    #     return self.width * i + j

    def find(self, x):
        """Function find parent for node"""
        y = x
        while self.labels[y] != y:
            y = self.labels[y]
        while self.labels[x] != x:
            z = self.labels[x]
            self.labels[x] = y
            x=z
        return y

    def union(self, x, y):
        """Function that sum two clusters"""
        self.labels[self.find(x)] = self.find(y)

    def hohesh_kopelman(self):
        """Function create clusters of burned trees"""
        # if trees == 0:
        #     #self.burned_trees = np.subtract(self.forest, self.forest_hk)
        # else:
        for i in range(self.width):
            for j in range(self.height):
                if self.grid[i][j] == 3:
                    self.grid[i][j] = -1
                else:
                    self.grid[i][j] = 0
        self.burned_trees = self.grid
        a = self.width**2
        for i in range(0,a):
            self.labels.append(i)
        largest_label = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.burned_trees[j][i] == -1:
                    if j == 0 and i == 0:
                        largest_label = largest_label + 1
                        self.burned_trees[j][i] = largest_label
                    elif j == 0 and i != 0:
                        left = self.burned_trees[j][i-1]
                        if left == 0:
                            largest_label = largest_label + 1
                            self.burned_trees[j][i] = largest_label
                        else:
                            self.burned_trees[j][i] = self.find(left)
                    elif j != 0 and i == 0:
                        top = self.burned_trees[j-1][i]
                        if top == 0:
                            largest_label = largest_label +1
                            self.burned_trees[j][i] = largest_label
                        else:
                            self.burned_trees[j][i] = self.find(top)
                    else:
                        top = self.burned_trees[j][i-1]
                        left = self.burned_trees[j-1][i]
                        if left == 0 and top == 0:
                            largest_label = largest_label + 1
                            self.burned_trees[j][i] = largest_label
                        elif left == 0 and top != 0:
                            self.burned_trees[j][i] = self.find(top)
                        elif left != 0 and top == 0:
                            self.burned_trees[j][i] = self.find(left)
                        else:
                            self.union(left, top)
                            self.burned_trees[j][i] = self.find(left)
        for i in range(self.width):
            for j in range(self.height):
                a = self.burned_trees[i][j]
                while a != self.labels[a]:
                    a = self.labels[a]
                self.burned_trees[i][j] = a


    def biggest_cluster (self):
        """Function that finds size of biigest cluster among burned trees"""
        for i in range(self.width):
            for j in range(self.width):
                self.labels_cnt.append([i*self.width+j, 0])
        for i in range(self.width):
            for j in range(self.height):
                k = self.burned_trees[i][j]
                self.labels_cnt[k][1] = self.labels_cnt[k][1] + 1
        self.labels_cnt.pop(0)
        max_cnt = max([el[1] for el in self.labels_cnt])
        max_lab = 0
        i=0
        max_lab = self.labels_cnt[i][0]
        #print(max_lab)
        i = i+1
        while self.labels_cnt[i][1] != max_cnt:
            max_lab = self.labels_cnt[i][0]
            #print(max_lab)
            i=i+1
        max_lab = self.labels_cnt[i][0]
        #print(max_lab)
        print("size max cluster:")
        print(max_cnt)
        print("label max cluster:")
        print(max_lab)
        print(self.labels_cnt)
        return max_lab


# class UnionFind:
#     def __init__(self, m, n):
#         self.m, self.n = m, n
#         self.labels = [i for i in range(m * n)]
#         self.size = [1] * (m * n)
#
#     def get_coor(self, p):
#         i, j = p
#         return self.m * i + j
#
#     def find(self, x):
#         x = self.get_coor(x)
#         y = x
#         while not self.labels[y] == y:
#             y = self.labels[y]
#         while not self.labels[x] == x:
#             z = self.labels[x]
#             self.labels[x] = y
#             x = z
#         return y
#
#     def union(self, first_field, second_field):
#         self.labels[self.find(first_field)] = self.find(second_field)
