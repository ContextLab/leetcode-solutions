# [Problem 3446: Sort Matrix by Diagonals](https://leetcode.com/problems/sort-matrix-by-diagonals/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks to sort each diagonal of an n x n matrix, but with a twist: diagonals on the bottom-left side (including the main diagonal) must be non-increasing, while diagonals on the top-right side must be non-decreasing. Diagonals here are the ones that run from top-left to bottom-right — those share the same value of (i - j).

A straightforward approach is to group elements by their diagonal identifier (i - j), sort each group's values in the required order, and then write them back to the matrix along the same diagonal positions. Because n ≤ 10, even slightly less optimal approaches are fine, but grouping + sorting is clean and simple.

## Refining the problem, round 2 thoughts
- Diagonal identifier: k = i - j ranges from -(n-1) to (n-1). If k >= 0 (i >= j) the diagonal is in the bottom-left triangle including main diagonal and should be sorted non-increasing. If k < 0 it's in the top-right triangle and should be sorted non-decreasing.
- Collect all values for each k into a list, sort accordingly, then write them back following the same traversal order (increasing i and j).
- Implementation detail: after sorting each list, use a pointer or pop from the front via collections.deque to efficiently place elements back. For n ≤ 10, either method is fine; I'll use index pointers for clarity.
- Complexity: There are O(n^2) elements; sorting each diagonal overall costs O(n^2 log n) in the worst case (but n is small). Space O(n^2) to store grouped values.

## Attempted solution(s)
```python
from collections import defaultdict

class Solution:
    def diagonalSort(self, grid: list[list[int]]) -> list[list[int]]:
        n = len(grid)
        diags = defaultdict(list)
        
        # Collect values per diagonal identified by k = i - j
        for i in range(n):
            for j in range(n):
                diags[i - j].append(grid[i][j])
        
        # Sort each diagonal according to its side of the main diagonal
        for k, lst in diags.items():
            if k >= 0:
                # bottom-left triangle (including main diagonal): non-increasing
                lst.sort(reverse=True)
            else:
                # top-right triangle: non-decreasing
                lst.sort()
        
        # Write sorted values back to the grid using index pointers
        pointers = {k: 0 for k in diags}
        for i in range(n):
            for j in range(n):
                k = i - j
                grid[i][j] = diags[k][pointers[k]]
                pointers[k] += 1
        
        return grid
```
- Notes on approach:
  - We group elements by diagonal (i - j), sort groups either ascending or descending depending on k, then refill the matrix in the same diagonal traversal order.
  - Time complexity: O(n^2 log n) overall (collect O(n^2), sorting all diagonals combined is bounded by O(n^2 log n), writing back O(n^2)).
  - Space complexity: O(n^2) for storing diagonal values (in the worst case we store all elements).
  - Because n ≤ 10, this approach is simple and efficient in practice.