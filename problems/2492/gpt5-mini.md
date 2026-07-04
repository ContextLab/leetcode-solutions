# [Problem 2492: Minimum Score of a Path Between Two Cities](https://leetcode.com/problems/minimum-score-of-a-path-between-two-cities/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimum possible "score" among all paths from city 1 to city n, where the score of a path is the minimum edge weight along that path. At first glance this looks like a "maximin"/"minimize the minimum" kind of problem (like bottleneck paths), but the phrasing "minimum possible score" means we want the smallest attainable minimum-edge along some path from 1 to n.

One observation: if there is any edge with very small weight inside the connected component that contains nodes 1 and n, we can construct a path from 1 to n that passes through that edge (go from 1 to one endpoint, take that edge, then go from the other endpoint to n). Since revisiting nodes/edges is allowed, this is valid. Therefore the answer should be the minimum edge weight among all edges in the connected component of node 1 (which contains n by problem guarantee).

So we just need to find all nodes reachable from 1 and take the minimum weight among all edges incident to that reachable set. That suggests a simple BFS/DFS (or union-find) over the graph and tracking the minimal edge weight seen.

## Refining the problem, round 2 thoughts
- Use BFS/DFS (iterative to avoid recursion depth issues) starting from node 1, mark visited nodes, and while exploring edges update the running minimum weight.
- Alternatively union-find: union all edges then scan edges whose endpoint's root equals root(1) and take the minimum weight.
- Time complexity must be near O(n + m) since n,m up to 1e5. BFS/DFS/union-find all meet this.
- Space O(n + m) for adjacency or parent arrays.
- Edge cases: problem guarantees at least one path 1 -> n so n is reachable from 1; the component will contain at least one edge. If some node is isolated, it doesn't matter.
- I'll implement BFS using deque and adjacency list (list-of-lists) for speed and simplicity.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for a, b, w in roads:
            adj[a].append((b, w))
            adj[b].append((a, w))
        
        # BFS from node 1 to find its connected component and track minimum edge weight
        visited = [False] * (n + 1)
        dq = deque([1])
        visited[1] = True
        min_edge = float('inf')
        
        while dq:
            u = dq.popleft()
            for v, w in adj[u]:
                # consider every edge we encounter in the component
                if w < min_edge:
                    min_edge = w
                if not visited[v]:
                    visited[v] = True
                    dq.append(v)
        
        return min_edge
```
- Approach: BFS from node 1, update the minimum edge weight seen while traversing the component. Return that minimum.
- Correctness rationale: any edge inside the connected component containing nodes 1 and n can be included in some path from 1 to n (go from 1 to one endpoint, traverse the edge, then go to n), so the minimum edge weight in the component is attainable as the score of some path. Conversely every path from 1 to n uses only edges in that component, so its score is at least the minimum weight among those edges — hence the global minimum over paths equals the minimum edge weight in the component.
- Time complexity: O(n + m) to build adjacency list and traverse the component (m = number of roads).
- Space complexity: O(n + m) for adjacency list and visited array.