# [Problem 3643: Flip Square Submatrix Vertically](https://leetcode.com/problems/flip-square-submatrix-vertically/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to flip a k x k square submatrix, whose top-left corner is at (x, y), by reversing the order of its rows vertically. That means the top row of the submatrix becomes the bottom row, the second becomes the second-from-bottom, etc., but columns within each row remain in the same left-to-right order.

First idea: simply swap corresponding rows inside the submatrix. For each i from 0 to k//2 - 1, swap the entire row (x + i) segment [y, y+k) with row (x + k - 1 - i) segment. This is straightforward, in-place, and O(k * k) time because each swap touches k elements, and there are ~k/2 swaps.

Alternative: extract the k rows into a temporary list, reverse that list, and write them back. That uses O(k * k) time and O(k * k) extra space; the in-place swapping is better for space.

Edge cases: k == 1 -> no change. Small grid sizes OK.

## Refining the problem, round 2 thoughts
Implementation details:
- Ensure we only swap columns y..y+k-1, not entire rows of the grid.
- Use simultaneous swapping of elements or swap slice by slice. In Python, swapping slices with assignment will create temporaries; explicit element-wise swaps are fine and clear.
- Complexity: time O(k*k) because we touch k elements for each of ~k/2 row swaps -> ~k^2/2 operations; space O(1) extra (in-place).
- Constraints are small (m,n <= 50), so this is efficient.

I'll implement an in-place element-wise swap across the relevant columns for each pair of rows to be swapped. Return the modified grid.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def flipVertically(self, grid: List[List[int]], x: int, y: int, k: int) -> List[List[int]]:
        # Swap rows inside the k x k submatrix vertically.
        # For each offset i from 0 to k//2 - 1, swap row (x+i)[y:y+k] with row (x+k-1-i)[y:y+k]
        for i in range(k // 2):
            r1 = x + i
            r2 = x + k - 1 - i
            # swap columns y .. y+k-1 between r1 and r2
            for c in range(y, y + k):
                grid[r1][c], grid[r2][c] = grid[r2][c], grid[r1][c]
        return grid
```
- Notes:
  - Approach: in-place swapping of corresponding rows within the submatrix. For each pair of rows equidistant from the top and bottom of the k x k submatrix, swap their k elements in the columns range [y, y+k).
  - Time complexity: O(k * k) — each of about k/2 row-swaps touches k elements, so ~k^2/2 operations.
  - Space complexity: O(1) extra space (in-place).
  - Handles k == 1 (no swaps performed) and respects bounds because 1 <= k <= min(m-x, n-y) per constraints.