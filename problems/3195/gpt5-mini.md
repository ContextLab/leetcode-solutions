# [Problem 3195: Find the Minimum Area to Cover All Ones I](https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness reasoning, but here is a concise summary of the approach instead:

- We need the smallest axis-aligned rectangle that contains all 1s. That rectangle is determined by the minimum and maximum row indices and the minimum and maximum column indices where a 1 appears.
- So scan the grid once, track min_row, max_row, min_col, max_col for cells equal to 1, and compute area = (max_row - min_row + 1) * (max_col - min_col + 1).

## Refining the problem, round 2 thoughts
- A single full scan of the grid (O(m * n)) is straightforward and fits constraints (up to 1e6 cells).
- Memory usage is O(1) beyond the input.
- Edge cases: input guarantees at least one 1, but implementation can still handle it defensively.
- Alternative approaches (binary search on rows/cols) could be used if we had additional structure, but they are unnecessary here.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minArea(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        min_row, max_row = m, -1
        min_col, max_col = n, -1
        
        for i in range(m):
            row = grid[i]
            for j in range(n):
                if row[j] == 1:
                    if i < min_row:
                        min_row = i
                    if i > max_row:
                        max_row = i
                    if j < min_col:
                        min_col = j
                    if j > max_col:
                        max_col = j
        
        # If no 1s found (problem statement says at least one 1 exists), handle defensively.
        if max_row == -1:
            return 0
        
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        return height * width
```
- Notes:
  - Approach: single-pass scan to find the extreme rows and columns that contain 1s, then compute the bounding rectangle area.
  - Time complexity: O(m * n), where m = number of rows and n = number of columns.
  - Space complexity: O(1) extra space (only a few integer variables).