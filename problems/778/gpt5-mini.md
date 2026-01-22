# [Problem 778: Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This problem asks for the minimum time t such that there's a path from (0,0) to (n-1,n-1) where every cell along the path has elevation <= t. That suggests the answer is the minimum over all paths of the maximum elevation along the path (i.e., minimize the path's bottleneck). Two standard approaches come to mind:

- Binary search on t (0..n^2-1) and for each candidate t run BFS/DFS to check connectivity using only cells with grid[i][j] <= t.
- Use a Dijkstra-like (best-first) search where the "distance" to a cell is the maximum elevation encountered along the path; use a min-heap keyed by that value and expand greedily.

Both are common; Dijkstra approach directly computes the minimum required time without an outer binary search and is elegant here.

Also note trivial case n=1 => answer grid[0][0].

## Refining the problem, round 2 thoughts
Dijkstra-like method: priority queue holds tuples (current_required_time, i, j) where current_required_time = max elevation along the best-known path to (i,j). Start with (grid[0][0], 0, 0). Pop the smallest current_required_time; if we reach (n-1,n-1) that popped value is the answer. For each neighbor, the new_required_time = max(current_required_time, grid[nx][ny]); push if not visited.

Time complexity: Each cell popped at most once (we mark visited), and each push is for neighbors, so O(n^2 log n^2) = O(n^2 log n). Space: O(n^2) for visited and heap. n <= 50 so this is fine.

Edge cases: n==1, and general bounds. Grid values are unique but algorithm doesn't rely on uniqueness.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if n == 1:
            return grid[0][0]
        
        # Min-heap storing (time_needed, i, j)
        heap = [(grid[0][0], 0, 0)]
        visited = [[False]*n for _ in range(n)]
        visited[0][0] = True
        
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        
        while heap:
            time, i, j = heapq.heappop(heap)
            # If we've reached the target, time is the minimal required water level
            if i == n-1 and j == n-1:
                return time
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n and not visited[ni][nj]:
                    visited[ni][nj] = True
                    # Need to wait for max(current path requirement, neighbor elevation)
                    next_time = max(time, grid[ni][nj])
                    heapq.heappush(heap, (next_time, ni, nj))
        # Problem guarantees reachability eventually, but return statement for completeness
        return -1
```
- Solution approach: Use a best-first search (Dijkstra-like) where the cost to enter a cell is the maximum elevation encountered so far. Pop the cell with smallest such cost and expand neighbors. When the target is popped, that cost is the minimum time required.
- Time complexity: O(n^2 log n^2) = O(n^2 log n) because each of the n^2 cells is pushed/popped at most once and heap operations cost log(heap_size).
- Space complexity: O(n^2) for visited and heap.
- Implementation details: We mark neighbors visited when pushing to avoid multiple pushes for the same cell. Starting time is grid[0][0]; for n==1 we return that immediately.