# [Problem 3620: Network Recovery Pathways](https://leetcode.com/problems/network-recovery-pathways/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the path from 0 to n-1 that maximizes the minimum edge cost (the bottleneck) subject to two constraints: all intermediate nodes are online, and the total sum of edge costs on the path is ≤ k. This is reminiscent of "maximize minimum" problems that are commonly solved by binary searching the threshold (candidate minimum edge cost T) and checking feasibility for that T.

If we fix T, then any path whose minimum edge cost ≥ T must use only edges with cost ≥ T. So the feasibility check becomes: is there a path from 0 to n-1 using only edges with cost ≥ T, visiting only online nodes, whose total sum of edge costs ≤ k?

The input graph is a DAG. For shortest-paths (by total cost) in a DAG we can compute distances in topological order in O(n+m). So we can:
- Precompute a topological order once.
- For a candidate T, iterate nodes in topo order and relax only edges with cost ≥ T and whose endpoints are online.
- If the distance to n-1 ≤ k, T is feasible.

Binary search T over the set of existing edge costs (unique costs) to find the largest feasible T. Complexity should be O((n+m) + (m * log M)) where M is number of unique costs (≤ m).

Edge cases: no path satisfying ≤ k -> return -1; costs may be zero; some nodes offline (we must not pass through them).

## Refining the problem, round 2 thoughts
- Since graph is DAG, using topological DP for shortest distances is faster and simpler than Dijkstra for each T, and gives O(n+m) per check.
- We should precompute topological order using Kahn's algorithm. Even if some nodes are offline, the topo order of the full graph is valid; during checks we’ll simply ignore edges leading to offline nodes and skip relaxations for offline nodes (except start and end which are always online per constraints).
- To limit binary search domain, use the sorted unique set of edge costs rather than searching over [0, maxcost]. This ensures O(log m) steps and only meaningful thresholds are tested.
- Prune relaxation when dist[u] > k (nonnegative edge costs guarantee extending such a path can’t get ≤ k).
- If there are no edges at all, automatically return -1 (unless n==1, but per constraints n>=2).
- Time complexity: building topo O(n+m), each check O(n + m_filtered) but worst-case O(n+m), repeated O(log m) times => overall O((n+m) log m). Space O(n+m).

Potential pitfalls:
- Make sure to not use offline nodes as intermediate nodes. That means for any edge u->v considered, both u and v must be online (u can be 0 and v can be n-1, but constraints guarantee 0 and n-1 are online).
- Since edge costs can be 0, ensure checking equality (≥ T) handles zeros correctly.
- Distances may become large (k up to 5e13), use a large INF (e.g., 1e30) to avoid overflow.

## Attempted solution(s)
```python
from typing import List
from collections import deque

class Solution:
    def maximumMinimumScore(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        n = len(online)
        # Build adjacency and indegree for topological sort
        adj = [[] for _ in range(n)]
        indeg = [0] * n
        costs = []
        for u, v, c in edges:
            adj[u].append((v, c))
            indeg[v] += 1
            costs.append(c)

        # If no edges, no path (n >= 2), return -1
        if not costs:
            return -1

        # Topological order (Kahn)
        q = deque()
        for i in range(n):
            if indeg[i] == 0:
                q.append(i)
        topo = []
        while q:
            u = q.popleft()
            topo.append(u)
            for v, _ in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        # (Graph guaranteed to be a DAG by problem statement.)

        # Unique sorted costs for binary search
        uniq = sorted(set(costs))

        INF = 10**30

        def feasible(T: int) -> bool:
            # shortest path in DAG using only edges with cost >= T and only online nodes
            dist = [INF] * n
            dist[0] = 0
            for u in topo:
                # prune unreachable or already exceeding k
                if dist[u] == INF or dist[u] > k:
                    continue
                # If u is offline (shouldn't be 0 or n-1 as per constraints), skip
                if not online[u]:
                    continue
                for v, c in adj[u]:
                    if c >= T and online[v]:
                        nd = dist[u] + c
                        if nd < dist[v]:
                            dist[v] = nd
            return dist[n-1] <= k

        # Binary search for the largest cost T that is feasible
        lo, hi = 0, len(uniq) - 1
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            T = uniq[mid]
            if feasible(T):
                ans = T
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
```
- Notes about the solution approach:
  - We binary search on candidate minimum edge cost T (only need to check distinct edge costs).
  - For each T we check whether there's a path using only edges with cost ≥ T and only passing through online nodes whose total edge-cost sum ≤ k.
  - Because the graph is a DAG we compute shortest sums via a single pass over a topological order, resulting in O(n + m) per feasibility check.
- Complexity:
  - Time: O((n + m) + (n + m) * log M) where M is number of unique edge costs (M ≤ m). Typically O((n + m) log m).
  - Space: O(n + m) for adjacency and topo structures.
- Implementation details:
  - We prune relaxations from nodes whose dist > k because extending such a path cannot produce a path ≤ k (nonnegative costs).
  - We ensure intermediate nodes must be online by skipping relaxations from or to offline nodes (start and end are guaranteed online by constraints).