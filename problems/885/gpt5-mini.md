# [Problem 885: Spiral Matrix III](https://leetcode.com/problems/spiral-matrix-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to walk in a clockwise spiral starting facing east from (rStart, cStart) and record positions that fall inside the rows x cols grid until I've seen every cell inside the grid. The natural approach is to simulate the spiral movement: move east 1, south 1, west 2, north 2, east 3, south 3, ... i.e., step-length increases by 1 after every two directions. As I move, I check whether the current cell is inside the grid bounds and if so add it to the result. Stop once we've collected rows * cols positions. This avoids building the whole outer infinite spiral beforehand. Edge cases: very small grids (1x1, 1xN), starting near edges or corners; but the general simulation handles those.

## Refining the problem, round 2 thoughts
- Direction order must be exactly: east, south, west, north, repeating.
- Keep a counter of how many cells we've added; stop when it equals rows * cols.
- We should append the starting cell first (it is guaranteed inside the grid).
- Implementation detail: after two directions, increase the step length.
- Complexity: we only append when inside bounds; the simulation may traverse some positions outside the grid, but the total number of steps until filling the grid is bounded (practically O(rows * cols) for constraints up to 100). Space complexity is O(rows * cols) for the output.
- Alternatives: computing ring-by-ring coordinates with clamped boundaries is possible but more error-prone; simulation is straightforward and robust.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def spiralMatrixIII(self, rows: int, cols: int, rStart: int, cStart: int) -> List[List[int]]:
        # Directions: east, south, west, north
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        ans = []
        total = rows * cols
        
        r, c = rStart, cStart
        ans.append([r, c])  # starting cell (guaranteed inside)
        if total == 1:
            return ans
        
        step_len = 1
        dir_idx = 0  # start facing east
        while len(ans) < total:
            # do two directions with the same step length
            for _ in range(2):
                dr, dc = dirs[dir_idx % 4]
                for _ in range(step_len):
                    r += dr
                    c += dc
                    if 0 <= r < rows and 0 <= c < cols:
                        ans.append([r, c])
                        if len(ans) == total:
                            return ans
                dir_idx += 1
            step_len += 1
        
        return ans
```
- Notes:
  - Approach: simulate the spiral using direction vectors and step lengths that increase after every two directions (east, south, west, north cycle).
  - Time complexity: O(R * C) positions will be appended; the simulation may take somewhat more steps (walking outside the grid), but with rows, cols <= 100 this is fine. In terms of asymptotics it's bounded by O(max(rows, cols)^2) in the worst interpretation of spiral steps, but effectively we stop after collecting rows*cols valid cells.
  - Space complexity: O(R * C) for the output list.