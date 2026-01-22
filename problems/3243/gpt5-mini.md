# [Problem 3243: Shortest Distance After Road Addition Queries I](https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a directed graph on nodes 0..n-1 where initially we have edges i -> i+1 for all i. Each added road is also u -> v with u < v, so every edge goes forward. That means the graph is a DAG and the natural topological order is just 0,1,2,...,n-1.

We need the shortest path length (in number of edges) from 0 to n-1 after each incremental insertion. Because edges are unweighted (each road counts 1), in a DAG we can compute shortest distances by a single pass in topological order: relax outgoing edges from each node. Since the topological order is the node index order, it's especially simple.

n and number of queries are ≤ 500, so recomputing distances after each inserted edge with an O(n + m) DP pass is fine (worst-case ~500 * (1000) operations).

## Refining the problem, round 2 thoughts
- Maintain adjacency lists. Initialize with the chain edges i->i+1.
- For each query, add the new directed edge to adjacency, then compute distances from 0 to all nodes by a single pass i=0..n-1:
  - dist[0] = 0, others = inf
  - for i in 0..n-1, if dist[i] is finite, for every neighbor v in adj[i]: dist[v] = min(dist[v], dist[i] + 1)
- Record dist[n-1] after each query.
- Edge cases: graph is always connected from 0 to n-1 via the initial chain, so dist[n-1] always finite.
- Complexity: For q queries, overall time is sum over queries of O(n + m_i), where m_i is number of edges after i queries. With m_i ≤ n-1 + i, total is O(q*n + q^2) worst-case but with q,n ≤ 500 that's fine. Space O(n + m).

Alternative approaches (more incremental updates) are possible but unnecessary given constraints.

## Attempted solution(s)
```python
from typing import List
import math

class Solution:
    def shortestPath(self, n: int, queries: List[List[int]]) -> List[int]:
        # adjacency list for forward-only edges
        adj = [[] for _ in range(n)]
        # initial chain edges i -> i+1
        for i in range(n - 1):
            adj[i].append(i + 1)
        
        res = []
        for u, v in queries:
            # add the new road
            adj[u].append(v)
            
            # compute shortest distances from 0 using topological order 0..n-1
            INF = 10**9
            dist = [INF] * n
            dist[0] = 0
            for i in range(n):
                if dist[i] == INF:
                    continue
                for w in adj[i]:
                    if dist[w] > dist[i] + 1:
                        dist[w] = dist[i] + 1
            res.append(dist[n-1])
        return res
```
- Notes:
  - We exploit that all edges go from a smaller index to a larger one, so node indices themselves form a valid topological order.
  - After each edge insertion we run a single DP relaxation pass in that order, which gives correct shortest path lengths (all edges weight 1).
  - Time complexity: For q queries and n nodes, each pass is O(n + m_current). With constraints n, q ≤ 500 this is efficient. Overall worst-case time is O(q*(n+q)) but practical and within limits for given bounds.
  - Space complexity: O(n + m) to store adjacency, plus O(n) for distances.