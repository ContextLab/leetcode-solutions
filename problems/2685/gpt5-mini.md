# [Problem 2685: Count the Number of Complete Components](https://leetcode.com/problems/count-the-number-of-complete-components/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share my internal stream-of-consciousness. Instead, here is a concise, non-sensitive summary of the approach:
- We need to identify connected components and determine whether each component is a complete graph (clique).
- For a component with k vertices, it is complete iff it has exactly k*(k-1)/2 edges.
- Use Union-Find (Disjoint Set Union) to group vertices into components while counting the number of vertices and edges per component. Then check the condition for each root.

## Refining the problem, round 2 thoughts
I can’t provide internal iterative thought process, but here are concise refinements and edge-case notes:
- When processing each undirected edge, increment the edge count for the component. If the two endpoints are already in the same component, increment that component's edge count by 1; otherwise, merge components and sum their edge counts plus the new edge.
- Edge cases: isolated vertices (k=1, edges=0) count as complete components. No edges means all vertices are complete components.
- Time complexity: O(n + m) (amortized inverse-Ackermann for DSU). Space: O(n).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        size = [1] * n
        edge_count = [0] * n  # number of edges in the component whose root is i

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra = find(a)
            rb = find(b)
            if ra == rb:
                # edge inside the same component
                edge_count[ra] += 1
                return
            # union by size: attach smaller to larger
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            # combine edge counts and add this new edge
            edge_count[ra] += edge_count[rb] + 1

        for u, v in edges:
            union(u, v)

        ans = 0
        for i in range(n):
            if parent[i] == i:
                k = size[i]
                e = edge_count[i]
                if e == k * (k - 1) // 2:
                    ans += 1
        return ans
```
- Notes on approach:
  - We use DSU to maintain component roots, sizes (number of vertices), and edge counts per component.
  - For each input edge, either increment the edge count of the existing component (if endpoints already connected) or merge components and combine sizes and edge counts (plus one for the merging edge).
  - After processing all edges, each root represents a component; check whether edge_count == k*(k-1)/2 where k is the component size.

- Complexity:
  - Time: O(n + m * α(n)) ≈ O(n + m), where m = len(edges) and α is the inverse Ackermann function (negligible).
  - Space: O(n) for parent, size, and edge_count arrays.