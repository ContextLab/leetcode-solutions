# [Problem 2493: Divide Nodes Into the Maximum Number of Groups](https://leetcode.com/problems/divide-nodes-into-the-maximum-number-of-groups/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to assign integer group indices (1..m) to nodes so that every edge connects nodes whose group indices differ by exactly 1. That forces every edge to connect nodes of opposite parity (odd/even indices), so any connected component must be bipartite — otherwise impossible. Within a bipartite connected component, all nodes of one color can share the same group index and the other color must be the next index (consecutive). Different connected components can interact by edges; those inter-component edges create ordering constraints between the "parity blocks" (color partitions) of components.

So approach: check bipartiteness per connected component and assign component ids and node colors. Then build a directed graph on parity-blocks (i.e., for each component and each color that actually exists create a meta-node). Add an internal edge from component_color0 -> component_color1 if both colors exist (ensuring the color1 block is one greater than color0). For every original edge that connects different components, add a directed edge from the source parity-block to the target parity-block following the node colors (u.color -> v.color). The constraints are "increase by 1" so we model edges as unit-weight directed edges. If this meta-graph has a positive cycle, grouping is impossible; otherwise the maximum number of groups equals the length of the longest path (in terms of nodes) in this DAG, which we can get by topological DP.

## Refining the problem, round 2 thoughts
- Need to be careful: components may have only one parity (e.g., a single isolated node). We should create meta-nodes only for parity classes that actually contain nodes, otherwise we'd artificially allow an extra group.
- When adding the internal edge for a component, only add it if both parities are present.
- After building the meta-graph (nodes <= 2 * number_of_components), run Kahn's topological sort and compute dp[v] = max(dp[v], dp[u] + 1) for u->v. Initialize dp[*] = 1 meaning the smallest possible group index represented is 1.
- If the topological sort doesn't process all meta-nodes (cycle), return -1.
- Complexity: building bipartite colors O(n + E), building meta-graph O(E), topological DP O(V_meta + E_meta). With n <= 500 and E <= 1e4, fine.

Edge cases:
- Non-bipartite component -> return -1.
- A component with only one parity (isolated node(s) all in same parity) should not produce two meta-nodes.
- Multiple edges between the same meta-nodes are fine (we may add duplicates; can dedupe or tolerate them since it doesn't break Kahn/DP, but we can keep as-is).

## Attempted solution(s)
```python
from collections import deque, defaultdict

class Solution:
    def magnificentSets(self, n: int, edges: list[list[int]]) -> int:
        # Build adjacency
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        color = [-1] * (n + 1)   # 0/1 bipartite color
        comp = [-1] * (n + 1)    # component id
        comp_count = 0
        # For each component, track whether parity 0 or 1 exists
        comp_has = []  # list of [has0, has1]

        # BFS to check bipartiteness and assign component ids
        for i in range(1, n + 1):
            if comp[i] != -1:
                continue
            # start new component
            q = deque([i])
            comp[i] = comp_count
            color[i] = 0
            has0 = 1
            has1 = 0
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if comp[v] == -1:
                        comp[v] = comp_count
                        color[v] = color[u] ^ 1
                        if color[v] == 0:
                            has0 = 1
                        else:
                            has1 = 1
                        q.append(v)
                    else:
                        # Check bipartite coloring
                        if color[v] == color[u]:
                            return -1
            comp_has.append((has0, has1))
            comp_count += 1

        # Map (component, parity) that actually exists to node index in meta-graph
        idx_map = {}
        idx = 0
        for c in range(comp_count):
            if comp_has[c][0]:
                idx_map[(c, 0)] = idx
                idx += 1
            if comp_has[c][1]:
                idx_map[(c, 1)] = idx
                idx += 1

        m = idx  # number of meta-nodes
        madj = [[] for _ in range(m)]
        indeg = [0] * m

        # Add internal edges: for components that have both parities, parity0 -> parity1
        for c in range(comp_count):
            if comp_has[c][0] and comp_has[c][1]:
                u = idx_map[(c, 0)]
                v = idx_map[(c, 1)]
                madj[u].append(v)
                indeg[v] += 1

        # For original edges connecting different components, add edge from (comp[u], color[u]) -> (comp[v], color[v])
        for u, v in edges:
            cu, cv = comp[u], comp[v]
            if cu == cv:
                continue
            su = (cu, color[u])
            sv = (cv, color[v])
            ui = idx_map[su]
            vi = idx_map[sv]
            madj[ui].append(vi)
            indeg[vi] += 1

        # Topological DP (Kahn). dp[node] = longest path length ending at node (count of nodes)
        dp = [1] * m
        q = deque([i for i in range(m) if indeg[i] == 0])
        processed = 0
        while q:
            x = q.popleft()
            processed += 1
            for y in madj[x]:
                if dp[y] < dp[x] + 1:
                    dp[y] = dp[x] + 1
                indeg[y] -= 1
                if indeg[y] == 0:
                    q.append(y)

        if processed != m:
            return -1

        return max(dp) if m > 0 else 0

# Example usage:
# sol = Solution()
# print(sol.magnificentSets(6, [[1,2],[1,4],[1,5],[2,6],[2,3],[4,6]]))  # expected 4
```

- Notes about the approach:
  - First BFS per connected component checks bipartiteness and records which parity classes exist for the component.
  - We create a meta-node for every existent (component, parity) pair; if a component has nodes only in one parity, we create only one meta-node for it (prevents artificially increasing groups).
  - We add an internal directed edge from the parity-0 meta-node to parity-1 meta-node for components that have both parities, representing that parity-1's group index must be parity-0's index + 1.
  - For each original cross-component edge u-v, add a directed edge from (comp[u], color[u]) to (comp[v], color[v]) with unit increment.
  - Then compute the longest path in the directed meta-graph via topological order; dp[v] = max(dp[v], dp[u] + 1).
  - If there's a cycle in the meta-graph (i.e., we couldn't topologically process all nodes), grouping is impossible -> return -1.
- Complexity:
  - Time: O(n + E) for BFS coloring + O(E) for building meta-graph + O(V_meta + E_meta) for topological DP. Since V_meta <= 2 * number_of_components <= 2n and E_meta <= E + components, overall O(n + E).
  - Space: O(n + E + V_meta + E_meta) = O(n + E).