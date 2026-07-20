# [Problem 1260: Shift 2D Grid](https://leetcode.com/problems/shift-2d-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
When I first read this, I think of performing the described shift operation k times. Doing that naively (simulate one shift, repeat k times) would be straightforward but could be inefficient if k were large. However, constraints show m,n ≤ 50 and k ≤ 100, so naive might actually pass here — but it's still good practice to do it in O(m*n) time regardless of k.

This is basically a rotation of all elements in row-major order by k positions to the right. So flatten the 2D grid into a 1D list, rotate that list by k (with k reduced mod total elements), and then reshape back into m x n. Alternatively, we can compute index mapping directly without an intermediate list.

I should be careful to take k % (m*n) and handle k == 0 specially (just return the grid as-is or a copy).

## Refining the problem, round 2 thoughts
Refinements:
- Compute total = m * n and do k = k % total to avoid unnecessary work.
- Flattening to a 1D list makes rotation easier: rotated = flat[-k:] + flat[:-k] (if k > 0).
- Reconstruct the 2D result by slicing the rotated list into rows of length n.
- Edge cases:
  - k == 0 (or k % total == 0) -> return the original grid (or a shallow copy).
  - m or n equals 1 -> still works with flatten+rotate approach.
- Complexity: flattening is O(total) time and space; rotating using slicing is O(total); rebuilding is O(total). So overall O(m*n) time and O(m*n) extra space. We could do an in-place cycle-rotate with O(1) extra space, but it's unnecessary here and adds complexity.

Now implement the clear, concise Python solution using flatten / slice / reshape.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m = len(grid)
        n = len(grid[0]) if m > 0 else 0
        total = m * n
        if total == 0:
            return grid
        
        k %= total
        if k == 0:
            # No change needed; return a copy to avoid mutating input if that matters
            return [row[:] for row in grid]
        
        # Flatten the grid in row-major order
        flat = [grid[i][j] for i in range(m) for j in range(n)]
        # Rotate the flattened list to the right by k
        rotated = flat[-k:] + flat[:-k]
        # Reconstruct the 2D grid
        res = []
        for i in range(m):
            row = rotated[i * n : (i + 1) * n]
            res.append(row)
        return res
```
- Notes about the approach:
  - We flatten the 2D grid to a 1D list in row-major order, perform a right rotation by k using slicing, and then reshape back to m x n.
  - Time complexity: O(m * n) — flattening, slicing and rebuilding each touch each element a constant number of times.
  - Space complexity: O(m * n) extra space for the flattened and rotated lists (can be reduced with an in-place cycle rotation, but not necessary given constraints).
  - Important detail: reduce k with k %= m*n to handle cases where k ≥ total elements.