# [Problem 2924: Find Champion II](https://leetcode.com/problems/find-champion-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see a directed acyclic graph (DAG) where an edge u -> v means u is stronger than v. The champion is a team that has no team stronger than it, i.e., no incoming edges. Because the input is generated transitive (if a > b and b > c then a > c) and no cycles, the relation is a partial order and edges include transitive information. So the simplest approach that comes to mind is to count indegrees: any node with indegree > 0 has at least one stronger team; nodes with indegree == 0 are candidates. If exactly one candidate exists, that's the unique champion; otherwise return -1. This should be O(n + m).

## Refining the problem, round 2 thoughts
Edge cases:
- No edges: all nodes indegree 0 => if n == 1 return 0 else -1.
- Exactly one node with indegree 0: return it.
- Multiple nodes with indegree 0: return -1.

Alternative approaches:
- Topological sort or finding a node that reaches all others would be overkill given the transitive property.
- Building adjacency or computing reachability is unnecessary because indegree alone suffices.

Complexity:
- Time: O(n + m) to count indegrees.
- Space: O(n) for the indegree array.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findChampion(self, n: int, edges: List[List[int]]) -> int:
        # indegree[i] counts how many teams are stronger than team i
        indegree = [0] * n
        for u, v in edges:
            indegree[v] += 1
        
        champ = -1
        count_zero = 0
        for i in range(n):
            if indegree[i] == 0:
                champ = i
                count_zero += 1
                if count_zero > 1:
                    return -1
        return champ if count_zero == 1 else -1
```
- Notes:
  - Approach: compute indegree for each node. A champion must have indegree 0 and must be unique.
  - Time complexity: O(n + m), where m = len(edges).
  - Space complexity: O(n) for the indegree array.
  - Implementation detail: early return -1 if more than one indegree-0 node is found to avoid extra work.