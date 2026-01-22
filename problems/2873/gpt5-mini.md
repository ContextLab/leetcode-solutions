# [Problem 2873: Maximum Value of an Ordered Triplet I](https://leetcode.com/problems/maximum-value-of-an-ordered-triplet-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We want the maximum value of (nums[i] - nums[j]) * nums[k] with i < j < k. A brute force triple loop is straightforward but O(n^3) and unnecessary since n ≤ 100 (brute force might pass but we can do better).

Observations:
- nums values are positive (>= 1), so nums[k] is always positive. That means the sign of the product is determined entirely by (nums[i] - nums[j]).
- For a fixed j, to maximize (nums[i] - nums[j]) we should pick the largest nums[i] with i < j.
- For a fixed j, to maximize the overall product we should also pick the largest nums[k] with k > j.
So for each j we can use the maximum to the left and maximum to the right, compute the value and take the best.

## Refining the problem, round 2 thoughts
Refinement and edge cases:
- For each j in range 1..n-2 (so there is at least one i before and one k after), we need max_left = max(nums[0..j-1]) and max_right = max(nums[j+1..n-1]).
- Compute prefix maximums and suffix maximums in O(n) time to get those quickly.
- Compute value = (max_left - nums[j]) * max_right. If this value is negative, final answer should be at least 0 per problem statement, so we'll track the maximum and finally return max(0, best).
- Time complexity O(n), space O(n) (can be O(1) if we compute suffix maximums on the fly, but O(n) is fine and simple).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumTripletValue(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 3:
            return 0

        # prefix_max[i] = max(nums[0..i])
        prefix_max = [0] * n
        prefix_max[0] = nums[0]
        for i in range(1, n):
            prefix_max[i] = max(prefix_max[i-1], nums[i])

        # suffix_max[i] = max(nums[i..n-1])
        suffix_max = [0] * n
        suffix_max[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            suffix_max[i] = max(suffix_max[i+1], nums[i])

        best = float('-inf')
        # j must be between 1 and n-2 inclusive so there exists i < j and k > j
        for j in range(1, n-1):
            max_left = prefix_max[j-1]
            max_right = suffix_max[j+1]
            val = (max_left - nums[j]) * max_right
            if val > best:
                best = val

        return max(0, best)
```
- Approach: Precompute prefix maximums and suffix maximums so for each middle index j we can in O(1) get the best i and k choices (largest nums[i] before j and largest nums[k] after j). Compute the value for each j and take the maximum, finally clamp to 0 if all are negative.
- Time complexity: O(n) to build prefix/suffix arrays and O(n) to evaluate j's, so O(n) total.
- Space complexity: O(n) for prefix_max and suffix_max (can be reduced to O(1) with a different scanning strategy).