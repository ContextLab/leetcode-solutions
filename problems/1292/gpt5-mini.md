# [Problem 1292: Maximum Side Length of a Square with Sum Less than or Equal to Threshold](https://leetcode.com/problems/maximum-side-length-of-a-square-with-sum-less-than-or-equal-to-threshold/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the largest side length L such that there exists an L x L sub-square whose sum <= threshold. The brute force: for every top-left and every possible size compute sum by summing elements — that's too slow (O(m * n * L^2)). A common trick for submatrix sums is a 2D prefix-sum (summed-area table) which lets you compute any sub-square sum in O(1). With prefix sums we can check all positions for a given L in O(m * n). Then we can either scan L from 1..min(m,n) (O(m*n*min)), or binary search L to reduce to O(m*n*log(min)). Binary search seems natural and efficient. Need to be careful with indices and off-by-one in prefix sums. Also consider small edge cases: threshold may be 0, matrix values up to 1e4, but Python ints handle sums fine.

## Refining the problem, round 2 thoughts
Refinement:
- Build prefix sum array ps of size (m+1)x(n+1) where ps[i][j] is sum of mat[:i][:j] (i and j are counts).
- For given side k, iterate bottom-right corner (i, j) in ps coordinates with i from k..m and j from k..n. Sum of square with bottom-right at (i,j) and size k is:
  sum = ps[i][j] - ps[i-k][j] - ps[i][j-k] + ps[i-k][j-k]
  Check <= threshold.
- Binary search over k in [1, min(m,n)]. If no k works, return 0.
Edge cases:
- If threshold is very small and no single cell <= threshold, return 0.
- If mat dimensions up to 300, prefix sum O(m*n) memory and time are fine.
Time / space:
- Building prefix sums: O(m*n) time, O(m*n) space.
- Each check for k: O(m*n).
- Binary search over up to log(min(m,n)) iterations: overall O(m*n*log(min(m,n))).
This is acceptable: at worst 300*300*~9 ≈ 810k checks.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        m = len(mat)
        n = len(mat[0]) if m > 0 else 0
        if m == 0 or n == 0:
            return 0

        # Build (m+1) x (n+1) prefix sum array
        ps = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            row_sum = 0
            for j in range(1, n + 1):
                row_sum += mat[i-1][j-1]
                ps[i][j] = ps[i-1][j] + row_sum

        # Helper to check if there exists a k x k square with sum <= threshold
        def exists_square_of_size(k: int) -> bool:
            if k == 0:
                return True
            for i in range(k, m + 1):
                for j in range(k, n + 1):
                    total = ps[i][j] - ps[i-k][j] - ps[i][j-k] + ps[i-k][j-k]
                    if total <= threshold:
                        return True
            return False

        lo, hi = 1, min(m, n)
        best = 0
        # Binary search over side length
        while lo <= hi:
            mid = (lo + hi) // 2
            if exists_square_of_size(mid):
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        return best
```
- Notes:
  - Approach: build 2D prefix sums to compute any square sum in O(1). Binary search the side length to reduce checks.
  - Time complexity: O(m * n * log(min(m, n))) — building prefix sums O(m*n), each binary-search step checks all possible positions O(m*n).
  - Space complexity: O(m * n) for the prefix-sum array ps.
  - Implementation detail: ps is sized (m+1)x(n+1) to simplify boundary handling; indices in mat are offset by 1 when using ps.