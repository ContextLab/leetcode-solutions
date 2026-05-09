# [Problem 1914: Cyclically Rotating a Grid](https://leetcode.com/problems/cyclically-rotating-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to rotate each "layer" (ring) of the matrix independently by k steps in the counter-clockwise direction. The grid is m x n with both m and n even, so the number of layers is min(m, n) // 2. For each layer we can extract the elements along its perimeter into a linear list (in some traversal order), rotate that list by k (mod its length), and then write the rotated values back to the same perimeter positions.

A key detail: how to pick the traversal order so that applying a simple array rotation corresponds to moving elements counter-clockwise in the grid. If we extract elements in counter-clockwise (CCW) order (for example: down the left column, right across the bottom row, up the right column, and left across the top row), then a rotation of the linear list by k positions forward (i.e., placing arr[i] at new index (i + k) % L) corresponds to moving each value k steps along the CCW direction on the grid.

So plan: for each layer l:
- collect coords in CCW order
- build values list
- k %= len(values)
- rotated_values[(i+k) % L] = values[i]
- write rotated_values back into grid using coords

This visits each cell a constant number of times, so O(m*n) time and O(m*n) extra in worst case for temporary lists (but per-layer lists are smaller overall).

## Refining the problem, round 2 thoughts
Edge cases:
- Very large k: reduce with modulo by ring length.
- Smallest layer when m or n are 2 still works with traversal logic.
- Ensure we don't duplicate corners when collecting coordinates (careful with loop bounds).
- Complexity: we extract and write back each cell exactly once across all layers, so O(m*n) time, and extra space is O(max perimeter length) which is O(m+n) per layer but worst-case across layers summed is O(m*n). Memory is acceptable for constraints.

Alternative: rotate in-place by walking cycles along ring, but extracting to list is simpler and clear.

Now implement the solution.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m = len(grid)
        n = len(grid[0])
        layers = min(m, n) // 2
        
        for l in range(layers):
            top, left = l, l
            bottom, right = m - 1 - l, n - 1 - l
            
            coords = []
            # down the left column
            for r in range(top, bottom + 1):
                coords.append((r, left))
            # right across the bottom row (excluding the corner already included)
            for c in range(left + 1, right + 1):
                coords.append((bottom, c))
            # up the right column (excluding the bottom corner)
            for r in range(bottom - 1, top - 1, -1):
                coords.append((r, right))
            # left across the top row (excluding the right corner and left corner)
            for c in range(right - 1, left, -1):
                coords.append((top, c))
            
            vals = [grid[r][c] for (r, c) in coords]
            L = len(vals)
            if L == 0:
                continue
            kk = k % L
            if kk == 0:
                continue
            
            rotated = [0] * L
            for i, v in enumerate(vals):
                rotated[(i + kk) % L] = v
            
            for (r, c), v in zip(coords, rotated):
                grid[r][c] = v
        
        return grid
```
- Notes:
  - We extract coordinates of each ring in counter-clockwise order: down left column, right across bottom, up right column, left across top. This order ensures that shifting the array forward by k corresponds to moving each element k steps counter-clockwise in the grid.
  - Time complexity: O(m * n) — each grid cell is read and written a constant number of times.
  - Space complexity: O(m * n) worst case across layers for temporary lists (practically O(perimeter) per layer). The implementation uses per-layer temporary lists for coordinates and values.