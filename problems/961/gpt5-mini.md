# [Problem 961: N-Repeated Element in Size 2N Array](https://leetcode.com/problems/n-repeated-element-in-size-2n-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have an array of length 2n with n+1 unique elements and exactly one value appears n times. That means one value is very frequent (half the array). The simplest idea is to scan and track seen values in a set or map; the first value we encounter twice must be the repeated one. There's also a known trick: because the repeated value occurs so often, two of its occurrences must be very close (distance 1 or 2), so checking adjacent or near-adjacent elements can also find it in O(1) extra space. But the straightforward O(n) time + O(n) space with a set is simple and safe.

## Refining the problem, round 2 thoughts
Edge cases: smallest n is 2 so length 4 — still fine. The set approach: iterate through nums, if a number already in set return it, otherwise add to set. This works because there is exactly one element repeated n times, so the first duplicate encountered must be that element. Time O(n), space O(n).

Alternative (O(1) space) approach: check for any i if nums[i] == nums[i+1] or nums[i] == nums[i+2] (also check nums[i+1] == nums[i+2]) — because with frequency n in 2n array, by pigeonhole there must be a pair of repeated entries within distance 2. That yields O(n) time, O(1) space. But I'll provide the clear set-based solution (and mention the neighbor-check trick).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def repeatedNTimes(self, nums: List[int]) -> int:
        seen = set()
        for x in nums:
            if x in seen:
                return x
            seen.add(x)
        # Given problem constraints, we should always return inside loop.
        # Return a fallback (not strictly necessary).
        return -1
```
- Approach: iterate through the array maintaining a set of seen values; the first value encountered that is already in the set is the N-repeated element.
- Time complexity: O(n) where n = len(nums) (actually O(2N) = O(N) in problem terms).
- Space complexity: O(n) worst-case for the set (O(N) in problem terms).
- Implementation details: The problem guarantees an answer exists, so the function will always find and return it inside the loop.

Optional note: For O(1) extra space, you can scan and check neighbors for equality (nums[i]==nums[i+1] or nums[i]==nums[i+2]) which is guaranteed to find the repeated value as well.