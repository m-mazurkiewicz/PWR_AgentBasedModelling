from List1.my_version.model import ForestFire

def hoshen_kapelman_alghoritm(ForestFire):
    #labels = ForestFire.grid
    #largest_label = 0
    UnionFind(ForestFire.height, ForestFire.width)
    for x in range(ForestFire.height):
        for y in range(ForestFire.width):
            if ForestFire.grid[x][y] == 3:
                left = ((x-1>0) & ForestFire.grid[x-1][y]==3)
                right = ((y-1>0) & ForestFire.grid[x][y-1]==3)
                #if left==False & right==False:
                #    largest_label+=1
                #    labels[x][y]=largest_label
                if left==True & right==False:
                    UnionFind.labels[UnionFind.get_coor((x,y))] = UnionFind.find(UnionFind.get_coor((x-1, y)))
                elif left==False & right==True:
                    UnionFind.labels[UnionFind.get_coor((x, y))] = UnionFind.find(UnionFind.get_coor((x, y-1)))
                    #labels[x][y]=find((x,y-1))
                else:
                    UnionFind.union(UnionFind.get_coor((x-1, y)), UnionFind.get_coor((x, y-1)))
                    #union((x-1, y), (x, y-1))
                    UnionFind.labels[UnionFind.get_coor((x, y))] = UnionFind.find(UnionFind.get_coor((x - 1, y)))
                    #labels[x][y] = find((x-1, y))
    print(UnionFind.labels)


class UnionFind:
    def __init__(self, m, n):
        self.m, self.n = m, n
        self.labels = [i for i in range(m * n)]
        self.size = [1] * (m * n)

    def get_coor(self, p):
        i, j = p
        return self.m * i + j

    def find(self, x):
        x = self.get_coor(x)
        y = x
        while not self.labels[y] == y:
            y= self.labels[y]
        while not self.labels[x] == x:
            z = self.labels[x]
            self.labels[x] = y
            x = z
        return y

    def union(self, first_field, second_field):
        self.labels[self.find(first_field)] = self.find(second_field)



# def union(first_field, second_field):
#     labels[find(first_field)] = find(second_field)
#
# def find(coordinates):
#     x, y = coordinates
#     while not labels[x][y] == (x, y):
#         x, y = labels[x][y]
#     while not labels[coordinates[0]][coordinates[1]] == coordinates:
#         a, b = labels[coordinates[0]][coordinates[1]]
#         labels[coordinates[0]][coordinates[1]] = (x, y)
#         coordinates = (a, b)
#     return x, y

# class UF:
#     """An implementation of union find data structure.
#     It uses weighted quick union by rank with path compression.
#     """
#
#     def __init__(self, N):
#         """Initialize an empty union find object with N items.
#
#         Args:
#             N: Number of items in the union find object.
#         """
#
#         self._id = list(range(N))
#         self._count = N
#         self._rank = [0] * N
#
#     def find(self, p):
#         """Find the set identifier for the item p."""
#
#         id = self._id
#         while p != id[p]:
#             p = id[p] = id[id[p]]   # Path compression using halving.
#         return p
#
#     def count(self):
#         """Return the number of items."""
#
#         return self._count
#
#     def connected(self, p, q):
#         """Check if the items p and q are on the same set or not."""
#
#         return self.find(p) == self.find(q)
#
#     def union(self, p, q):
#         """Combine sets containing p and q into a single set."""
#
#         id = self._id
#         rank = self._rank
#
#         i = self.find(p)
#         j = self.find(q)
#         if i == j:
#             return
#
#         self._count -= 1
#         if rank[i] < rank[j]:
#             id[i] = j
#         elif rank[i] > rank[j]:
#             id[j] = i
#         else:
#             id[j] = i
#             rank[i] += 1
#
#     def __str__(self):
#         """String representation of the union find object."""
#         return " ".join([str(x) for x in self._id])
#
#     def __repr__(self):
#         """Representation of the union find object."""
#         return "UF(" + str(self) + ")"
