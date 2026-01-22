# [Problem 2685: Count the Number of Complete Components](https://leetcode.com/problems/count-the-number-of-complete-components/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count connected components that are "complete" (i.e., every pair of vertices in the component has an edge). A complete component with k vertices must have exactly k*(k-1)/2 edges. So approach: find connected components, compute their sizes and how many edges lie entirely inside each component, and then check the edges count equals the required amount.

For finding components we can use DFS/BFS or Union-Find (DSU). DSU is convenient: union all edges, then for each node get its root to compute component size; for each edge increment the edge-count for the root (each undirected edge is given once in input so no need to divide counts). Finally test edges_count == k*(k-1)/2.

Edge cases: isolated vertex (k=1, edges=0) should count as complete. No edges at all should treat all nodes as complete components.

## Refining the problem, round 2 thoughts
- Do unions first so all nodes belonging to same connected component share same representative.
- After unions, iterate nodes to compute sizes per root.
- Iterate edges again and increment edges_count[root(find(u))] once per edge.
- Check for each component if edges_count == size*(size-1)//2.
- Complexity: O(n + m * alpha(n)), with n <= 50 and m up to n*(n-1)/2. Memory O(n).

## Attempted solution(s)
```python
from collections import defaultdict

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0]*n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[ry] < self.rank[rx]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

class Solution:
    def countCompleteComponents(self, n: int, edges: list[list[int]]) -> int:
        dsu = DSU(n)
        # Union all edges
        for u, v in edges:
            dsu.union(u, v)

        # Count sizes per component root
        size = defaultdict(int)
        for i in range(n):
            r = dsu.find(i)
            size[r] += 1

        # Count edges per component (each input edge counts once)
        edge_count = defaultdict(int)
        for u, v in edges:
            r = dsu.find(u)  # same as dsu.find(v)
            edge_count[r] += 1

        # Check complete condition for each component root
        complete = 0
        for r, k in size.items():
            expected = k * (k - 1) // 2
            if edge_count.get(r, 0) == expected:
                complete += 1

        return complete
```
- Notes:
  - We use DSU to group connected vertices. After all unions, every vertex's representative identifies its component.
  - size[root] counts number of vertices in that component.
  - edge_count[root] counts number of edges inside that component (each undirected edge appears once in input).
  - A component is complete iff edge_count == k*(k-1)/2.
  - Time complexity: O(n + m * α(n)) where m = len(edges) and α is inverse-Ackermann (practically constant). Space complexity: O(n + m) for bookkeeping (mostly O(n)).