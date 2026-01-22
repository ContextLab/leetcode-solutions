# [Problem 2033: Minimum Operations to Make a Uni-Value Grid](https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t provide stream-of-consciousness text, but here is a concise summary of the approach:
- All elements must be reachable from each other by adding/subtracting multiples of x, so every element must have the same remainder modulo x.
- If the modulo check passes, convert the grid to a flat list and pick a target value that minimizes the sum of absolute differences. The median of the values minimizes sum |a - t|.
- Each operation changes a value by x, so the number of operations for an element is abs(a - target) // x. Sum these to get the answer.

## Refining the problem, round 2 thoughts
Concise refinements and edge cases:
- First check feasibility: every grid[i][j] % x must equal grid[0][0] % x. If not, return -1.
- Use median of flattened values to minimize total moves (works for integer steps because all values differ by multiples of x).
- Implementation choices:
  - Sorting flattened list (O(N log N) where N = m * n) and taking median is simple and acceptable because N ≤ 1e5.
  - Could use selection algorithm for O(N) but unnecessary here.
- Compute steps as integer division by x, i.e., abs(a - median) // x.
- Return sum of steps as integer.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        # Flatten grid
        vals = [v for row in grid for v in row]
        n = len(vals)
        if n == 0:
            return 0
        
        # Check modulo compatibility
        mod0 = vals[0] % x
        for v in vals:
            if v % x != mod0:
                return -1
        
        # Sort and pick median
        vals.sort()
        median = vals[n // 2]
        
        # Sum operations: each op changes by x, so steps = abs(diff) // x
        ops = 0
        for v in vals:
            ops += abs(v - median) // x
        
        return ops
```
- Solution approach: flatten grid, verify all elements share same remainder mod x, choose median target (minimizes sum of absolute differences), sum moves as abs(diff)//x.
- Time complexity: O(N log N) due to sorting, where N = m * n (N ≤ 1e5).
- Space complexity: O(N) for the flattened list.