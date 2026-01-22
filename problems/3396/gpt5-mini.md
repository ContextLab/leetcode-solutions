# [Problem 3396: Minimum Number of Operations to Make Elements in Array Distinct](https://leetcode.com/problems/minimum-number-of-operations-to-make-elements-in-array-distinct/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can only remove elements from the beginning and each operation removes 3 elements (or all remaining if fewer than 3). After k operations the array is just the suffix starting at index 3*k (or empty if 3*k >= n). So for a given number of operations k, the resulting array is nums[3*k:]; we need that suffix to have all distinct elements.

Thus the problem reduces to: find the smallest k >= 0 such that nums[3*k:] has no duplicates. Because n <= 100, it's fine to try k = 0,1,2,... until we find one that works (or until we remove the whole array). Checking distinctness can be done with a set. This is straightforward and efficient enough.

## Refining the problem, round 2 thoughts
Edge cases:
- The array is already distinct -> answer is 0.
- We might need to remove the whole array -> answer is ceil(n/3).

Alternative way: for each possible start index s (0..n), check if suffix nums[s:] is distinct; if so answer is ceil(s/3). But iterating k directly (k from 0..ceil(n/3)) is simpler and clearer.

Time complexity: For each k we check distinctness of up to O(n) elements using a set; we try up to O(n/3) values of k, so worst-case O(n^2) time. Space complexity: O(n) for the set.

This is fine for n <= 100.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        max_ops = (n + 2) // 3  # ceil(n/3)
        for ops in range(max_ops + 1):
            start = ops * 3
            # If we've removed all elements, array is empty -> distinct
            if start >= n:
                return ops
            suffix = nums[start:]
            if len(set(suffix)) == len(suffix):
                return ops
        # Should never reach here because removing all elements always works
        return max_ops
```
- Approach: Try increasing number of operations ops = 0..ceil(n/3). After ops operations the array becomes nums[3*ops:]. Check if that suffix has all distinct elements using a set; if yes, return ops. If 3*ops >= n the array is empty and thus distinct.
- Time complexity: O(n^2) in the worst case (n <= 100 so it's fine).
- Space complexity: O(n) for the set used to check distinctness.