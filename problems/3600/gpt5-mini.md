# [Problem 3600: Maximize Spanning Tree Stability with Upgrades](https://leetcode.com/problems/maximize-spanning-tree-stability-with-upgrades/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum possible minimum edge strength (stability) in a spanning tree, where some edges are mandatory and cannot be upgraded, and up to k optional edges can be upgraded (doubling their strength). This screams binary search on the target minimum strength T: for a candidate T, check whether a valid spanning tree exists whose every used edge has strength >= T, with at most k upgrades used.

How to check feasibility for a given T? 
- A must-edge with s < T cannot be fixed (cannot be upgraded) so T is impossible.
- Must-edges that form a cycle make any spanning tree impossible (they must all be included).
- Optional edges are of three types for T:
  - free usable: s >= T (no upgrade needed)
  - upgradable usable: s < T but 2*s >= T (usable only if we spend one upgrade)
  - unusable: 2*s < T
We should try to connect the graph starting from must-edges, then use all free optional edges to reduce components, and finally see if we can bridge remaining components using upgradable edges. Each bridging using an upgradable edge consumes one upgrade and reduces the number of components by one. If we can reduce to one component with <= k such merges, T is feasible.

Binary search T over [1, 2*max_s]. First verify connectivity possibility at minimal T (1) — if impossible, answer is -1.

This approach is efficient: each feasibility check is union-find passes over edges, and binary search adds log factor.

## Refining the problem, round 2 thoughts
Edge cases / details:
- Must-edges forming a cycle => impossible for any T (immediately return -1).
- Must-edges with s < T => T infeasible.
- We should carefully avoid counting an upgradable edge that links nodes inside the same current component; only merges that reduce component count should count towards upgrades.
- When checking feasibility for T we only need to perform unions; union order for upgradable edges doesn't matter because each successful union reduces component count by exactly 1 and yields the minimal number of upgrades used to connect components using those edges.
- Binary search bounds: min answer is at least 1 if possible, maximum possible strength is 2 * max(original s). Use standard integer binary search (upper mid rounding up to avoid infinite loop).
- Complexity: m edges, n nodes. Each check is O(m α(n)). Binary search over up to ~18 bits (since s <= 1e5), so overall O(m log S α(n)).

I'll now implement a DSU and the described binary search + feasibility check.

## Attempted solution(s)
```python
from typing import List

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0]*n
        self.count = n  # number of components

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # union by rank
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[ry] < self.rank[rx]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        self.count -= 1
        return True

class Solution:
    def maxSTStability(self, n: int, edges: List[List[int]], k: int) -> int:
        # Pre-split edges to speed up checks
        must_edges = []
        optional_edges = []
        max_s = 0
        for u, v, s, must in edges:
            max_s = max(max_s, s)
            if must == 1:
                must_edges.append((u, v, s))
            else:
                optional_edges.append((u, v, s))

        # Feasibility check for a given target strength T
        def feasible(T: int) -> bool:
            dsu = DSU(n)
            # 1) Include must edges: they must be present and cannot be upgraded
            for u, v, s in must_edges:
                if s < T:
                    return False  # cannot satisfy this must edge
                # if union fails, a cycle among must edges -> impossible
                if not dsu.union(u, v):
                    return False

            # 2) Use optional edges that already meet T (no upgrade)
            for u, v, s in optional_edges:
                if s >= T:
                    dsu.union(u, v)

            if dsu.count == 1:
                return True  # already connected without upgrades

            # 3) Use upgradable optional edges (s < T <= 2*s) to connect components.
            # Each union using such an edge consumes one upgrade.
            upgrades_used = 0
            # We only need to perform (components - 1) successful unions
            needed = dsu.count - 1
            # Iterate through upgradable edges and try to merge components
            for u, v, s in optional_edges:
                if s < T and 2*s >= T:
                    if dsu.union(u, v):
                        upgrades_used += 1
                        needed -= 1
                        if needed == 0:
                            break
            if needed == 0 and upgrades_used <= k:
                return True
            return False

        # Quick impossibility check: if even T=1 is not feasible, return -1
        if not feasible(1):
            return -1

        lo, hi = 1, 2 * max_s
        # Binary search maximum feasible T
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo

# Hook for LeetCode style invocation
def maxStability(n: int, edges: List[List[int]], k: int) -> int:
    return Solution().maxSTStability(n, edges, k)
```

- Notes about the approach:
  - We binary search the candidate minimum strength T.
  - For each T we use DSU to (a) ensure must edges are feasible and don't form cycles, (b) union all optional edges with s >= T, (c) attempt to connect remaining components using upgradable edges (s < T <= 2*s), counting upgrades used. If we can connect all components and used_upgrades <= k, T is feasible.
  - Correctness: We greedily use all free edges first (no upgrade cost). Then every successful union using an upgradable edge reduces the component count by 1; using any such edge inside a component is useless, so counting only successful unions yields the minimal number of upgrades needed to connect the current components with those edges.
- Complexity:
  - Let m = len(edges), n nodes.
  - Each feasibility check is O(m α(n)) (a few passes over edges, union-find operations).
  - Binary search over strengths up to 2*max_s (max_s <= 1e5) costs O(log max_s) ~ <= 18 iterations.
  - Total time: O(m log S * α(n)), space O(n + m) for storing edges and DSU.
- Important implementation details:
  - We must detect cycles among must edges early and treat it as impossible for any T.
  - We check feasibility at T=1 to determine if any spanning tree at all can be formed; if not, return -1 early.
  - The solution uses integer binary search with upper mid (lo+hi+1)//2 to avoid infinite loop and to find maximum feasible T.