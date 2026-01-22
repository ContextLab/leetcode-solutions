# [Problem 1380: Lucky Numbers in a Matrix](https://leetcode.com/problems/lucky-numbers-in-a-matrix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need numbers that are minimum in their row and maximum in their column. The straightforward idea: compute the minimum value for each row and the maximum value for each column, then find values that satisfy both properties. Because the matrix size is small (m,n ≤ 50) an O(m * n) scan is fine. Since all elements are distinct, any value that appears in both "row-min" set and "col-max" set is a lucky number. Another thought: we could keep indices (rowMinIndex) and check column maxima at those indices, but computing two arrays (row minima, column maxima) is simplest and clean.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- Single element matrix: that element is both row-min and col-max, so it's lucky.
- Distinctness guarantees no repeats, so intersection logic is safe.
- Implementation choices: (a) compute row_mins list and col_max list then scan matrix checking equality, or (b) compute sets of row minima and column maxima and take intersection. Option (b) is concise and uses O(m + n) extra space.
- Complexity target: O(m * n) time to compute column maxima (or to scan matrix), O(m + n) space for the two arrays/sets.

I'll implement the set-intersection approach for clarity and simplicity.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def luckyNumbers (self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return []
        m, n = len(matrix), len(matrix[0])
        # Row minima
        row_mins = [min(row) for row in matrix]
        # Column maxima
        col_maxes = [max(matrix[i][j] for i in range(m)) for j in range(n)]
        # Use sets and intersection (elements are distinct)
        row_min_set = set(row_mins)
        col_max_set = set(col_maxes)
        lucky = list(row_min_set & col_max_set)
        return lucky
```
- Notes:
  - Approach: compute minimum of each row and maximum of each column, then return the intersection of those values (every lucky number must be both).
  - Time complexity: O(m * n) — computing each column maximum requires scanning m rows for each of n columns (or scanning entire matrix to build both lists).
  - Space complexity: O(m + n) for storing row minima and column maxima (plus output).
  - Implementation details: uses Python built-ins min and max and set intersection for concise code. The distinctness constraint guarantees no duplicate values to worry about; returning the intersection in any order is allowed.