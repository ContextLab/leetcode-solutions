# https://leetcode.com/problems/longest-balanced-subarray-ii/description/?envType=daily-question

## Initial thoughts (stream-of-consciousness)
We need the longest contiguous subarray where the number of distinct even numbers equals the number of distinct odd numbers. Distinctness makes this harder than simple parity counts because repeated occurrences of the same value don't increase the distinct count.

A natural idea is a sliding window: keep counts of each value in the current window and also track how many distinct evens and distinct odds are present. As we move the right pointer, if a value appears for the first time in the window, it increments the appropriate distinct counter. If we move the left pointer and remove the last occurrence of a value, it decrements the corresponding distinct counter.

We want windows where distinct_even == distinct_odd. Sliding-window can enumerate windows while maintaining distinct counts. The main question: does a standard two-pointer scheme (expand right, shrink left when needed) find the global maximum? For many window properties the two-pointer technique works because the property is monotone when expanding; here equality is not monotone, but for each fixed right endpoint the process of advancing left until the window becomes "balanced" (if possible) will find the longest balanced window ending at that right — because advancing left only removes values (monotone in length) and we can check when distinct_even == distinct_odd. So scanning right from 0..n-1 and shrinking left when needed while maintaining counts will enumerate candidate maximal-length balanced windows (one per right) and keep the global maximum.

This yields an O(n) two-pointer solution with O(n) auxiliary memory (for counts).

## Refining the problem, round 2 thoughts
- We'll maintain:
  - cnt: dict mapping value -> its count within current window [l..r]
  - distinct_even and distinct_odd: number of distinct evens/odds with count > 0 in window
- For r from 0..n-1:
  - increment cnt[nums[r]]
  - if cnt becomes 1: increment the correct distinct counter
  - Then try to shrink left while distinct_even > distinct_odd or distinct_odd > distinct_even? We can shrink while difference != 0 to try to find a balanced window ending at r. But care: if we always shrink until equal, we might shrink too far in some situations where equality could have been achieved with a smaller shrink. However shrinking is monotone in length; we want the longest balanced window ending at r which corresponds to the smallest l such that distinct counts are equal. Starting from previous l (which is minimal for previous r), repeatedly advancing r and shrinking l until equality will find that smallest l for current r. Each index will be removed at most once, so overall O(n).
- Edge cases: entire array might be balanced; arrays with only even or only odd distinct numbers will never be balanced (answer 0 or maybe 0? but constraint says subarray nonempty, but if no balanced subarray exists the longest length is 0 — confirm by examples/description: they don't say answer >=1; returning 0 is reasonable).
- Complexity: each element enters and leaves window at most once => O(n) time; space is O(n) for dict.

I'll implement this sliding-window approach.

## Attempted solution(s)
```python
from collections import defaultdict

class Solution:
    def longestBalancedSubarray(self, nums: list[int]) -> int:
        n = len(nums)
        cnt = defaultdict(int)
        distinct_even = 0
        distinct_odd = 0
        l = 0
        ans = 0

        for r, x in enumerate(nums):
            cnt[x] += 1
            if cnt[x] == 1:
                if x % 2 == 0:
                    distinct_even += 1
                else:
                    distinct_odd += 1

            # Shrink left while we can make progress toward balance.
            # We try to move l forward as long as moving it does not skip a possible longer balanced window ending at r.
            # We advance l while the current window is unbalanced and moving l might help (we simply keep shrinking until either balanced or l passes r).
            while l <= r and distinct_even != distinct_odd:
                y = nums[l]
                cnt[y] -= 1
                if cnt[y] == 0:
                    if y % 2 == 0:
                        distinct_even -= 1
                    else:
                        distinct_odd -= 1
                l += 1

            # If balanced, update answer. Note: after the while loop, either l > r or distinct_even == distinct_odd.
            if distinct_even == distinct_odd:
                # window is [l..r]
                length = r - l + 1
                if length > ans:
                    ans = length

        return ans
```
- Notes about the approach:
  - We maintain counts of values in the current window and distinct counters for even/odd. As we move right, new first-time values increment the respective distinct counter. We then move left forward until the window becomes balanced (distinct_even == distinct_odd) or the window empties.
  - Each index enters the window once (when r increases) and leaves the window at most once (when l increases), so each update to cnt is O(1) and total time is O(n). Space is O(n) for the counts dictionary.
  - Time complexity: O(n). Space complexity: O(n) worst case (number of distinct values).
  - Implementation detail: returning 0 if no balanced subarray exists.