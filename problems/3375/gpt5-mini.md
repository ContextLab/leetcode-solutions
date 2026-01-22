# [Problem 3375: Minimum Operations to Make Array Values Equal to K](https://leetcode.com/problems/minimum-operations-to-make-array-values-equal-to-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can only decrease numbers (operation sets nums[i] > h to h). A chosen h is valid only if all elements strictly greater than h are identical. That suggests we can only operate on the current maximum value(s) (or a single distinct top value) at a time. If there are two different values above some h, that h is invalid because the set of elements > h would contain multiple distinct values.

Also, since operations never increase values, if any element is < k initially, it's impossible to reach k for that element. If all elements are already k, answer is 0.

It seems natural that each distinct value strictly greater than k must be "collapsed" at least once (reduced) through operations. So count distinct values > k.

## Refining the problem, round 2 thoughts
- If any nums[i] < k -> impossible -> return -1.
- Consider the distinct values greater than k, sorted descending v1 > v2 > ...; we can pick h = v2 to reduce all v1 to v2 (valid because elements > v2 are exactly those equal to v1). Repeat until everything above k is reduced down step by step. Each distinct value > k requires one operation to eliminate (merge) it into the next lower value (eventually to k).
- Thus the minimal number of operations equals the number of distinct values strictly greater than k.
- Complexity: we just need to scan the array, check for any < k, and build a set of values > k. O(n) time, O(U) space where U <= 100 due to value bounds.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        # If any element is less than k, we can never increase it -> impossible
        for v in nums:
            if v < k:
                return -1
        # Count distinct values strictly greater than k
        greater = {v for v in nums if v > k}
        return len(greater)
```
- Notes:
  - Correctness: An operation can only validly target the current maximum distinct value(s). You can reduce the current maximum value to the next distinct value (or to k) in one valid operation. Therefore each distinct value > k must be removed at least once; doing so in descending order achieves this optimally.
  - Time complexity: O(n) to scan nums and build the set.
  - Space complexity: O(U) for the set of distinct values > k (U <= min(n, 100) given constraints).