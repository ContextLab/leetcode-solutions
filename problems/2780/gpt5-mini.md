# [Problem 2780: Minimum Index of a Valid Split](https://leetcode.com/problems/minimum-index-of-a-valid-split/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the smallest index i (0 <= i < n-1) where both left and right subarrays have the same dominant element. The whole array is guaranteed to have exactly one dominant element (occurs > n/2). So that global dominant is a natural candidate for being dominant on both sides. If some split is valid, the dominant element for both sides must be the global dominant (because a dominant in a subarray must also be the global dominant if it's dominant on both sides — but more directly, problem statement guarantees a unique global dominant so we should check splits for that value).

So plan: find the global dominant element first (Boyer–Moore majority vote or hash counts). Then count its total occurrences. Iterate from left to right, maintaining how many of that value are in the left prefix. For each split at i, left length = i+1, right length = n-i-1. Check if left_count * 2 > left_len AND (total_count - left_count) * 2 > right_len. Return the first i that satisfies both. If none, return -1.

Edge cases: small n (no valid split if n == 1), candidate verification (though the problem guarantees one exists, but still safe to verify). Using Boyer-Moore gives O(n) time and O(1) extra space.

## Refining the problem, round 2 thoughts
Refinements:
- Even though the problem guarantees a dominant element exists, I'll still use Boyer–Moore then count to get the total occurrences to be robust.
- No need to store a prefix array; maintain left_count incrementally while scanning once more.
- Complexity: one pass to find candidate, one pass to count total, one pass to find split — but candidate finding and counting could be combined (two passes). We can do candidate (pass1), count total (pass2) and scanning for split (pass3) while maintaining left_count — effectively three linear passes but still O(n) time and O(1) extra space.
- Alternatively, we could get counts via a hashmap in one pass, but that uses O(n) extra space unnecessarily.
- Make sure to check only i up to n-2.

Corner cases:
- If the candidate isn't actually > n/2 (shouldn't happen per constraints), return -1.
- If n == 1, immediately -1 because no valid split range.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumIndex(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 1:
            return -1

        # 1) Boyer-Moore to find majority candidate
        candidate = None
        count = 0
        for x in nums:
            if count == 0:
                candidate = x
                count = 1
            elif candidate == x:
                count += 1
            else:
                count -= 1

        # 2) Count total occurrences of candidate to verify and get total_count
        total_count = 0
        for x in nums:
            if x == candidate:
                total_count += 1

        # Verify (problem guarantees this, but be safe)
        if total_count * 2 <= n:
            return -1

        # 3) Scan and maintain left_count to check splits
        left_count = 0
        for i, x in enumerate(nums):
            if x == candidate:
                left_count += 1
            left_len = i + 1
            right_len = n - left_len
            # Only consider valid split indices i < n-1
            if i < n - 1:
                right_count = total_count - left_count
                if left_count * 2 > left_len and right_count * 2 > right_len:
                    return i

        return -1
```
- Approach: Find the global dominant using Boyer–Moore majority vote, count its total occurrences, then scan left-to-right maintaining the count of dominant in the prefix and check the dominance condition on both sides for each split.
- Time complexity: O(n) — a few linear passes but all linear.
- Space complexity: O(1) extra space (excluding input).