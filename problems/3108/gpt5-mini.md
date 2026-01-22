# [Problem 3108: Minimum Cost Walk in Weighted Graph](https://leetcode.com/problems/minimum-cost-walk-in-weighted-graph/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- The walk can repeat edges and vertices arbitrarily. The cost of the walk is the bitwise AND of all edge weights used (repetitions don't change the AND).
- If I want to minimize the AND for a walk from s to t, I can include as many edges as I want as long as I can traverse them and still connect s and t by a walk. In particular, if s and t belong to some connected component (ignoring weights), I can traverse the whole component (visiting every edge at least once by repeated traversal) and thereby include every edge weight in the AND.
- AND of a larger set of numbers is less than or equal to the AND of any subset; therefore the AND of all edges in the connected component is the minimum possible AND achievable by any walk that stays inside that connected component and connects s to t.
- Conversely, any walk from s to t uses a subset of edges of the component, so its AND is >= AND(all edges in the component). Therefore the minimal achievable cost for s,t inside the same connected component is exactly the bitwise AND of all edges in that component.
- If s and t are in different connected components (ignoring weights), there is no walk and answer is -1.

So the solution reduces to: compute connected components of the undirected graph ignoring weights, compute for each component the bitwise AND of all edge weights that belong to that component, and answer queries by checking whether s and t share a component and, if so, returning that component's AND.

## Refining the problem, round 2 thoughts
- Implementation plan:
  - Use DSU (union-find) to union endpoints of every edge (ignore weights) to obtain components.
  - For each edge (u, v, w), find the root of u (after union phase) and accumulate comp_and[root] &= w. Initialize comp_and for a root to all-ones mask (enough bits to cover max weight). Since weights <= 1e5, 17 bits are enough (2^17 = 131072).
  - For queries: if find(s) != find(t), answer -1; otherwise answer comp_and[find(s)].
- Edge cases:
  - Isolated nodes (no edges): these nodes are their own component; since queries require s != t, such queries will only appear when s and t different and thus roots differ → answer -1. No extra handling needed.
  - If a component has no edges (shouldn't happen if it contains >=2 nodes because edges define unions), comp_and would remain all-ones. But that won't be used except maybe if there is a component with 2+ nodes but union happened via some edges: by construction comp with >=2 nodes has at least one edge and comp_and will be updated.
- Complexity:
  - Building DSU unions: O(m α(n)).
  - Accumulating AND per component: O(m α(n)) for finds.
  - Answering q queries with finds: O(q α(n)).
  - Memory O(n + m).

This is efficient for the constraints (n, m, q <= 1e5).

## Attempted solution(s)
```python
# Complete Python solution

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        else:
            self.parent[ry] = rx
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
        return True

class Solution:
    def minCostWalk(self, n, edges, query):
        """
        n: int
        edges: List[List[int]] where each is [u, v, w]
        query: List[List[int]] where each is [s, t]
        return: List[int]
        """
        # Step 1: build DSU by ignoring weights (connectivity)
        dsu = DSU(n)
        for u, v, _ in edges:
            dsu.union(u, v)

        # Step 2: compute bitwise AND of all edges per component root
        # weights <= 1e5, so 17 bits suffice (2^17 = 131072)
        ALL_ONES = (1 << 17) - 1
        comp_and = {}
        for u, v, w in edges:
            r = dsu.find(u)  # root for the component
            # initialize if needed
            if r not in comp_and:
                comp_and[r] = ALL_ONES
            comp_and[r] &= w

        # If a root exists but had no edges, comp_and won't have entry.
        # But such a root must be a singleton; queries always have s != t,
        # so they won't ask about two distinct nodes in the same singleton root.

        # Step 3: answer queries
        res = []
        for s, t in query:
            rs = dsu.find(s)
            rt = dsu.find(t)
            if rs != rt:
                res.append(-1)
            else:
                # If root exists in comp_and, use it; otherwise component has no edges,
                # but since s != t, this case shouldn't occur. For safety:
                res.append(comp_and.get(rs, -1))
        return res

# Example usage:
# sol = Solution()
# print(sol.minCostWalk(5, [[0,1,7],[1,3,7],[1,2,1]], [[0,3],[3,4]]))  # [1, -1]
# print(sol.minCostWalk(3, [[0,2,7],[0,1,15],[1,2,6],[1,2,1]], [[1,2]]))  # [0]
```

- Notes about the solution approach:
  - Correctness: For any connected component (ignoring weights), any walk between two nodes in the component can only use edges from that component. The bitwise AND over any subset of edges is always >= the AND over the entire set of edges in the component. Because you can construct a walk that traverses every edge in the component (repeating edges if needed), the minimum achievable AND for any pair of nodes in that component is exactly the AND of all edge weights in the component. If s and t are in different components, no walk exists and the answer is -1.
  - Time complexity: O((n + m + q) * α(n)) where m = len(edges), q = len(query), and α is inverse Ackermann (from DSU). Practically linear for given constraints.
  - Space complexity: O(n + m) for DSU arrays and storing edges (input) and comp_and map.

This solution is efficient and straightforward once the key observation (minimum equals AND of all edges in the connected component) is recognized.