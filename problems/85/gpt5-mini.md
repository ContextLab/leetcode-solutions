# [Problem 85: Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the largest-area rectangle containing only '1's in a binary matrix. A brute-force approach would enumerate all possible rectangles and check if they're all '1's, but that's O((mn)^2) rectangles times O(mn) check — far too slow for m,n up to 200.

I recall a common trick: treat each row as the base of a histogram where the height at each column is the number of consecutive '1's up to that row. Then the problem reduces, for each row, to "largest rectangle in histogram" which can be solved in O(n) using a monotonic stack. So overall O(m * n) time. That seems promising.

I'll update heights row-by-row and compute largest-rectangle-in-histogram each time. Need to handle edge cases: empty matrix; rows or columns equal to 1; all zeros.

## Refining the problem, round 2 thoughts
- For each row i, compute heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0.
- Compute largest rectangle area from heights with the standard mono-decreasing stack using a sentinel (append a 0).
- Complexity: for m rows and n columns, updating heights is O(n) per row, histogram algorithm is O(n) per row, total O(m*n). Space is O(n) for heights and stack.
- Edge cases: if matrix is empty, return 0. If a row has all zeros, heights will reset to zero and histogram will yield 0 correctly.
- Implementation detail: do not mutate heights length permanently; use a temporary heights_with_sentinel = heights + [0] when scanning with stack.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        heights = [0] * cols
        max_area = 0

        for r in range(rows):
            # update histogram heights for this row
            for c in range(cols):
                if matrix[r][c] == '1':
                    heights[c] += 1
                else:
                    heights[c] = 0

            # compute largest rectangle in histogram heights
            # use a monotonic increasing stack of indices
            stack = []
            extended = heights + [0]  # sentinel to flush stack at the end
            for i, h in enumerate(extended):
                while stack and extended[stack[-1]] > h:
                    height = extended[stack.pop()]
                    width = i if not stack else i - stack[-1] - 1
                    area = height * width
                    if area > max_area:
                        max_area = area
                stack.append(i)

        return max_area
```
- Notes:
  - Approach: treat each row as the base of a histogram of consecutive '1's above that row; for each histogram compute largest rectangle using a monotonic stack.
  - Time complexity: O(rows * cols) — each cell is processed a constant number of times.
  - Space complexity: O(cols) for the heights array and stack.
  - Implementation details: append a 0 sentinel to flush out remaining heights; widths are computed from popped index and current index with stack top as previous smaller index. Handles empty matrix and all-zero rows correctly.