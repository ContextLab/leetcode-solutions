# [Problem 2872: Maximum Number of K-Divisible Components](https://leetcode.com/problems/maximum-number-of-k-divisible-components/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a tree and node values; we can remove some edges so that every resulting connected component has sum of node values divisible by k. The total sum is divisible by k (given), so at least the whole tree is valid (no cuts). Cutting an edge splits a subtree from the rest; the sum of that subtree must be divisible by k. That suggests we should look at subtree sums modulo k.

If we root the tree somewhere (say node 0), for any non-root node u, if the sum of the subtree rooted at u is divisible by k, then we may cut the edge between u and its parent and get an extra valid component. Cutting such an edge doesn't break the property for other disjoint subtrees. Intuitively we can cut every edge whose child-subtree sum % k == 0 independently. So count how many non-root nodes have subtree sum % k == 0; answer is that count + 1 (components = cuts + 1). DFS to compute subtree sum modulo k seems natural.

## Refining the problem, round 2 thoughts
- Implementation detail: sums can be large but we only need them modulo k, so propagate s = (s + child_sum) % k.
- When a subtree sum % k == 0 for node u (u != root), we can increment cut count and return 0 to parent (simulate cutting so parent doesn't include the subtree sum).
- Edge cases:
  - n == 1 -> no edges, answer should be 1.
  - k == 1 -> every value % 1 == 0, every subtree sum % 1 == 0 -> we can cut all n-1 edges -> answer = n.
- Complexity: one DFS over n nodes, O(n) time and O(n) space for adjacency + recursion stack. For Python recursion, increase recursion limit (n up to 3e4).
- Correctness: cutting every edge where the child-subtree sum is 0 (mod k) is never harmful — those subtrees are independent of the rest and produce valid components. Since total sum divisible by k, root ends up with 0 mod k but we don't attempt to cut above root.

## Attempted solution(s)
```python
import sys
from typing import List

class Solution:
    def maxKDivisibleComponents(self, n: int, edges: List[List[int]], values: List[int], k: int) -> int:
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        sys.setrecursionlimit(1000000)
        cuts = 0

        def dfs(u: int, parent: int) -> int:
            nonlocal cuts
            # subtree sum modulo k
            s = values[u] % k
            for v in adj[u]:
                if v == parent:
                    continue
                child_mod = dfs(v, u)
                s = (s + child_mod) % k
            # If this subtree (excluding parent) sums to 0 mod k and it's not the root,
            # we can cut the edge to parent and return 0 upwards.
            if parent != -1 and s == 0:
                cuts += 1
                return 0
            return s

        dfs(0, -1)
        # components = cuts + 1 (initial component + each cut increases count by 1)
        return cuts + 1

# Example usage:
# sol = Solution()
# print(sol.maxKDivisibleComponents(5, [[0,2],[1,2],[1,3],[2,4]], [1,8,1,4,4], 6))  # -> 2
```

- Notes about the solution:
  - Approach: Root the tree (node 0), DFS to compute subtree sums modulo k. Whenever a non-root subtree sums to 0 mod k, increment cut count and return 0 so parent doesn't include it.
  - Time complexity: O(n) — each node/edge visited once.
  - Space complexity: O(n) for adjacency list + O(n) recursion stack in worst case.
  - Implementation details: use modulo arithmetic to avoid large integers; increase recursion limit for deep trees.