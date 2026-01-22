# [Problem 36: Valid Sudoku](https://leetcode.com/problems/valid-sudoku/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to verify three constraints (rows, columns, 3x3 sub-boxes) for a 9x9 board. The board is partially filled and uses '.' for empties, so only filled cells matter. The straightforward idea: iterate every cell and for each non '.' check whether the digit has already appeared in the same row, column, or box. Using sets to track seen digits is natural. For boxes I can compute an index like (r//3, c//3) or flatten to single index 3*(r//3) + (c//3). If any duplicate is found return False early. This is simple and fast.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- The constraints guarantee 9x9 and only digits '1'..'9' or '.', so I don't need extra validation, but code can be robust if desired.
- Use three arrays of sets: rows[9], cols[9], boxes[9]. When visiting cell (r,c) with value v:
  - if v in rows[r] return False
  - if v in cols[c] return False
  - box index b = (r//3)*3 + (c//3); if v in boxes[b] return False
  - otherwise add v to each set.
- Alternative solutions: bitmasks instead of sets to reduce overhead, or do three separate scans (one for rows, one for cols, one for boxes). But a single pass with 3 sets per cell is concise and O(1) time for fixed board size.
- Time complexity: O(81) = O(1) for fixed-size, or in general O(n^2) for an n x n board. Space complexity: O(27) sets storing up to 81 elements total → O(n^2) worst-case; for fixed board it's constant.
- Implementation details: compute box index carefully; early exit on violation.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # rows[i] contains digits seen in row i
        rows = [set() for _ in range(9)]
        # cols[j] contains digits seen in column j
        cols = [set() for _ in range(9)]
        # boxes[k] contains digits seen in 3x3 box k, where k = (i//3)*3 + (j//3)
        boxes = [set() for _ in range(9)]

        for i in range(9):
            for j in range(9):
                val = board[i][j]
                if val == '.':
                    continue

                # Check row
                if val in rows[i]:
                    return False
                rows[i].add(val)

                # Check column
                if val in cols[j]:
                    return False
                cols[j].add(val)

                # Check 3x3 box
                box_index = (i // 3) * 3 + (j // 3)
                if val in boxes[box_index]:
                    return False
                boxes[box_index].add(val)

        return True
```
- Notes:
  - Approach: Single pass through the board while maintaining sets for rows, columns, and 3x3 boxes. For each filled cell, check for duplicates in the corresponding row/column/box and return False on the first violation.
  - Time complexity: O(1) for a fixed 9x9 board (practically O(81)), or O(n^2) for an n x n board. Each cell results in O(1) set operations (avg).
  - Space complexity: O(1) for fixed board (a constant number of small sets), or O(n^2) in the worst case as the sets can store up to all elements of the board.
  - This implementation is simple, clear, and efficient for the problem constraints.