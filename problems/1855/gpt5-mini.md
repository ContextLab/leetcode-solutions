# [Problem 1855: Maximum Distance Between a Pair of Values](https://leetcode.com/problems/maximum-distance-between-a-pair-of-values/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum j - i such that i <= j and nums1[i] <= nums2[j]. Both arrays are non-increasing (i.e., non-increasing / descending or equal). For a fixed i, the set of j with nums2[j] >= nums1[i] is a prefix (from 0 up to some last valid index t) because nums2 is non-increasing; once nums2[j] < nums1[i] for some j, it will be < for all larger j. We also require j >= i, so for each i we want the largest j >= i that still satisfies nums2[j] >= nums1[i]. Since nums1 is non-increasing, nums1[i] gets smaller (or equal) as i increases, so the last valid j (t) will not move left when i increases — t is non-decreasing. That suggests a two-pointer approach walking i from 0 up and j only moving forward.

## Refining the problem, round 2 thoughts
Two-pointer approach:
- Initialize j = 0.
- For each i in 0..len(nums1)-1:
  - Ensure j >= i (set j = max(j, i)) because pairs require i <= j.
  - Advance j while j + 1 < len(nums2) and nums2[j+1] >= nums1[i] (we try to push j to the right as far as nums2 keeps meeting the condition).
  - If nums2[j] >= nums1[i], compute distance j - i and update answer.
This runs in O(n1 + n2) because j never moves left and each pointer moves at most its array length. Edge cases: if j ends up < i or nums2[j] < nums1[i], no valid pair for that i. If no valid pair ever, return 0.

Alternative is binary search on nums2 for every i (search last j with nums2[j] >= nums1[i]); that would be O(n1 * log n2), still acceptable but two-pointer is simpler and linear.

Space O(1) extra.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxDistance(self, nums1: List[int], nums2: List[int]) -> int:
        n1, n2 = len(nums1), len(nums2)
        j = 0
        ans = 0
        for i in range(n1):
            if j < i:
                j = i  # ensure j >= i
            # move j as far right as possible while maintaining nums2[j] >= nums1[i]
            while j + 1 < n2 and nums2[j + 1] >= nums1[i]:
                j += 1
            # check current j
            if j < n2 and nums2[j] >= nums1[i]:
                ans = max(ans, j - i)
            # if j == n2 - 1 and nums2[j] < nums1[i], further i will have nums1[i] <= previous value,
            # but since nums1 is non-increasing, future nums1 might be smaller making condition possible;
            # so we cannot break early based only on this.
        return ans
```
- Approach: Two-pointer scanning. For each i in nums1 we push j (in nums2) forward as much as possible while keeping nums2[j] >= nums1[i] and ensuring j >= i. Because both arrays are non-increasing, j never needs to move left; complexity is linear.
- Time complexity: O(n1 + n2) — each pointer moves forward at most the length of its array.
- Space complexity: O(1) extra space.
- Implementation notes: We set j = max(j, i) to satisfy the i <= j condition. The while loop advances j to the right while the condition nums2[j+1] >= nums1[i] holds. After updating answer if valid, continue to next i. This handles all edge cases (including when no valid pair exists — we return 0).