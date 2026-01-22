# [Problem 2845: Count of Interesting Subarrays](https://leetcode.com/problems/count-of-interesting-subarrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count subarrays where the number of indices i in the subarray with nums[i] % modulo == k has its count cnt satisfying cnt % modulo == k. That screams reduction to a 0/1 array: mark an element as 1 if nums[i] % modulo == k, otherwise 0. Then cnt is just the sum of that segment. We want (sum over segment) % modulo == k.

This is a standard prefix-sum + frequency-of-remainders problem: for prefix sums S[], we need S[r+1] % modulo == (S[l] + k) % modulo, so S[l] % modulo == (S[r+1] - k) % modulo. So as we iterate prefixes we can count how many earlier prefixes had the required remainder. Use a hashmap for counts of prefix remainders. Note modulo can be large (up to 1e9) so use dict, not an array. Complexity O(n).

## Refining the problem, round 2 thoughts
Edge cases: modulo = 1 (then k must be 0) — every subarray qualifies; the method still works because remainders are all 0 and frequencies count combinations. We should be careful to use Python's modulo on negative numbers (Python's % yields non-negative result, so (curr - k) % modulo works fine).

We can avoid constructing a separate boolean list by computing the increment (0 or 1) on the fly. Initialize freq with remainder 0 seen once (empty prefix). For each element, update current prefix remainder, find target remainder (curr - k) % modulo and add freq[target] to answer, then increment freq[curr]. Time O(n), space O(min(n, modulo)) (at most n+1 distinct prefix remainders will be stored).

## Attempted solution(s)
```python
from typing import List
from collections import defaultdict

class Solution:
    def countInterestingSubarrays(self, nums: List[int], modulo: int, k: int) -> int:
        # freq maps prefix_sum % modulo -> count of prefixes seen
        freq = defaultdict(int)
        freq[0] = 1  # empty prefix
        curr = 0
        ans = 0
        for x in nums:
            # increment by 1 if this element matches the condition
            if x % modulo == k:
                curr = (curr + 1) % modulo
            # else curr remains same (adding 0)
            target = (curr - k) % modulo
            ans += freq.get(target, 0)
            freq[curr] += 1
        return ans
```
- Notes:
  - Approach: convert to implicit 0/1 by checking x % modulo == k, maintain prefix sum modulo `modulo`. For each prefix remainder `curr` (prefix ending at current index), the number of earlier prefixes with remainder `(curr - k) % modulo` gives the count of subarrays ending here that satisfy the condition.
  - Time complexity: O(n), where n = len(nums).
  - Space complexity: O(min(n, modulo)) for the hashmap of remainders (in practice O(n+1) distinct prefixes).
  - Implementation detail: use defaultdict(int) for cleaner counting and Python's modulo handles negative values correctly so `(curr - k) % modulo` yields the intended target remainder.