# [Problem 802: Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I know a safe node is one from which every path eventually ends at a terminal node (no outgoing edges). That basically means the node is not part of any cycle and does not lead into any cycle. So the problem reduces to identifying nodes that are not in cycles (or that only reach nodes that are also safe).

First approaches that come to mind:
- Do a DFS with coloring (0=unvisited, 1=visiting, 2=safe/visited) to detect cycles: if during DFS you reach a "visiting" node, you found a cycle and that path is unsafe. Mark nodes that finish without hitting a cycle as safe.
- Alternatively, use a graph transformation: reverse edges and run a Kahn-style topological process starting from terminal nodes (outdegree 0). In the reversed graph, when you remove a terminal node you effectively reduce outdegree of its predecessors; those whose outdegree becomes 0 become safe too. That yields all safe nodes.

Both are common; the reverse graph + queue (BFS topological) is clean and linear time.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- Self-loops: a node with an edge to itself is in a cycle and should not be safe unless the loop can be otherwise bypassed (but a self-loop alone makes it unsafe).
- Graph nodes already sorted in graph[i] doesn't matter for correctness; final output must be sorted ascending. If we iterate nodes 0..n-1 for output, it's naturally sorted.
- Complexity requirement: need O(V + E) time and space which both DFS-coloring and reverse-graph + queue achieve.
- Implementation details: build reversed adjacency list rev where for each edge u->v we add u into rev[v]. Keep an array outdeg[u] = len(graph[u]). Initialize queue with nodes whose outdeg == 0 (terminal). Pop node, for each predecessor p in rev[node], decrement outdeg[p]. If outdeg[p] becomes 0, add to queue. After processing, nodes with outdeg==0 are exactly the safe nodes.

I'll implement the reverse-graph + Kahn approach. It's straightforward and avoids recursion depth issues.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        # outdegree for each node
        outdeg = [len(graph[i]) for i in range(n)]
        # reversed adjacency list: for each edge u->v, add u to rev[v]
        rev = [[] for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                rev[v].append(u)
        # queue initialized with terminal nodes (outdeg == 0)
        q = deque([i for i in range(n) if outdeg[i] == 0])
        # process nodes; nodes that eventually become outdeg 0 are safe
        while q:
            node = q.popleft()
            for pred in rev[node]:
                outdeg[pred] -= 1
                if outdeg[pred] == 0:
                    q.append(pred)
        # safe nodes are those with outdeg == 0; iterate in order for sorted result
        return [i for i in range(n) if outdeg[i] == 0]
```
- Notes about approach:
  - We use the reversed graph so that we can propagate "safeness" backwards from terminal nodes.
  - Time complexity: O(V + E) — building rev and processing each edge at most once.
  - Space complexity: O(V + E) — for the reversed adjacency list and auxiliary arrays/queue.
  - This approach avoids recursion and is robust for large graphs. An alternative is DFS with 3-color marking (detect cycles), which is also O(V+E) but uses recursion (or an explicit stack).