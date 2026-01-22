# [Problem 959: Regions Cut By Slashes](https://leetcode.com/problems/regions-cut-by-slashes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This problem describes an n x n grid of characters '/', '\', or ' ' where each single cell is partitioned by the slash characters and we must count the number of connected regions. Immediately I recall two common approaches:

- Expand each 1x1 cell into a finer grid (e.g., 3x3) and treat slashes as blocked cells, then count connected components of empty cells.
- Use a union-find (disjoint set) by splitting each cell conceptually into 4 triangular regions (top, right, bottom, left). Inside a cell, depending on the character, some of these 4 subregions are connected; across neighboring cells, matching subregions connect. Then count how many disjoint sets remain.

The union-find with 4-subcells is memory/time efficient and straightforward to implement. I'll use that: represent each cell with 4 nodes, union internal edges according to the slash type, and union across neighboring cells (right and down connections). The number of root sets equals the number of regions.

## Refining the problem, round 2 thoughts
Mapping the 4 subregions to indices consistently is important. I'll use:
- 0 = top
- 1 = right
- 2 = bottom
- 3 = left

For characters:
- ' ' (space): all four subregions inside the cell are connected (union 0-1, 1-2, 2-3).
- '/' : this slash runs from top-right to bottom-left, effectively separating top-right from bottom-left. The internal unions that remain are top with left, and right with bottom -> union(0,3) and union(1,2).
- '\' : runs from top-left to bottom-right; the internal unions that remain are top with right, and bottom with left -> union(0,1) and union(2,3).

Neighbor connections:
- current cell's bottom (2) connects with cell below's top (0).
- current cell's right (1) connects with cell to the right's left (3).

Edge cases:
- n as small as 1.
- All blank cells (should give 1 region).
- Mixture of slashes producing many small regions.

Complexity:
- We have 4 * n * n nodes. Each union/find operation is nearly O(1) amortized (inverse Ackermann). So time is O(n^2 * α(N)) ~ O(n^2). Space is O(n^2).

Now I'll provide the full working Python solution using DSU.

## Attempted solution(s)
```python
class Solution:
    def regionsBySlashes(self, grid):
        """
        :type grid: List[str]
        :rtype: int
        """
        n = len(grid)
        # DSU for 4 * n * n nodes
        N = 4 * n * n
        parent = list(range(N))
        rank = [0] * N

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return False
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
            return True

        def node(i, j, k):
            # i, j: cell coordinates, k in [0..3] subregion
            return (i * n + j) * 4 + k

        for i in range(n):
            for j in range(n):
                ch = grid[i][j]
                # internal unions based on character
                if ch == ' ':
                    # connect all four
                    union(node(i, j, 0), node(i, j, 1))
                    union(node(i, j, 1), node(i, j, 2))
                    union(node(i, j, 2), node(i, j, 3))
                elif ch == '/':
                    # top with left, right with bottom
                    union(node(i, j, 0), node(i, j, 3))
                    union(node(i, j, 1), node(i, j, 2))
                elif ch == '\\':
                    # top with right, bottom with left
                    union(node(i, j, 0), node(i, j, 1))
                    union(node(i, j, 2), node(i, j, 3))

                # connect to right neighbor: current right (1) with right cell left (3)
                if j + 1 < n:
                    union(node(i, j, 1), node(i, j + 1, 3))

                # connect to down neighbor: current bottom (2) with below cell top (0)
                if i + 1 < n:
                    union(node(i, j, 2), node(i + 1, j, 0))

        # count distinct roots
        roots = set()
        for x in range(N):
            roots.add(find(x))
        return len(roots)
```
- Notes on approach:
  - Each cell is partitioned into 4 subregions. Internal unions depend on the character in the cell; neighbor unions connect adjacent subregions across cell boundaries.
  - The number of unique DSU roots after all unions is the number of regions.
  - Time complexity: O(n^2 * α(4n^2)) ≈ O(n^2). Space complexity: O(n^2) for the DSU arrays.
  - Alternative approach: expand each cell to a 3x3 grid and count connected components of empty pixels. That approach works too but uses more memory and a simpler flood-fill. The union-find 4-subcell approach is cleaner and efficient.