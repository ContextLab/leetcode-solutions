# [Problem 944: Delete Columns to Make Sorted](https://leetcode.com/problems/delete-columns-to-make-sorted/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count how many columns (positions across all strings) are not sorted top-to-bottom. The strings all have the same length, so I can iterate column indices 0..m-1 and check that character at row i is <= character at row i+1 for all adjacent rows. If any adjacent pair violates that, the column must be deleted.

In Python a neat trick is to use zip(*strs) to iterate columns as tuples. For each column tuple, check whether it's non-decreasing. Alternatives: build each column string and compare it to its sorted version, or check adjacent pairs directly. The simplest is checking adjacent pairs to allow early exit when a violation is found.

## Refining the problem, round 2 thoughts
Edge cases:
- Only one row (n = 1) — every column is trivially sorted, so answer is 0.
- All columns unsorted — count equals length of strings.
- Performance: n up to 100, m up to 1000, so an O(n * m) solution is fine.

Choice between implementations:
- zip(*strs) + any(previous > current for pairs) is clean and avoids creating additional large structures per column.
- Comparing column to sorted(column) is also easy but creates a new list for sorting (slightly more overhead).

Time complexity: O(n * m) where n = number of strings, m = length of each string.
Space complexity: O(1) extra (ignoring input) or O(n) per column if considering the tuple created by zip; overall negligible given constraints.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minDeletionSize(self, strs: List[str]) -> int:
        # Count columns that are not sorted top-to-bottom.
        deletions = 0
        # Iterate over columns using zip to collect column characters
        for col in zip(*strs):
            # If any previous character is greater than the next, column is unsorted
            if any(a > b for a, b in zip(col, col[1:])):
                deletions += 1
        return deletions
```
- Notes:
  - Approach: iterate columns (zip(*strs)) and check adjacent pairs for order violation; increment count if any violation found.
  - Time complexity: O(n * m) where n = number of strings and m = length of each string (we check each character once).
  - Space complexity: O(1) extra (aside from the temporary tuple for each column produced by zip, which is size n).