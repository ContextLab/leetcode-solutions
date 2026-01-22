# [Problem 3203: Find Minimum Diameter After Merging Two Trees](https://leetcode.com/problems/find-minimum-diameter-after-merging-two-trees/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have two trees. We must add exactly one edge between a node in tree1 and a node in tree2 and want the minimum possible diameter of the resulting combined tree.

A classic property: for a tree with diameter D, its radius r = ceil(D/2). If we connect the two trees by joining their centers (nodes achieving the radius), the new longest path that crosses the new edge will have length r1 + 1 + r2. The overall diameter after connecting is the maximum of:
- the maximum diameter that already exists inside either original tree (D1 or D2), and
- the longest path that goes through the new edge (r1 + 1 + r2).

Therefore the optimal strategy is to connect centers (or appropriate nodes) to minimize the cross-tree longest path, and the minimal resulting diameter is:
max(D1, D2, ceil(D1/2) + 1 + ceil(D2/2)).

So we only need each tree's diameter D (and then radius r = ceil(D/2)). To get a tree's diameter we can use two BFS/DFS passes: BFS from any node to find a farthest node u, then BFS from u to find farthest distance D.

This yields an O(n+m) time solution and O(n+m) space.

## Refining the problem, round 2 thoughts
Edge cases:
- Trees of size 1 (diameter 0) — formula still works: r = 0, cross path = 0+1+0 = 1.
- Larger trees with even/odd diameters — use ceil(D/2) = (D+1)//2.
- We only need integer distances; BFS on trees is fine (no weights).

Complexities:
- Building adjacency lists: O(n) per tree.
- BFS twice per tree: O(n) per tree.
- Total time O(n + m), total space O(n + m).

We'll implement a helper to compute diameter and radius for a given tree and apply the formula.

## Attempted solution(s)
```python
from collections import deque
from typing import List, Tuple

def diameter_and_radius(n: int, edges: List[List[int]]) -> Tuple[int, int]:
    if n == 1:
        return 0, 0
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def bfs(start: int):
        dist = [-1] * n
        q = deque([start])
        dist[start] = 0
        far = start
        while q:
            u = q.popleft()
            for w in adj[u]:
                if dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)
                    far = w
        return far, dist

    # first BFS to find one endpoint of diameter
    u, _ = bfs(0)
    # second BFS from u to get distances and diameter
    v, dist_u = bfs(u)
    diameter = max(dist_u)  # distance to farthest node from u
    radius = (diameter + 1) // 2  # ceil(diameter/2)
    return diameter, radius

class Solution:
    def minimizeDiameter(self, edges1: List[List[int]], edges2: List[List[int]]) -> int:
        n = len(edges1) + 1
        m = len(edges2) + 1
        D1, r1 = diameter_and_radius(n, edges1)
        D2, r2 = diameter_and_radius(m, edges2)
        return max(D1, D2, r1 + 1 + r2)
```
- Notes:
  - We compute each tree's diameter using two BFS passes (standard tree diameter technique).
  - radius = ceil(D/2) computed as (D+1)//2.
  - Final answer is max(D1, D2, r1 + 1 + r2).
  - Time complexity: O(n + m) where n and m are node counts of the two trees.
  - Space complexity: O(n + m) for adjacency lists and BFS arrays.