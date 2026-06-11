# [Problem 3558: Number of Ways to Assign Edge Weights I](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- We only care about the path from node 1 to some deepest node x. All other edges are ignored.
- Let L be the number of edges on that path (the maximum depth measured in edges).
- Each edge can be assigned weight 1 (odd) or 2 (even). The parity of the total path cost is determined solely by how many edges assigned weight 1 there are: sum parity = (number of 1s) mod 2.
- So among all 2^L assignments, exactly half will have an odd number of 1s (except the degenerate L=0 case). That suggests the answer is 2^{L-1}.
- Need to compute the maximum depth L from root 1 to any node in the tree (number of edges). Then answer = 2^{L-1} mod 1e9+7.

## Refining the problem, round 2 thoughts
- Compute depth using BFS (level-order) or iterative DFS to avoid recursion depth limits for n up to 1e5.
- BFS from node 1: count number of levels; max depth in edges = levels - 1.
- Edge cases: constraints say n >= 2 so L >= 1, so formula 2^{L-1} valid. If n could be 1, result should be 0 because no edges (but not relevant here).
- Complexity: building adjacency list O(n), BFS O(n), computing pow with modular exponentiation O(log MOD). Total O(n) time, O(n) space.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def numberOfWays(self, edges: List[List[int]]) -> int:
        MOD = 10**9 + 7
        n = len(edges) + 1
        # build adjacency
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        # BFS to compute number of levels
        q = deque([1])
        seen = [False] * (n + 1)
        seen[1] = True
        levels = 0
        while q:
            levels += 1
            for _ in range(len(q)):
                u = q.popleft()
                for w in adj[u]:
                    if not seen[w]:
                        seen[w] = True
                        q.append(w)
        max_depth = levels - 1  # number of edges from root to deepest node
        # answer = 2^(max_depth - 1) mod MOD (since we need odd sum)
        # max_depth >= 1 because n >= 2 per constraints
        return pow(2, max_depth - 1, MOD)
```

- Notes:
  - Key observation: parity of the path sum depends only on the count of edges assigned weight 1 (odd). Number of sequences of length L over {1,2} with an odd number of 1s is exactly 2^{L-1}.
  - Time complexity: O(n) to build adjacency & BFS.
  - Space complexity: O(n) for adjacency + seen + queue.