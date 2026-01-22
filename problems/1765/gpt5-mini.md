# [Problem 1765: Map of Highest Peak](https://leetcode.com/problems/map-of-highest-peak/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to assign non-negative heights so water cells are 0 and adjacent cells differ by at most 1, while maximizing the maximum height in the grid. This reminds me of computing distance from water: since heights can only change by at most 1 per step, the height of a land cell can't exceed its shortest distance to any water cell. To maximize heights overall, set each cell's height equal to its distance to the nearest water cell. That suggests a multi-source BFS starting from all water cells simultaneously, assigning distances (heights) as we expand.

## Refining the problem, round 2 thoughts
- Multi-source BFS from all water cells (those with isWater == 1) will compute the shortest distance (in steps) to the nearest water for every cell.
- Initialize heights for water cells to 0 and for land to -1/unvisited.
- Enqueue all water cells; BFS neighbors that are unvisited assign height = curr_height + 1 and enqueue.
- Edge cases: at least one water cell guaranteed. Large grid up to 1e6 cells — BFS is O(mn) and fits memory/time in Python if implemented efficiently.
- Alternative approaches: repeated DP passes or Dijkstra; BFS is simpler and optimal here.
- Complexity: time O(m*n) because each cell is visited once; space O(m*n) for heights and queue.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def highestPeak(self, isWater: List[List[int]]) -> List[List[int]]:
        if not isWater:
            return []
        m, n = len(isWater), len(isWater[0])
        heights = [[-1] * n for _ in range(m)]
        q = deque()
        
        # Initialize queue with all water cells (height 0)
        for i in range(m):
            for j in range(n):
                if isWater[i][j] == 1:
                    heights[i][j] = 0
                    q.append((i, j))
        
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        
        # Multi-source BFS
        while q:
            x, y = q.popleft()
            curr_h = heights[x][y]
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and heights[nx][ny] == -1:
                    heights[nx][ny] = curr_h + 1
                    q.append((nx, ny))
        
        return heights
```
- Notes:
  - Approach: multi-source BFS from all water cells to assign each cell the shortest distance to water, which equals the maximal valid height under the adjacency constraint.
  - Time complexity: O(m * n) — each cell is enqueued and processed at most once; each edge (up to 4 per cell) is considered constant times.
  - Space complexity: O(m * n) for the heights matrix and the BFS queue in the worst case.
  - Implementation details: heights initialized to -1 to mark unvisited; water cells set to 0 and enqueued initially. BFS assigns increasing heights level-by-level. This guarantees the maximum height possible under the rules.