# [Problem 2467: Most Profitable Path in a Tree](https://leetcode.com/problems/most-profitable-path-in-a-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum net income Alice can get when she travels from root (0) toward some leaf, while Bob moves from his start toward the root. The key interaction is that if Bob reaches a node before Alice, the gate is already opened and Alice gets nothing from that node; if they arrive simultaneously they split the value; otherwise Alice gets full value.

So for any node we only need to know the time (number of steps from start) when Alice would reach it (which is simply the depth along the chosen path) and the time when Bob reaches it (if ever; otherwise infinity). That suggests:
- Precompute Bob's arrival time to every node (infinite for nodes not on Bob->0 path).
- Do a DFS from root to every leaf tracking Alice's time (depth) and cumulative profit, computing contribution at each node based on comparison with Bob's time.
- Keep the maximum profit seen at leaves.

We must be careful about leaf detection (in rooted tree a leaf is a node with no children; equivalently node != 0 and degree==1). Also handle shared arrival (half the amount). Because n up to 1e5, use iterative parent building or increase recursion limit.

## Refining the problem, round 2 thoughts
Implementation details:
- Build adjacency list.
- Build parent array (rooted at 0) via iterative stack/BFS to avoid recursion depth issues while constructing parents.
- Walk from bob up to root using parent pointers to set bobTime[node] = distance from bob (0 at bob).
- DFS from root accumulating profit. For each visited node at Alice time t:
  - if bobTime[node] < t: contribution = 0
  - elif bobTime[node] == t: contribution = amount[node] // 2
  - else: contribution = amount[node]
- When a leaf (in the rooted sense) is reached, update global maximum profit.
Edge cases:
- The root being a leaf if the tree has size 1 — constraints n >= 2 so not necessary but handle generality.
- Ensure integer division is safe because amounts are even.
Complexities:
- Time O(n) to build graph, compute parents, mark bob times, and DFS.
- Space O(n) for adjacency, parent, bobTime.

## Attempted solution(s)
```python
import sys
from typing import List

sys.setrecursionlimit(1 << 25)

class Solution:
    def mostProfitablePath(self, edges: List[List[int]], bob: int, amount: List[int]) -> int:
        n = len(amount)
        # build adjacency
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # build parent array rooted at 0 (iterative)
        parent = [None] * n
        parent[0] = -1
        stack = [0]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if parent[v] is None:
                    parent[v] = u
                    stack.append(v)

        # compute bob arrival times: bobTime[node] = time when Bob reaches node (0 at bob), inf if never
        INF = 10**18
        bobTime = [INF] * n
        t = 0
        node = bob
        while node != -1:
            bobTime[node] = t
            t += 1
            node = parent[node]

        # DFS from root tracking Alice's time (depth) and current sum
        self.ans = -10**30

        def dfs(u: int, p: int, depth: int, cur_sum: int) -> None:
            # compute contribution at node u based on bobTime
            if bobTime[u] < depth:
                contrib = 0
            elif bobTime[u] == depth:
                contrib = amount[u] // 2
            else:
                contrib = amount[u]
            cur_sum += contrib

            # detect leaf in rooted tree: node != 0 and degree == 1
            is_leaf = (u != 0 and len(adj[u]) == 1)
            if is_leaf:
                if cur_sum > self.ans:
                    self.ans = cur_sum
                return

            # continue to children
            for v in adj[u]:
                if v == p:
                    continue
                dfs(v, u, depth + 1, cur_sum)

        dfs(0, -1, 0, 0)
        return self.ans
```
- Approach: Build parent pointers to record Bob's arrival times along his path to root. Then DFS from root, at each node compute contribution according to Bob's arrival vs Alice's current depth, accumulate and propagate to children; update max at leaves.
- Time complexity: O(n) — building adjacency O(n), parent traversal O(n), Bob path O(depth) ≤ O(n), final DFS O(n).
- Space complexity: O(n) for adjacency, parent, bobTime, recursion stack (depth up to n in worst-case chain). If recursion depth is a concern, the DFS can be converted to an explicit stack.