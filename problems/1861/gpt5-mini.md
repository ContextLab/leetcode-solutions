# [Problem 1861: Rotating the Box](https://leetcode.com/problems/rotating-the-box/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to rotate the box 90 degrees clockwise, but stones ('#') fall after rotation due to gravity. Rather than literally rotating first and then simulating gravity (which is possible), I notice gravity after rotation points "down" in the rotated matrix — that corresponds to the right direction in the original matrix. So if we first let stones fall to the right in each original row (until they hit '*' or the row edge), then rotate the whole grid clockwise, the result will match the described behavior. This avoids simulating falling in the rotated coordinates and keeps things simple by working in-place (row by row) before the rotation.

A common technique: for each row, scan from right to left, keep a write pointer at the rightmost available position (just before any obstacle '*'), and move stones to that pointer.

## Refining the problem, round 2 thoughts
- Work row-by-row independently. For each row, process from right to left:
  - If we see '*', reset the write pointer to the position just left of the obstacle.
  - If we see '#', move it to the write pointer (set the original spot to '.'), decrement write pointer.
  - If we see '.', just continue.
- After processing all rows, build the rotated matrix of size n x m by mapping new[j][m-1-i] = box[i][j].
- Edge cases:
  - Rows that contain no stones or no obstacles.
  - Single row or single column (m or n = 1).
  - Large grids (up to 500x500) — algorithm must be O(m*n).
- Complexity:
  - Time: O(m * n) — one scan to let stones fall and one scan to rotate.
  - Space: O(m * n) for the returned rotated grid. In-place adjustments for the falling step (no extra grid needed there).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def rotateTheBox(self, boxGrid: List[List[str]]) -> List[List[str]]:
        # Let stones fall to the right in each original row (right is "down" after rotation)
        m = len(boxGrid)
        n = len(boxGrid[0]) if m > 0 else 0
        # Work on a shallow copy of rows to avoid mutating caller's input if desired:
        box = [row[:] for row in boxGrid]

        for i in range(m):
            write = n - 1  # rightmost position where a stone can fall within current segment
            # scan from right to left
            for j in range(n - 1, -1, -1):
                if box[i][j] == '*':
                    # obstacle: next available position is just left of it
                    write = j - 1
                elif box[i][j] == '#':
                    # move stone to 'write' if needed
                    if j != write:
                        box[i][j] = '.'
                        box[i][write] = '#'
                    write -= 1
                # if '.', do nothing

        # Now rotate 90 degrees clockwise to produce the final shape
        rotated = [['.' for _ in range(m)] for _ in range(n)]
        for i in range(m):
            for j in range(n):
                rotated[j][m - 1 - i] = box[i][j]

        return rotated
```
- Notes on approach:
  - The key observation: after a 90-degree clockwise rotation, gravity acts along the original rows' right direction. So we can simulate stones falling to the right before rotating.
  - The in-row rightward "fall" is implemented with a write pointer that is reset when an obstacle '*' is encountered.
- Complexity:
  - Time: O(m * n) — each cell is touched a constant number of times.
  - Space: O(m * n) for the output matrix; the falling step modifies a copy of the input rows in-place, so additional auxiliary space is O(1) beyond the output.