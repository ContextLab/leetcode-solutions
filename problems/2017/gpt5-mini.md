# [Problem 2017: Grid Game](https://leetcode.com/problems/grid-game/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a 2 x n grid. Both robots start at (0,0) and end at (1,n-1), only moving right or down. The first robot goes first, collects its path cells (those cells become 0), then the second robot tries to collect as many points as possible. The first robot wants to minimize what the second can get.

Observation: any valid path from top-left to bottom-right that moves only right and down must move right some number of steps on the top row, then move down exactly once, then move right on the bottom row. So a path is fully determined by the column k where the robot moves down (k in [0..n-1]). That simplifies the problem: the first robot's choice is which column k to move down.

If the first robot moves down at column k, it zeroes:
- top row columns 0..k
- bottom row columns k..n-1

What remains for the second robot are:
- top row columns k+1..n-1 (if any)
- bottom row columns 0..k-1 (if any)

The second robot will choose a path (a down-column j) that collects some subset of these remaining cells. Reasoning shows the second's maximum given first's k equals max(sum of bottom[0..k-1], sum of top[k+1..n-1]) (he can either stay on top until after k and pick the top suffix, or go down early and pick the left bottom prefix). So the first robot should pick k that minimizes that maximum.

That suggests a linear scan computing prefix sums of bottom row and suffix sums of top row and returning min_k max(prefix_bottom_up_to_k-1, suffix_top_from_k+1).

## Refining the problem, round 2 thoughts
Edge cases: n = 1 => first robot zeros both cells he visits (top[0] then bottom[0]), leaving nothing for the second -> result 0. Sums can be large (n up to 5e4, values up to 1e5), but Python ints handle it easily. Complexity target O(n) time and O(1) extra space besides input.

Implementation detail: compute total sum of top row. Maintain prefix sums as we iterate k from 0..n-1:
- prefix_bottom = sum bottom[0..k-1]
- prefix_top = sum top[0..k-1]
Then top_right = total_top - prefix_top - top[k] (i.e. sum top[k+1..n-1]). Candidate for that k is max(prefix_bottom, top_right). Keep minimum candidate.

This avoids building extra arrays and runs in O(n) time, O(1) extra memory.

## Attempted solution(s)
```python
class Solution:
    def gridGame(self, grid: list[list[int]]) -> int:
        top = grid[0]
        bottom = grid[1]
        n = len(top)

        total_top = sum(top)
        prefix_top = 0  # sum of top[0..k-1]
        prefix_bottom = 0  # sum of bottom[0..k-1]

        ans = float('inf')
        for k in range(n):
            # top_right = sum of top[k+1..n-1]
            top_right = total_top - prefix_top - top[k]
            bottom_left = prefix_bottom  # sum bottom[0..k-1]

            ans = min(ans, max(bottom_left, top_right))

            # update prefixes for next k
            prefix_top += top[k]
            prefix_bottom += bottom[k]

        return ans
```
- Notes:
  - Approach: iterate over the possible down-column k for the first robot. For each k, the second robot's maximum possible score (after first zeroes its path) is max(sum bottom[0..k-1], sum top[k+1..n-1]). Minimize that over k.
  - Time complexity: O(n) — single pass over columns.
  - Space complexity: O(1) extra space (only a few accumulators), aside from input storage.