# [Problem 2392: Build a Matrix With Conditions](https://leetcode.com/problems/build-a-matrix-with-conditions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to place numbers 1..k into distinct cells of a k x k matrix such that given row constraints (a should be in a row above b) and column constraints (c should be in a column left of d) are satisfied. This essentially requires determining a relative ordering of the numbers for rows and independently for columns. That screams topological sorting on two directed graphs: one for row constraints and one for column constraints. If either graph has a cycle, there is no valid placement (return []). Otherwise, topological orders give exact row and column indices (0..k-1) for each number, and we can place number i at (row_pos[i], col_pos[i]). Need to ensure we include nodes with no incoming/outgoing edges. Also watch out for duplicate constraints so indegree counting isn't incremented twice for the same directed edge.

## Refining the problem, round 2 thoughts
- Use Kahn's algorithm (BFS topological sort) because it's simple and detects cycles (order length < k).
- Build adjacency lists and indegree arrays for 1..k. Use a set to deduplicate edges to avoid overcounting indegrees.
- If topo sort succeeds for both row and column graphs, map each number to its index in the corresponding topo order (row index and column index) and fill the matrix.
- Complexity: building graph + topo sort: O(k + E) per graph (E = number of constraints). Building matrix O(k^2) space and O(k) placements. Constraints allow k up to 400, edges up to 1e4 — this is fine.
- Edge cases: duplicate edges, isolated nodes, cycles (return empty list), constraints are 1-indexed — keep indices consistent.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def topo_sort(k: int, edges: List[List[int]]) -> List[int]:
            adj = [[] for _ in range(k + 1)]
            indeg = [0] * (k + 1)
            seen = set()
            for u, v in edges:
                if (u, v) not in seen:
                    seen.add((u, v))
                    adj[u].append(v)
                    indeg[v] += 1

            dq = deque()
            for node in range(1, k + 1):
                if indeg[node] == 0:
                    dq.append(node)

            order = []
            while dq:
                u = dq.popleft()
                order.append(u)
                for v in adj[u]:
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        dq.append(v)

            if len(order) != k:
                return []  # cycle detected or missing nodes
            return order

        row_order = topo_sort(k, rowConditions)
        if not row_order:
            return []

        col_order = topo_sort(k, colConditions)
        if not col_order:
            return []

        row_pos = {num: i for i, num in enumerate(row_order)}
        col_pos = {num: i for i, num in enumerate(col_order)}

        matrix = [[0] * k for _ in range(k)]
        for num in range(1, k + 1):
            r = row_pos[num]
            c = col_pos[num]
            matrix[r][c] = num

        return matrix
```
- Notes about the solution:
  - We perform two independent topological sorts (one for rows, one for columns). If either returns an ordering of length < k, constraints are contradictory → return [].
  - Use a set to avoid counting duplicate edges multiple times.
  - Time complexity: O(k + R + C) where R = len(rowConditions), C = len(colConditions). Building the k x k matrix uses O(k^2) space and O(k) placements.
  - Space complexity: O(k + R + C + k^2) total; adjacency and indegree arrays use O(k + R + C), matrix uses O(k^2).