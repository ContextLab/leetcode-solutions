# [Problem 3432: Count Partitions with Even Sum Difference](https://leetcode.com/problems/count-partitions-with-even-sum-difference/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want to count partition indices i (0 <= i < n-1) where difference between sum(left) and sum(right) is even. Let total sum be S and left sum be L. Difference = L - (S - L) = 2L - S. 2L is always even, so whether 2L - S is even depends only on S's parity. If S is even, 2L - S is even for any L; if S is odd, 2L - S is odd for any L. So the property doesn't depend on where we split except via total S.

## Refining the problem, round 2 thoughts
Thus the answer is either all possible partitions (n-1) when total sum S is even, or 0 when S is odd. Edge cases: n >= 2 guaranteed, so n-1 >= 1. Complexity: we only need to compute the total sum O(n) time and O(1) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countPartitions(self, nums: List[int]) -> int:
        """
        Return number of valid partition indices where difference between
        left and right subarray sums is even.
        """
        total = sum(nums)
        return (len(nums) - 1) if (total % 2 == 0) else 0
```
- Notes:
  - Approach: Use parity observation: difference = 2L - S, which is even iff S is even.
  - Time complexity: O(n) to compute the sum.
  - Space complexity: O(1) extra space.