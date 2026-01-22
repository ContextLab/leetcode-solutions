# [Problem 2779: Maximum Beauty of an Array After Applying Operation](https://leetcode.com/problems/maximum-beauty-of-an-array-after-applying-operation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want the longest subsequence of equal elements after changing each element at most once within ±k. For a chosen target value x, an index i can contribute to a subsequence of x if x lies in [nums[i]-k, nums[i]+k]. So each element defines an interval of possible x values. The problem becomes: choose an integer x that lies in the maximum number of these intervals. That's the classic "maximum overlap of intervals" problem. I can sweep over interval endpoints (or use events +1 at left, -1 after right) to find the maximum coverage. Complexity should be O(n log n) due to sorting events.

## Refining the problem, round 2 thoughts
- Each nums[i] gives interval [nums[i]-k, nums[i]+k]. Intervals are inclusive. To handle integer points cleanly, I can add +1 at left and -1 at (right + 1) so that integer coverage counting is correct.
- Edge cases: k = 0 (intervals are points) reduces to finding mode frequency. Negative left endpoints are fine — events can be keyed by negatives.
- Values stay small enough: nums[i] and k up to 1e5, so endpoints are within about [-1e5, 2e5].
- Implementation detail: use a dict (collections.defaultdict) to store events, then iterate sorted keys accumulating current coverage and track max.
- Time: O(n log n) for sorting event keys. Space: O(n) for events.

## Attempted solution(s)
```python
from typing import List
from collections import defaultdict

class Solution:
    def maximumBeauty(self, nums: List[int], k: int) -> int:
        events = defaultdict(int)
        # For each element, it contributes +1 to any integer x in [a-k, a+k].
        # Use +1 at left, -1 at right+1 to count integer coverage.
        for a in nums:
            left = a - k
            right = a + k
            events[left] += 1
            events[right + 1] -= 1

        cur = 0
        ans = 0
        for x in sorted(events):
            cur += events[x]
            if cur > ans:
                ans = cur
        return ans
```
- Approach: Convert each nums[i] into an interval [nums[i]-k, nums[i]+k]. Use difference-array / sweep-line technique with events: +1 at left, -1 at right+1. Sort event keys and sweep to find the maximum overlap, which is the maximum number of elements that can be made equal to the same x.
- Time complexity: O(n log n) due to sorting the distinct event keys (at most 2n keys).
- Space complexity: O(n) to store events.