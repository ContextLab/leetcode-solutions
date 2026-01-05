# [Problem 1975: Maximum Matrix Sum](https://leetcode.com/problems/maximum-matrix-sum/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The operation flips the sign of two adjacent cells (multiply both by -1). That toggles the sign of two entries at once. I recall similar problems where flipping pairs implies the parity (even/odd) of the number of negative elements is important because each operation changes the count of negative elements by 0 or ±2. So the parity of negative count is invariant when there are no zeros. If the negative count is even, we should be able to make every entry non-negative; if it's odd, at least one negative must remain. If there is any zero, we can use that zero together with a negative to toggle a single negative to positive (zero remains zero), effectively allowing us to achieve any parity. The best final sum should be the sum of absolute values except when we are forced to leave one element negative — in that case we should leave the smallest absolute-value element negative, costing 2 * min_abs from the total absolute sum.

So the approach: scan matrix, compute total sum of absolute values, count negatives, find minimum absolute value, and check for zeros. Return total_abs if neg_count even or zero exists; otherwise return total_abs - 2 * min_abs.

## Refining the problem, round 2 thoughts
Edge cases:
- Zeros: If any zero exists, we can always reach total_abs (no penalty).
- All values positive: trivial, return sum.
- All values negative: if count is even, all can be flipped to positive; if odd and no zero, one smallest-abs stays negative and we subtract twice its abs.
- Keep in mind 0 * -1 = 0, so flipping a zero and a negative changes negative count by 1 effectively (allowing parity change).
Time and space: a single pass O(n^2) time, O(1) extra space. n <= 250 so fine. Values up to 1e5, Python integers handle sums easily.

## Attempted solution(s)
```python
class Solution:
    def maximumMatrixSum(self, matrix: list[list[int]]) -> int:
        total_abs = 0
        neg_count = 0
        has_zero = False
        min_abs = float('inf')

        for row in matrix:
            for val in row:
                if val == 0:
                    has_zero = True
                if val < 0:
                    neg_count += 1
                a = abs(val)
                total_abs += a
                if a < min_abs:
                    min_abs = a

        # If there's a zero or the number of negatives is even, we can make all non-negative.
        if has_zero or (neg_count % 2 == 0):
            return total_abs
        # Otherwise, we must leave one smallest-abs value negative: subtract 2 * min_abs
        return total_abs - 2 * min_abs
```
- Notes:
  - Approach: Compute sum of absolute values, count negatives, detect zeros, track minimum absolute value. If negatives count is even or there's a zero, the maximum sum equals total sum of absolute values. If negatives count is odd and no zero exists, we must leave one element negative; to maximize sum that negative should be the element with smallest absolute value, giving total_abs - 2 * min_abs.
  - Time complexity: O(n^2) where n is matrix dimension (we visit each element once).
  - Space complexity: O(1) extra space beyond input.
  - Implementation detail: treat zero specially because flipping a negative with a zero toggles the parity of negative count (zero stays zero), enabling us to reach the total absolute sum.