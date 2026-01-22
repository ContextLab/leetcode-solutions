# [Problem 3346: Maximum Frequency of an Element After Performing Operations I](https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find the maximum number of elements that can be made equal to the same value after performing exactly numOperations operations, where each operation picks a distinct index and adds an integer in [-k, k]. Adding 0 is allowed (so performing an operation doesn't force a change). Each element a can be transformed to any value in [a-k, a+k] if we choose to operate on it. So for a chosen target T, any element with value in [T-k, T+k] can be made T by using at most one operation (0 if already T). Elements not in that interval cannot be turned into T.

Because operations must be applied on distinct indices and exactly numOperations times, but adding 0 is allowed, we can effectively treat this as "we can change at most numOperations elements to T (distinct indices)"; elements already equal to T count without consuming an operation if we don't pick them, but even if we pick them we can add 0. Thus total frequency for target T is number of elements already equal to T plus up to numOperations extra elements from those in [T-k, T+k] that are not already T. That simplifies to min(count_in_range(T), count_equal(T) + numOperations).

So it's about finding, over all integer targets T, the maximum between these expressions. The interval [T-k, T+k] is length 2k+1 on the value axis. We can compute counts with prefix sums over value frequencies.

## Refining the problem, round 2 thoughts
We only need to consider T values in the range of numbers present (1..max(nums)), since windows centered outside that range will not increase the count beyond windows inside. Build frequency array freq[v] for v in [1..maxV], compute prefix sums pref so count_in_range(T) = pref[min(maxV, T+k)] - pref[max(1, T-k)-1]. Then for each T in 1..maxV compute candidate = min(count_in_range, freq[T] + numOperations) and take max.

Edge cases:
- k = 0: no element can change to another value => answer is max frequency of any existing value.
- numOperations = 0: must not change any values => answer is max frequency of any existing value (same formula works).
- Large k that covers entire value span: count_in_range(T) will be n for any T, so answer is min(n, freq[T] + numOperations) and we take max over T; equivalently min(n, max_freq + numOperations).
Time complexity: building freq and prefix sums O(maxV + n). Scanning T from 1..maxV O(maxV). With maxV <= 1e5 this is fine. Space O(maxV).

## Attempted solution(s)
```python
from typing import List
import collections

class Solution:
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        if not nums:
            return 0
        n = len(nums)
        maxV = max(nums)
        # frequency array indexed 1..maxV
        freq = [0] * (maxV + 1)
        for a in nums:
            freq[a] += 1
        # prefix sums
        pref = [0] * (maxV + 1)
        running = 0
        for v in range(1, maxV + 1):
            running += freq[v]
            pref[v] = running
        def range_sum(l: int, r: int) -> int:
            if l > r:
                return 0
            l = max(l, 1)
            r = min(r, maxV)
            if l > r:
                return 0
            return pref[r] - (pref[l-1] if l-1 >= 0 else 0)
        ans = 0
        for T in range(1, maxV + 1):
            l = T - k
            r = T + k
            cnt_in_range = range_sum(l, r)
            cnt_equal = freq[T]
            # we can convert up to numOperations elements (distinct indices) to T,
            # but only those within [T-k, T+k]. So final freq is min(cnt_in_range, cnt_equal + numOperations).
            candidate = min(cnt_in_range, cnt_equal + numOperations)
            if candidate > ans:
                ans = candidate
            # early exit if we already can achieve all elements
            if ans == n:
                return n
        return ans
```
- Notes on approach:
  - Build frequency array and prefix sums over value axis (1..maxV).
  - For each candidate target T, compute the number of elements whose values lie within [T-k, T+k] and the number already equal to T. The best achievable frequency for T is min(count_in_range, count_equal + numOperations).
  - Time complexity: O(n + maxV). Space complexity: O(maxV).
  - This solution works within constraints since maxV <= 1e5 and n <= 1e5.