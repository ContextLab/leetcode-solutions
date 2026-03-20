# [Problem 3567: Minimum Absolute Difference in Sliding Submatrix](https://leetcode.com/problems/minimum-absolute-difference-in-sliding-submatrix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks for the minimum absolute difference between any two distinct values inside every k x k submatrix. "Distinct values" here refers to distinct value *types* (unique values), not distinct positions — the examples confirm that duplicates do not produce a difference of 0 unless there is only one unique value overall (in which case the answer is 0).

A straightforward approach: for each k x k window, collect the unique values, sort them, and compute the minimum difference between consecutive values. Constraints are small (m, n ≤ 30), so the total number of windows is at most 900 and each window has at most 900 elements. A brute-force per-window unique+sort approach is likely sufficient and simple.

I also note a more advanced sliding-window approach using frequency tables + ordered structure or coordinate compression + Fenwick tree could be used for larger constraints, but that's unnecessary here.

## Refining the problem, round 2 thoughts
Edge cases:
- If the unique-value set size is 0 or 1, return 0 for that window.
- Values can be negative, but sorting handles that naturally.
- Complexity: For each of up to (m-k+1)*(n-k+1) windows, we inspect k*k elements and then sort the unique values. In the worst case k=k_max and all values are distinct, this is O((m-k+1)(n-k+1) * (k^2 log k^2)). With m,n ≤ 30 this is easily feasible.

Alternative solutions:
- Maintain a sliding multiset of frequencies as we move the window right and down, along with an ordered structure (like sorted list or balanced BST). That reduces repeated work between neighboring windows, but complexity plus implementation is more intricate and not necessary for these constraints.

I'll implement the simple, clear approach:
- For each top-left corner (i, j) of a k x k submatrix:
  - Gather values into a Python set.
  - If len(set) ≤ 1 -> answer 0.
  - Else sort the unique values and scan to find min difference between consecutive values.

Time complexity: O((m-k+1)(n-k+1) * (k^2 + u log u)) where u ≤ k^2 unique values. For given constraints this is fine.
Space: O(k^2) extra per window (set + sorted list).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minDifference(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m = len(grid)
        n = len(grid[0])
        out_rows = m - k + 1
        out_cols = n - k + 1
        ans = [[0] * out_cols for _ in range(out_rows)]
        
        for i in range(out_rows):
            for j in range(out_cols):
                # collect unique values in k x k submatrix starting at (i, j)
                s = set()
                for r in range(i, i + k):
                    # small optimization: extend from row slice
                    for c in range(j, j + k):
                        s.add(grid[r][c])
                        # early exit: if we already have many values and minimal possible diff is 0 can't occur,
                        # but nothing to early-exit since duplicates do not produce 0; continue normally.
                if len(s) <= 1:
                    ans[i][j] = 0
                    continue
                arr = sorted(s)
                min_diff = float('inf')
                for a, b in zip(arr, arr[1:]):
                    diff = b - a
                    if diff < min_diff:
                        min_diff = diff
                        # smallest possible positive diff is 1 if integers; if 1 break early
                        if min_diff == 1:
                            break
                ans[i][j] = min_diff if min_diff != float('inf') else 0
        return ans
```
- Notes:
  - This solution collects unique values per k x k window using a set, sorts them, and finds the minimum adjacent difference.
  - Time complexity is acceptable given m, n ≤ 30: at most ~900 windows and up to 900 elements per window.
  - Space usage is dominated by the temporary set and sorted list per window: O(k^2).
  - A more complex sliding-window approach with a frequency map + ordered container (to reuse work between windows) is possible but unnecessary for these constraints.