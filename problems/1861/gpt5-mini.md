# [Problem 1861: Rotating the Box](https://leetcode.com/problems/rotating-the-box/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal stream-of-consciousness. I can, however, give a brief high-level summary of the approach I will use:
- Simulate gravity in the original orientation so that stones ('#') fall to the right until they hit an obstacle ('*') or the row end. This is done per row in one pass from right to left.
- After applying gravity (stones now sit as if the box were tilted right), rotate the matrix 90 degrees clockwise to produce the final box.

## Refining the problem, round 2 thoughts
- Observations:
  - Gravity after rotation is equivalent to, before rotation, letting stones slide right within each row until blocked by '*' or the row end.
  - It's efficient to perform an in-place-like transformation per row (using mutable lists) that shifts '#' rightward into the nearest available slot.
  - After processing each row, rotate the resulting matrix using the mapping (i, j) -> (j, m-1-i).
- Edge cases:
  - Rows with no stones or no obstacles behave naturally with the same algorithm.
  - Single-row or single-column matrices are handled normally.
- Complexity:
  - Time: O(m * n) — one pass per cell to settle stones and another O(m * n) to rotate/copy.
  - Space: O(m * n) for the returned rotated matrix (the output); we only use O(1) extra besides the output if we modify rows in place.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def rotateTheBox(self, box: List[List[str]]) -> List[List[str]]:
        m = len(box)
        n = len(box[0])
        
        # Convert each row to mutable list (they already are lists of chars on LeetCode, but ensure)
        for i in range(m):
            row = box[i]
            write = n - 1  # position where next '#' will fall to (rightmost empty in current segment)
            # Sweep from right to left
            for j in range(n - 1, -1, -1):
                if row[j] == '*':
                    # obstacle -> reset write pointer to the cell left of obstacle
                    write = j - 1
                elif row[j] == '#':
                    # move stone to write position if needed
                    if j != write:
                        row[j] = '.'
                        row[write] = '#'
                    write -= 1
                # if '.', do nothing

        # Now rotate box 90 degrees clockwise: new dims are n x m
        res = [['.' for _ in range(m)] for _ in range(n)]
        for i in range(m):
            for j in range(n):
                res[j][m - 1 - i] = box[i][j]
        return res
```
- Notes about the solution approach:
  - First stage (per-row sweep): For each row, scan from right to left with a write pointer indicating the next position a stone should occupy. When encountering an obstacle '*', reset the write pointer to one position left of it because stones cannot cross obstacles. When encountering a stone '#', place it at the write pointer and decrement the write pointer. This yields the configuration as if gravity acted to the right.
  - Second stage (rotation): Build the rotated matrix explicitly using the mapping (i, j) -> (j, m-1-i).
- Complexity:
  - Time: O(m * n) — each cell is examined a constant number of times.
  - Space: O(m * n) for the output matrix. In-place modification of input rows is used to avoid extra per-row space.