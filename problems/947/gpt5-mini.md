# [Problem 947: Most Stones Removed with Same Row or Column](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks for the maximum number of stones that can be removed given that a stone can be removed if it shares a row or column with another remaining stone. Removing as many stones as possible suggests leaving one stone per connected “group” (component) of stones connected by same-row or same-column relations. That smells like graph connectivity: build a graph where nodes are stones and edges exist between stones in the same row or same column; in each connected component of size k you can remove k-1 stones, so total removed = n - number_of_components.

To find components efficiently, union-find (DSU) or DFS/BFS on an adjacency representation works. Building full pairwise adjacency is O(n^2) in the worst case and unnecessary. Instead, use maps from row -> a representative stone index and col -> representative index: when visiting a stone, union it with the representative for its row (if any) and with the representative for its column (if any). This yields near-linear behavior.

## Refining the problem, round 2 thoughts
Edge cases: single stone -> 0 removed; multiple stones all isolated by unique rows and columns -> 0 removed; many stones sharing rows/cols -> remove n - components. Complexity: we want about O(n α(n)) time and O(n) extra space. Implementation detail: DSU with path compression and union by size/rank. Keep track of number of distinct components by counting unique DSU roots among indices that exist.

Alternative: treat rows and columns as nodes in a bipartite graph and union row and column nodes (with offset for columns) — works too. Simpler approach here is union-by-index using row_to_index and col_to_index maps.

## Attempted solution(s)
```python
from typing import List

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        # path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # union by size
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        return True

class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        n = len(stones)
        if n <= 1:
            return 0

        dsu = DSU(n)
        row_map = {}  # row value -> index of a stone seen with this row
        col_map = {}  # col value -> index of a stone seen with this column

        for i, (r, c) in enumerate(stones):
            if r in row_map:
                dsu.union(i, row_map[r])
            else:
                row_map[r] = i

            if c in col_map:
                dsu.union(i, col_map[c])
            else:
                col_map[c] = i

        # count distinct roots among all stones
        roots = set()
        for i in range(n):
            roots.add(dsu.find(i))

        # we can remove all stones except one per connected component
        return n - len(roots)
```
- Notes:
  - Approach: DSU on stone indices. For each stone, union it with any previously seen stone in the same row and same column using maps row_map and col_map. The number of removable stones equals n minus the number of connected components.
  - Time complexity: O(n α(n)) where α is the inverse Ackermann function (practically constant). Each stone processes constant-time map lookups and at most two unions.
  - Space complexity: O(n) for DSU arrays and O(n) for maps in the worst case.