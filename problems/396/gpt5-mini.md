# [Problem 396: Rotate Function](https://leetcode.com/problems/rotate-function/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I could compute F(k) directly for each rotation by actually rotating the array (or indexing into it) and summing i * arr_k[i]. That is straightforward but would be O(n^2) in the worst case (n rotations, each O(n) to compute) which is too slow for n up to 1e5.

There must be a recurrence relation between consecutive F(k) values because rotating just reorders indices. I recall there is a standard trick: compute F(0) and the total sum of elements once, then update F(k) from F(k-1) in O(1) time. Need to carefully derive the formula to avoid off-by-one errors: for clockwise rotation by 1, the last element moves to index 0 and every other index shifts right by 1. Figure out how contributions change and which element is subtracted multiplied by n.

Edge cases: n == 1 should return 0 (only index 0 contributes 0 * nums[0]). Negative numbers are allowed but formula still holds. Use 64-bit (Python int is fine).

## Refining the problem, round 2 thoughts
Derive relation precisely:
- Let n = len(nums). Define F(k) as given where arr_k is nums rotated k positions clockwise.
- For k = 1, arr_1[0] = nums[n-1], arr_1[1] = nums[0], ..., arr_1[n-1] = nums[n-2].
- Compute difference F(1) - F(0):
  F(1) = 0*nums[n-1] + 1*nums[0] + 2*nums[1] + ... + (n-1)*nums[n-2]
  F(0) = 0*nums[0] + 1*nums[1] + ... + (n-1)*nums[n-1]
  Subtract: F(1) - F(0) = (1-0)*nums[0] + (2-1)*nums[1] + ... + ((n-1)-(n-2))*nums[n-2] + (0-(n-1))*nums[n-1]
                  = nums[0] + nums[1] + ... + nums[n-2] - (n-1)*nums[n-1]
                  = sum(nums) - n * nums[n-1]
So F(1) = F(0) + sum(nums) - n * nums[n-1].

For general k, the element that was at index n-k in nums becomes the last removed-from-weight element, so:
F(k) = F(k-1) + sum(nums) - n * nums[n-k]

This gives an O(n) algorithm: compute sum and F(0), then iterate k = 1..n-1 updating current F and tracking max.

Time complexity: O(n). Space complexity: O(1) extra. Works with negatives; Python ints avoid overflow issues.

## Attempted solution(s)
```python
class Solution:
    def maxRotateFunction(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0

        total = sum(nums)
        # F(0)
        f0 = sum(i * num for i, num in enumerate(nums))
        max_f = f0
        curr = f0

        # Use recurrence: F(k) = F(k-1) + total - n * nums[n-k]
        # iterate k = 1..n-1
        for k in range(1, n):
            # nums[n-k] is the element that was at index n-k in original,
            # which becomes the element that gets "moved" out of high-weight positions.
            curr = curr + total - n * nums[n - k]
            if curr > max_f:
                max_f = curr

        return max_f
```
- Notes:
  - Approach: compute F(0) and total sum once, then use the derived recurrence F(k) = F(k-1) + total - n * nums[n-k] to update in O(1) per rotation.
  - Time complexity: O(n) to compute sum, F(0), and iterate through n-1 updates.
  - Space complexity: O(1) extra (excluding input).
  - Works for negative numbers and large n. The problem statement guarantees the answer fits in 32-bit integer, but Python's int handles larger values safely.