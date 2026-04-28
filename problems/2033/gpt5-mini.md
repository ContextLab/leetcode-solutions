# [Problem 2033: Minimum Operations to Make a Uni-Value Grid](https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can add or subtract x any number of times to any element. For it to be possible to make all elements equal, every number must be congruent modulo x to the same remainder (otherwise you can't change remainders by adding/subtracting multiples of x). If that condition holds, we can consider changing elements in steps of x; each operation changes a value by x, so number of operations to change a to b is |a - b| / x (which will be integer if congruences match).

We want to pick the final value that minimizes total operations. This is minimizing sum of absolute differences (|ai - t|) where each difference is measured in units of x. Minimizing sum of absolute differences is solved by choosing t to be a median of the values. So flatten the grid, check remainders, pick median, compute total operations as sum(|ai - median| / x).

Edge cases: single element (0 ops), impossible case due to differing remainders, even count where any median in interval works (pick lower/any median).

## Refining the problem, round 2 thoughts
- Confirm feasibility: check ai % x are all equal.
- Implementation detail: flatten grid to 1D list. Because mn <= 1e5, sorting (N log N) is fine. Could also use selection algorithm (O(N)) to find median but not necessary here.
- Because all ai have same remainder, (ai - median) is divisible by x, so integer division is safe.
- Complexity: O(N log N) time for sorting, O(N) extra space for flattened list.
- Alternative: scale down by subtracting remainder and dividing values by x to work with smaller integers; equivalently compute ops using //x.
- Example of impossible case: grid = [[1,2],[3,4]] with x = 2 because remainders are mixed.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        # Flatten the grid
        vals = [v for row in grid for v in row]
        n = len(vals)
        if n == 0:
            return 0

        # Check all values have the same remainder modulo x
        r = vals[0] % x
        for v in vals:
            if v % x != r:
                return -1

        # Sort and pick median
        vals.sort()
        median = vals[n // 2]

        # Sum operations: each operation changes by x, so use integer division
        ops = 0
        for v in vals:
            ops += abs(v - median) // x
        return ops
```
- Notes:
  - Approach: Flatten grid, check modulo-x feasibility, pick median to minimize L1 distance, compute total ops as sum(|ai - median| / x).
  - Time complexity: O(N log N) dominated by sorting (N = m * n).
  - Space complexity: O(N) for the flattened list.
  - Implementation detail: Because all values share same remainder modulo x, (v - median) is divisible by x, so integer division // x is safe. This avoids floating arithmetic.