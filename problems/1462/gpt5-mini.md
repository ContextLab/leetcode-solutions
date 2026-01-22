# [Problem 1462: Course Schedule IV](https://leetcode.com/problems/course-schedule-iv/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to answer multiple reachability queries on a directed acyclic graph (courses -> prerequisites). The queries ask whether u is a (direct or indirect) prerequisite of v, i.e., whether there's a path from u to v. numCourses is at most 100, which is small. That suggests I can precompute transitive closure of the graph and then answer each query in O(1). Floyd–Warshall (O(n^3)) or repeated BFS/DFS from each node (O(n*(n+m))) are both viable. Because n ≤ 100, Floyd–Warshall is easy, simple to implement, and fast enough. Alternatively, I could run BFS from each node to build a reachable set; that would also be straightforward.

## Refining the problem, round 2 thoughts
Edge cases: no prerequisites -> all answers false. Graph is guaranteed acyclic, but algorithm doesn't need that assumption aside from nicer semantics. Prerequisites list can be up to ~n*(n-1)/2 but still fine. For correctness and simplicity I will build an n x n boolean matrix reachable, set reachable[a][b] = True for every direct edge, and run Floyd–Warshall-like propagation: if i -> k and k -> j then i -> j. After transitive closure, each query is just lookup.

Time complexity: O(n^3) for Floyd–Warshall (with n ≤ 100, that's ~1e6 iterations of innermost body, trivial). Space complexity: O(n^2) for the matrix.

Alternative: Do BFS/DFS from each node to compute reachable sets (O(n*(n+m)) time), or optimize using bitsets for faster inner loops. But Floyd–Warshall is simplest and clear.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        n = numCourses
        # reachable[i][j] will be True if i is a prerequisite of j (i -> ... -> j)
        reachable = [[False] * n for _ in range(n)]
        
        # direct prerequisites
        for a, b in prerequisites:
            reachable[a][b] = True
        
        # Floyd-Warshall style transitive closure
        for k in range(n):
            for i in range(n):
                if reachable[i][k]:
                    row_i = reachable[i]
                    row_k = reachable[k]
                    # propagate all j such that k -> j to i -> j
                    for j in range(n):
                        if row_k[j]:
                            row_i[j] = True
        
        # answer queries with O(1) lookup
        return [reachable[u][v] for u, v in queries]
```
- Notes:
  - Approach: Build boolean adjacency (reachability) matrix and compute transitive closure with a Floyd–Warshall style triple loop. After that, each query is a matrix lookup.
  - Time complexity: O(n^3) where n = numCourses. Given n ≤ 100, this is efficient.
  - Space complexity: O(n^2) for the reachability matrix.
  - Implementation detail: the inner loops check reachable[i][k] before scanning j to avoid unnecessary work; also local references row_i and row_k slightly optimize Python looping.