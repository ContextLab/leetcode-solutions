# [Problem 1351: Count Negative Numbers in a Sorted Matrix](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[The matrix is sorted in non-increasing order both row-wise (left to right decreases) and column-wise (top to bottom decreases). I need to count negatives quickly. A naive approach is to check every cell O(m*n). Since rows are sorted, in each row I could binary search the first negative index, giving O(m log n). But the follow-up asks for O(m + n). I recall a standard trick: start at the top-right corner. If that element is negative, then everything below in that column must be negative (because column is non-increasing downwards), so I can add (m - i) and move left one column. If it's non-negative, move down to next row. That walks at most m + n steps. This should be simple and constant extra space.]

## Refining the problem, round 2 thoughts
[Check edge cases: all positives -> algorithm should return 0 (we'll just move down rows and never add). All negatives -> starting at top-right it's negative so we add m and move left repeatedly until columns exhausted, total m*n. Single row/column cases should work. Must ensure indices don't go out of range. Alternative: binary search per row (O(m log n)) is acceptable for constraints up to 100x100 but follow-up prefers O(m + n). Time complexity for two-pointer top-right approach is O(m + n), space O(1). Implementation detail: start i = 0 (row), j = n - 1 (col). While i < m and j >= 0: if grid[i][j] < 0: count += m - i; j -= 1 else: i += 1.]

## Attempted solution(s)
```python
class Solution:
    def countNegatives(self, grid: list[list[int]]) -> int:
        m = len(grid)
        if m == 0:
            return 0
        n = len(grid[0])
        i, j = 0, n - 1
        count = 0
        # Start at top-right, move left when we find negatives (adding whole column below),
        # move down when value is non-negative.
        while i < m and j >= 0:
            if grid[i][j] < 0:
                # All elements grid[i..m-1][j] are negative
                count += (m - i)
                j -= 1
            else:
                i += 1
        return count
```
- Notes:
  - Approach: two-pointer traversal starting at top-right achieves O(m + n) time by moving either left or down on each step.
  - Time complexity: O(m + n), where m = number of rows and n = number of columns.
  - Space complexity: O(1) additional space.
  - Correctness: Uses the sorted (non-increasing) property both row-wise and column-wise to count entire columns below a discovered negative in constant time per column move.