import random
import numpy as np

class UnionFind:
    def __init__(self, m, n):
        self.m, self.n = m, n
        self.root = [i for i in range(m * n)]
        self.size = [1] * (m * n)

    def union(self, p1, p2):
        p1, p2 = self.getcoor(p1), self.getcoor(p2)
        root1 = self.find(p1)
        root2 = self.find(p2)
        if root1 == root2: return
        self.root[root2] = root1
        self.size[root1] += self.size[root2]

    def find(self, p):
        if isinstance(p, list):
            p = self.getcoor(p)
        while p != self.root[p]:
            p = self.root[p]
        return p

    def getcoor(self, p):
        i, j = p
        return self.m * i + j

    def getans(self, i, j, grid):
        """
        calc sum of all the unique adjacent islands + 1
        """
        seen = set()
        res = 0
        for di, dj in [[0, 1], [1, 0], [-1, 0], [0, -1]]:
            ni, nj = i + di, j + dj
            if not -1 < ni < self.m or not -1 < nj < self.n: continue  # invalid coor
            if grid[ni][nj] == 0: continue  #
            rij = self.find([ni, nj])
            if rij in seen: continue  # not unique
            seen.add(rij)

            res += self.size[rij]
        return res + 1


class Solution:
    def __init__(self, grid):
        self.grid = grid

    def largestIsland(self):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        #if not grid: return 0
        m, n = len(self.grid), len(self.grid[0])
        ans = 0
        uf = UnionFind(m, n)
        for i in range(m):  # init union-find of grid
            for j in range(n):
                #if not self.grid[i][j]==3: continue
                if i < m - 1 and self.grid[i + 1][j] == 1:
                    uf.union([i, j], [i + 1, j])
                if j < n - 1 and self.grid[i][j + 1] == 1:
                    uf.union([i, j], [i, j + 1])

        for i in range(m):
            for j in range(n):
                if self.grid[i][j] == 0:
                    ans = max(ans, uf.getans(i, j, self.grid))

        print(np.sum(self.grid))
        return ans if ans else m * n

    def print(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                print(self.grid[x][y], end=' ')
            print('\n')

grid = []
for x in range(5):
    row = []
    for y in range(5):
        tree = 0
        if random.random() < .4:  # self.density:
            tree = 1
            # if x==0:
            #    tree = [x, y, 2]
            #    self.burning_trees.put((x,y))
        row.append(tree)
    grid.append(row)

check = Solution(grid)
check.print()
print(check.largestIsland())