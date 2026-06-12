# [Problem 3559: Number of Ways to Assign Edge Weights II](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The query asks, for the path between two nodes u and v in a tree, how many assignments of weights 1 or 2 to edges on that path yield an odd total cost. Only edges on the path matter (ignore the rest). Observing parity: weight 1 is odd (parity 1), weight 2 is even (parity 0). So for a path with k edges, we need the number of binary strings of length k with odd number of 1s. That's exactly half of all strings when k >= 1, i.e. 2^{k-1}. For k = 0 (same node), there are 0 ways because sum is 0 (even). So the problem reduces to computing the number of edges on the path (distance) between u and v for each query, and returning 0 if distance = 0, else 2^{distance-1} modulo 1e9+7.

So main work: fast distance (edge count) between two nodes in a tree for up to 1e5 queries. Use depths + LCA (binary lifting) to get distance = depth[u] + depth[v] - 2*depth[lca(u,v)].

## Refining the problem, round 2 thoughts
- Precompute depth and binary lifting parents with a single BFS/DFS from root 1.
- Use bit_length of n to set number of levels (LOG).
- Precompute powers of two up to n (since max distance <= n-1) modulo MOD for O(1) query answers.
- For each query, compute LCA in O(LOG) and distance in O(1), then answer is pow2[distance-1] if distance > 0 else 0.
- Time complexity: O((n + q) * LOG) for building parents and answering queries. Space complexity: O(n * LOG) for parent table and O(n) for adjacency.
- Edge cases: u == v => distance 0 => answer 0. Tree is 1-indexed in input.

## Attempted solution(s)
```python
from collections import deque
import sys

MOD = 10**9 + 7

def number_of_ways(n, edges, queries):
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Prepare binary lifting
    LOG = (n).bit_length()  # enough levels so that 2^(LOG-1) >= n
    parent = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)

    # BFS from root 1 to set depth and parent[0]
    root = 1
    q = deque([root])
    depth[root] = 0
    parent[0][root] = 0  # 0 denotes no parent
    visited = [False] * (n + 1)
    visited[root] = True
    while q:
        node = q.popleft()
        for nei in adj[node]:
            if not visited[nei]:
                visited[nei] = True
                depth[nei] = depth[node] + 1
                parent[0][nei] = node
                q.append(nei)

    # Build parent[k][v]
    for k in range(1, LOG):
        pk = parent[k-1]
        pk1 = parent[k]
        for v in range(1, n + 1):
            mid = pk[v]
            pk1[v] = parent[k-1][mid] if mid != 0 else 0

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        # lift u up to depth v
        diff = depth[u] - depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = parent[bit][u]
            diff >>= 1
            bit += 1
        if u == v:
            return u
        # lift both up
        for k in range(LOG - 1, -1, -1):
            if parent[k][u] != parent[k][v]:
                u = parent[k][u]
                v = parent[k][v]
        return parent[0][u]

    # Precompute powers of two up to n
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD

    ans = []
    for u, v in queries:
        w = lca(u, v)
        dist = depth[u] + depth[v] - 2 * depth[w]
        if dist == 0:
            ans.append(0)
        else:
            # number of assignments with odd sum = 2^(dist-1)
            ans.append(pow2[dist-1])
    return ans

# Example usage for LeetCode style input:
# edges = [[1,2],[1,3],[3,4],[3,5]]
# queries = [[1,4],[3,4],[2,5]]
# print(number_of_ways(5, edges, queries))  # [2,1,4]
```

- Notes about the approach:
  - Observing parity simplifies the counting: parity only depends on whether each edge contributes 1 (odd) or 0 (even). For path length d, number of binary vectors with odd sum = 2^{d-1} for d >= 1.
  - We use BFS to avoid recursion depth issues; BFS populates depths and immediate parents.
  - Binary lifting gives O(LOG n) LCA per query.
  - Precomputing pow2 makes each query O(LOG n) time for LCA and O(1) for final answer.
- Complexity:
  - Time: O(n * LOG + q * LOG), where LOG = O(log n). Building parent table iterates LOG * n; answering q queries each does O(LOG) lifting.
  - Space: O(n * LOG) for parent table + O(n) for adjacency and depth arrays.