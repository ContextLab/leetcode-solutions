# [Problem 2127: Maximum Employees to Be Invited to a Meeting](https://leetcode.com/problems/maximum-employees-to-be-invited-to-a-meeting/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a directed graph where each node i has exactly one outgoing edge to favorite[i]. For a circular table, each invited person must have their favorite adjacent to them. Typical patterns: directed cycles are natural candidates because in a cycle everyone can be seated next to their favorite. But there is also the special case of 2-cycles (mutual favorites i<->j) that can be extended by chains (trees) that lead into i or j, because those chains can end at i or j and be arranged with i and j adjacent.

So approach: find all directed cycles. For cycles of length >= 3, you can invite the entire cycle (contribution = cycle length). For 2-cycles (mutual pairs), you can invite the pair plus the longest chain coming into each node (not using nodes in cycles). So we need to compute longest chain length ending at each node (from nodes that are not in cycles). To compute that, remove nodes with indegree 0 in topological fashion; while doing that compute distances (longest path) to their successor. After removal, remaining nodes are in cycles. Then:
- compute max cycle length among cycles (>=3).
- for each mutual pair i<->j, sum 2 + chain_len[i] + chain_len[j].
Answer = max(max_cycle_length, sum_over_all_mutual_pairs).

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Use indegree-based topological removal to strip acyclic parts and compute depth (longest chain into each node).
- After removal nodes with indegree>0 are exactly nodes in cycles.
- For cycles length >=3, take the maximum cycle size.
- For mutual pairs (i < favorite[i] and favorite[favorite[i]] == i), add 2 + depth[i] + depth[favorite[i]] to a running total (sum of all such pair-extensions).
- Final answer is max(max_cycle_length, sum_pairs_extensions).

Complexity:
- Build indegrees and reverse adjacency: O(n).
- Topological BFS removing nodes: O(n).
- Cycle traversal to count sizes: O(n).
Total time O(n). Space O(n).

Now the implementation.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def maximumInvitations(self, favorite: List[int]) -> int:
        n = len(favorite)
        indeg = [0] * n
        for v in favorite:
            indeg[v] += 1

        # depth[u] will store the longest chain length ending at u coming from nodes removed (acyclic part)
        depth = [0] * n
        q = deque([i for i in range(n) if indeg[i] == 0])

        # Topological removal: compute longest path (chain) lengths into nodes
        while q:
            u = q.popleft()
            v = favorite[u]
            depth[v] = max(depth[v], depth[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

        # Remaining nodes with indeg > 0 are in cycles
        visited = [False] * n
        max_cycle = 0
        for i in range(n):
            if indeg[i] > 0 and not visited[i]:
                # traverse this cycle to count its length
                length = 0
                u = i
                while not visited[u]:
                    visited[u] = True
                    length += 1
                    u = favorite[u]
                max_cycle = max(max_cycle, length)

        # Handle mutual pairs and sum their best extensions
        pair_sum = 0
        for i in range(n):
            j = favorite[i]
            # mutual pair i <-> j and count only once (i < j)
            if favorite[j] == i and i < j:
                pair_sum += 2 + depth[i] + depth[j]

        return max(max_cycle, pair_sum)
```
- Notes:
  - We remove acyclic nodes with indegree 0 and propagate depth to the successor, storing the length of the longest chain ending at each node.
  - After removal, nodes left with positive indegree form cycles. We find the largest cycle length (for cycles length >= 3 this is a candidate).
  - For 2-cycles (mutual pairs), we take pair contribution = 2 + depth[left] + depth[right] and sum across all disjoint mutual pairs.
  - The answer is the maximum between the largest cycle and the sum of all extended mutual pairs.
- Time complexity: O(n). Space complexity: O(n).