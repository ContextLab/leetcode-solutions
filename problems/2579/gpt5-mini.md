# [Problem 2579: Count Total Number of Colored Cells](https://leetcode.com/problems/count-total-number-of-colored-cells/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The grid starts with one colored cell. Each minute, every uncolored cell that "touches" a blue cell becomes blue. "Touches" here (from the examples) means sharing an edge (4-directional adjacency), not just corner-touching — the colored region grows like a diamond (Manhattan distance) around the starting cell. After t minutes (t = n), the maximum Manhattan distance from the center that is colored equals n-1. I recall the count for all integer points with |x|+|y| <= r (an L1 ball of radius r) has a simple closed form. Try to derive a formula rather than simulating.

## Refining the problem, round 2 thoughts
Let r = n - 1. For each y from -r to r, the horizontal half-width is r - |y|, so row width = 2*(r - |y|) + 1. Summing over y yields a known sum. Alternatively think of building from center: starting with 1, each outward minute adds 4, then 8, then 12, ... (i.e., 4 * i for i=1..r). So total = 1 + 4 * sum_{i=1..r} i = 1 + 4 * r*(r+1)/2 = 1 + 2*r*(r+1). Replace r with n-1 to get closed form. Edge case n=1 gives 1. Complexity is O(1) time and O(1) space.

## Attempted solution(s)
```python
class Solution:
    def coloredCells(self, n: int) -> int:
        """
        Return the number of colored cells after n minutes.
        Derived formula: r = n - 1
        answer = 1 + 2 * r * (r + 1) = 1 + 2 * (n-1) * n
        """
        return 1 + 2 * (n - 1) * n
```
- Notes:
  - Approach: observe colored cells form an L1-ball (diamond) of radius r = n-1; count lattice points directly or sum incremental rings.
  - Time complexity: O(1).
  - Space complexity: O(1).
  - The result fits in 64-bit for n up to 1e5 (value ~ 2e10), so Python int is safe.