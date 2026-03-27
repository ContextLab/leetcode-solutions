# [Problem 2946: Matrix Similarity After Cyclic Shifts](https://leetcode.com/problems/matrix-similarity-after-cyclic-shifts/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are applying the same cyclic shift operation to each row k times: even-indexed rows shift left, odd-indexed rows shift right. Doing the same shift repeatedly is equivalent to shifting by (k mod n) positions where n is the row length. So for each row we only need to check whether that row is invariant under the appropriate net shift. If any row after the net shift differs from the original row, the final matrix differs from the original. Edge-case: when k % n == 0 no change; when all elements equal any shift gives same row. Another thought: we could reason with cycles/GCD, but a simple slice-based rotation comparison is enough given constraints (m,n <= 25).

## Refining the problem, round 2 thoughts
- Let n = number of columns, s = k % n. For even i, net operation is left shift by s; for odd i, net operation is right shift by s (equivalently left shift by n - s).
- If s == 0, all rows unchanged => return True quickly.
- For each row, compute the rotated version using slicing and compare to the original row. If any mismatch => False.
- Time complexity O(m * n) and space O(n) additional per-row for the rotated list (but can also be done in O(1) extra by comparing indices). Given constraints this is fine.
- Edge cases: single-column (n = 1) => always unchanged since s % 1 == 0; all-equal rows; small/large k covered by modulo.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def areSimilarAfterShifts(self, mat: List[List[int]], k: int) -> bool:
        if not mat:
            return True
        m = len(mat)
        n = len(mat[0])
        # effective shift amount
        s = k % n
        if s == 0:
            return True
        for i in range(m):
            row = mat[i]
            if i % 2 == 0:
                # even-indexed rows: left shift by s
                rotated = row[s:] + row[:s]
            else:
                # odd-indexed rows: right shift by s
                rotated = row[-s:] + row[:-s]
            if rotated != row:
                return False
        return True
```
- Notes:
  - Approach: compute effective shift s = k % n. For each row, build its shifted version and compare to original. Even rows use left rotation, odd rows use right rotation.
  - Time complexity: O(m * n) where m = number of rows and n = number of columns (building and comparing each row).
  - Space complexity: O(n) extra per row for the rotated list (can be lowered by index-wise comparison if desired).