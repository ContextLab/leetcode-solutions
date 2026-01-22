# [Problem 2221: Find Triangular Sum of an Array](https://leetcode.com/problems/find-triangular-sum-of-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share internal stream-of-consciousness or chain-of-thought. Instead, here is a concise summary of the initial reasoning and approach:
- The process repeatedly replaces the array with pairwise sums mod 10 until one element remains.
- A straightforward simulation reduces the array length by 1 each step and is simple to implement.
- This simulation can be done in-place in the input array to use O(1) extra space and runs in O(n^2) time, which is acceptable for n <= 1000.

## Refining the problem, round 2 thoughts
- Edge cases: array length 1 should return that element unchanged.
- Two main approaches:
  1. Direct simulation (in-place): repeatedly compute nums[i] = (nums[i] + nums[i+1]) % 10 for i from 0 to current_length-2, then shorten the considered length. Simpler and O(n^2) time, O(1) extra space.
  2. Combinatorial: triangular sum equals sum_{i=0..n-1} C(n-1, i) * nums[i] (mod 10). Computing binomial coefficients modulo 10 is trickier because 10 is composite; computing Pascal's triangle coefficients and applying mod 10 also results in O(n^2) time and similar complexity.
- Given constraints (n <= 1000), the in-place simulation is clear, easy, and efficient enough.

## Attempted solution(s)
```python
class Solution:
    def triangularSum(self, nums: list[int]) -> int:
        """
        Compute the triangular sum by simulating the process in-place.
        Time: O(n^2), Space: O(1) extra (modifies input array).
        """
        n = len(nums)
        # If only one element, return it directly
        if n == 1:
            return nums[0]
        # We will shrink the active length `m` from n down to 1
        m = n
        while m > 1:
            # Update elements 0..m-2 using their current next neighbor
            for i in range(m - 1):
                nums[i] = (nums[i] + nums[i + 1]) % 10
            m -= 1
        return nums[0]
```
- Notes:
  - The implementation updates the array in-place from index 0 up to the active length - 2 each iteration, then decreases the active length m by 1. This avoids creating new arrays and uses constant extra memory.
  - Time complexity: O(n^2) because the outer loop runs n-1 times and the inner loop runs up to O(n) steps in early iterations.
  - Space complexity: O(1) extra space (not counting the input array), since updates are done in-place.
  - This approach is straightforward, simple to reason about, and fits the problem constraints.