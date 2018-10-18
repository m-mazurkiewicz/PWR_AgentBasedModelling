from collections import Counter
import copy


def hoshen_kapelman_alghoritm(ForestFire):
    burnt_trees_test = copy.deepcopy(ForestFire.grid)
    for x in range(ForestFire.height):
        for y in range(ForestFire.width):
            if burnt_trees_test[x][y] == 3:
                burnt_trees_test[x][y] = -1
            else:
                burnt_trees_test[x][y] = 0
    largest_label = 0
    for i in range(ForestFire.width * ForestFire.height):
        ForestFire.labels.append(i)
    for x in range(ForestFire.height):
        for y in range(ForestFire.width):
            if burnt_trees_test[x][y] == -1:
                top = ((x - 1 >= 0) and (burnt_trees_test[x - 1][y] != 0))
                left = ((y - 1 >= 0) and (burnt_trees_test[x][y - 1] != 0))
                if left == False and top == False:
                    largest_label += 1
                    burnt_trees_test[x][y] = largest_label
                elif left == True and top == False:
                    burnt_trees_test[x][y] = find(ForestFire, burnt_trees_test[x][y - 1])
                elif left == False and top == True:
                    burnt_trees_test[x][y] = find(ForestFire, burnt_trees_test[x - 1][y])
                else:
                    union(ForestFire, burnt_trees_test[x][y - 1], burnt_trees_test[x - 1][y])
                    burnt_trees_test[x][y] = find(ForestFire, burnt_trees_test[x][y - 1])
    for i in range(ForestFire.width):
        for j in range(ForestFire.height):
            a = burnt_trees_test[i][j]
            while a != ForestFire.labels[a]:
                a = ForestFire.labels[a]
            burnt_trees_test[i][j] = a
    d = dict()
    for i in range(ForestFire.width):
        d = Counter(burnt_trees_test[i]) + Counter(d)
    del d[0]
    return max((d.values()))
    #print(max(d.values()))


def find(ForestFire, x):
    y = x
    while not ForestFire.labels[y] == y:
        y = ForestFire.labels[y]
    while not ForestFire.labels[x] == x:
        z = ForestFire.labels[x]
        ForestFire.labels[x] = y
        x = z
    return y


def union(ForestFire, first_field, second_field):
    ForestFire.labels[ForestFire.find(first_field)] = ForestFire.find(second_field)