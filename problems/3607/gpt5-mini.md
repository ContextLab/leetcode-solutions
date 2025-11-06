# [Problem 3607: Power Grid Maintenance](https://leetcode.com/problems/power-grid-maintenance/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have c stations and static undirected connections which partition the stations into connected components (power grids). Initially every station is online. Queries are two kinds:
- [1, x]: ask which operational station will resolve the check for x. If x is online return x; otherwise return the smallest id online station in x's component (or -1 if none).
- [2, x]: mark x offline.

Observations:
- The connectivity (components) never changes — taking nodes offline doesn't change component membership.
- So we can compute components once (DSU / union-find).
- For each component we need to maintain the set of currently-online station ids with fast removal and fast retrieval of the minimum id.
- Operations are only deletions (mark offline) and queries for min element. A min-heap per component with lazy deletions (keep popping offline tops) looks simple and efficient. Alternatively a balanced BST (sorted set) per component would work but Python doesn't have one built-in.

So plan: build DSU, create a heap (min-heap) of members for each component, maintain an online boolean array. For a type-1 query: if x is online return x; otherwise find its component, lazily pop from that component's heap until top is online (or empty). Return top or -1. For a type-2 query: mark x offline (idempotent).

## Refining the problem, round 2 thoughts
Edge cases and details:
- There may be repeated [2, x] operations; marking offline twice should be safe (we'll check online flag before setting, but setting to False again is harmless).
- Heaps initially contain every member; lazy popping ensures each node is popped at most once across all queries, so overall pop complexity is O(c log c).
- Queries involve DSU finds; with path compression and union by rank, find is effectively almost O(1) amortized (inverse-Ackermann).
- Space: heaps total hold c items initially; online boolean array size c+1.

Complexity:
- Building DSU from connections: O(n * α(c)).
- Building heaps: O(c) pushes, total O(c log c) to heapify incrementally.
- Each query: find + potentially popping. Each item popped at most once so overall pop cost O(c log c); each query also does a constant number of heap/lookups. So total time O((c + n + q) log c) worst-case dominated by heap operations (more precisely O((c + number_of_pops) log c) and pops ≤ c).
- Space O(c + n) for DSU and heaps.

This approach is simple and should pass bounds (c ≤ 1e5, queries ≤ 2e5).

## Attempted solution(s)
```python
import heapq
from typing import List

class DSU:
    def __init__(self, n):
        self.parent = list(range(n+1))
        self.rank = [0]*(n+1)
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[rb] < self.rank[ra]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1

class Solution:
    def powerGridMaintenance(self, c: int, connections: List[List[int]], queries: List[List[int]]) -> List[int]:
        dsu = DSU(c)
        for u, v in connections:
            dsu.union(u, v)
        # Build a heap for each component representative
        heaps = [None] * (c + 1)  # heaps[rep] is a min-heap of node ids for that component
        for node in range(1, c+1):
            rep = dsu.find(node)
            if heaps[rep] is None:
                heaps[rep] = []
            heapq.heappush(heaps[rep], node)
        online = [True] * (c + 1)  # online[0] unused

        ans = []
        for typ, x in queries:
            if typ == 1:
                if online[x]:
                    ans.append(x)
                else:
                    rep = dsu.find(x)
                    heap = heaps[rep]
                    # If there is no heap (shouldn't happen since every node was added), handle gracefully
                    if heap is None:
                        ans.append(-1)
                        continue
                    # lazy remove offline nodes
                    while heap and not online[heap[0]]:
                        heapq.heappop(heap)
                    if heap:
                        ans.append(heap[0])
                    else:
                        ans.append(-1)
            else:  # typ == 2
                # mark offline (idempotent)
                if online[x]:
                    online[x] = False
        return ans

# The LeetCode entry point expects the method name; adapt if needed.
# Example usage:
# sol = Solution()
# print(sol.powerGridMaintenance(5, [[1,2],[2,3],[3,4],[4,5]], [[1,3],[2,1],[1,1],[2,2],[1,2]]))
```

- Notes about the solution approach:
  - Use DSU (union-find) to compute connected components once.
  - Maintain a min-heap per component containing all node ids initially. Because nodes are only ever removed (marked offline), lazy deletion on the heap (pop until the top is online) is efficient: each id is popped at most once overall.
  - For a [1, x] query, if x is online return x. Otherwise find component representative and retrieve the heap's current minimum after lazy cleanup; return -1 if heap becomes empty.
  - For a [2, x] query, mark x offline. No immediate heap modification is necessary.
- Complexity:
  - Time: Building DSU O(n α(c)). Building heaps O(c log c) (pushes). Each node popped at most once across all queries -> total pop cost O(c log c). Each query performs O(α(c)) find plus occasional heap pops. So overall roughly O((c + n + q) log c) worst-case.
  - Space: O(c + n) for DSU structures and heaps (heaps store each node once).