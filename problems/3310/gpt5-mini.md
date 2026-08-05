# [Problem 3310: Remove Methods From Project](https://leetcode.com/problems/remove-methods-from-project/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to find all methods that are "suspicious" — i.e., reachable from k following invocations (directed edges a -> b). Those form a set S. We can remove S only if no method outside S invokes any method inside S (no incoming edges from outside into S). So compute S by a DFS/BFS from k on the directed graph. Then check all edges: if any edge a->b has b in S but a not in S, removal is blocked and we must return the full list of methods (none removed). Otherwise return the nodes not in S. Complexity should be linear in nodes+edges.

## Refining the problem, round 2 thoughts
- Build adjacency list for outgoing edges and do an iterative stack/queue to mark all nodes reachable from k.
- Use a boolean array visited (size n) for S for O(1) membership checks.
- Then iterate through invocations list (edges) to check if any edge comes from outside into S; if found, abort and return all nodes.
- If not found, return [i for i in range(n) if not visited[i]].
- Edge cases:
  - invocations empty: S = {k}, no incoming edges -> removal allowed.
  - S = all nodes: no outside node exists -> allowed to remove all -> return [].
- Complexity: O(n + m) time and O(n + m) space.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def findAllUsedMethods(self, n: int, k: int, invocations: List[List[int]]) -> List[int]:
        # build adjacency list for outgoing edges
        adj = [[] for _ in range(n)]
        for a, b in invocations:
            adj[a].append(b)
        # BFS/DFS from k to find all suspicious methods reachable from k
        visited = [False] * n
        stack = [k]
        visited[k] = True
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        # If any edge comes from outside the suspicious set into the suspicious set,
        # we cannot remove the suspicious methods.
        for a, b in invocations:
            if visited[b] and not visited[a]:
                # blocked: some outside method invokes a suspicious method
                return list(range(n))
        # Otherwise we can remove all suspicious methods: return remaining methods
        return [i for i in range(n) if not visited[i]]

# For LeetCode, the required function name is removeMethodsFromProject:
class Solution:
    def removeMethodsFromProject(self, n: int, k: int, invocations: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(n)]
        for a, b in invocations:
            adj[a].append(b)
        visited = [False] * n
        stack = [k]
        visited[k] = True
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        for a, b in invocations:
            if visited[b] and not visited[a]:
                return list(range(n))
        return [i for i in range(n) if not visited[i]]
```
- Notes:
  - Approach: mark all nodes reachable from k (suspicious set S). If any edge from outside S goes into S, removal is blocked and we return all methods. Otherwise return the methods not in S.
  - Time complexity: O(n + m), where m = len(invocations). Building adjacency list and traversal are O(n + m), and checking edges is O(m).
  - Space complexity: O(n + m) for adjacency list and O(n) for visited array.