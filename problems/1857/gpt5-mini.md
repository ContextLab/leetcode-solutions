# [Problem 1857: Largest Color Value in a Directed Graph](https://leetcode.com/problems/largest-color-value-in-a-directed-graph/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum frequency of any color along any directed path. Graph may contain cycles — in that case we return -1. This sounds like a topological-order DP problem: if the graph is a DAG we can process nodes in topological order and maintain, for each node, the best counts for each of the 26 colors for paths ending at that node. When propagating from a node u to neighbor v, we can update v's color-count array using u's array. If there's a cycle Kahn's algorithm will detect it because not all nodes will be processed. The alphabet size (26) is small, so storing a 26-sized array per node is feasible (26 * 1e5 ~ 2.6e6 integers). Complexity should be O((n + m) * 26) which is acceptable.

## Refining the problem, round 2 thoughts
Implementation details:
- Build adjacency list and indegree array.
- dp[node] is a list of 26 ints: dp[node][c] = maximum count of color c along any path that ends at node (but not yet including the node's own color increment).
- We will use Kahn's algorithm: push indegree-0 nodes into queue. When we pop u, increment dp[u][color_u] by 1 (account for u itself), update global answer with max(dp[u]). Then for each neighbor v, merge dp[u] into dp[v] by max per color; decrement indegree[v], and enqueue when indegree becomes 0.
- After processing, if processed nodes < n then a cycle exists -> return -1.
Edge cases: self-loop, isolated nodes, large graphs. Memory/time constraints are satisfied.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        n = len(colors)
        # Build adjacency list and indegree
        adj = [[] for _ in range(n)]
        indeg = [0] * n
        for u, v in edges:
            adj[u].append(v)
            indeg[v] += 1

        # dp[node][c] = max count of color c along any path ending at node (before counting node itself)
        dp = [[0] * 26 for _ in range(n)]

        q = deque()
        # enqueue zero indegree nodes
        for i in range(n):
            if indeg[i] == 0:
                q.append(i)

        processed = 0
        ans = 0
        while q:
            u = q.popleft()
            processed += 1
            cu = ord(colors[u]) - ord('a')
            # count the node's own color
            dp[u][cu] += 1
            # update global answer with best at u
            local_max = max(dp[u])
            if local_max > ans:
                ans = local_max

            # propagate dp[u] to neighbors
            for v in adj[u]:
                # merge dp arrays: for each color keep the maximum
                # small optimization: inline loop over 26
                for c in range(26):
                    if dp[u][c] > dp[v][c]:
                        dp[v][c] = dp[u][c]
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        # if not all nodes processed, there is a cycle
        if processed < n:
            return -1
        return ans
```
- Notes:
  - Approach: Kahn's topological sort + dynamic programming per node over 26 colors.
  - Time complexity: O((n + m) * 26) = O(n + m) with a constant factor 26. For n, m up to 1e5 this is fine.
  - Space complexity: O(n * 26 + m) for dp arrays and adjacency list, i.e., O(n + m) with a 26x factor for dp.
  - Important detail: we increment the node's own color count at the time we pop it from the queue — after all predecessors have propagated their dp values to it — ensuring correctness. Detect cycles by comparing number of processed nodes to n.