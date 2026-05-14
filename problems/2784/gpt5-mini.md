# [Problem 2784: Check if Array is Good](https://leetcode.com/problems/check-if-array-is-good/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to determine if nums is a permutation of base[n] = [1,2,...,n-1,n,n] for some n. The obvious candidate n is the maximum element in nums because base[n] contains n (and no element greater than n). For base[n] the length is n+1, so if len(nums) != max(nums) + 1 we can immediately return False. If the length matches, we must ensure that every integer from 1..n-1 appears exactly once and n appears exactly twice. Counting occurrences (Counter or array of counts) seems simplest. Alternatively, sort and check sequence, but counting is O(n) and clearer.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- If max(nums) = n, require len(nums) == n+1, otherwise false.
- Use a Counter to verify counts: counts[n] == 2 and for all i in 1..n-1 counts[i] == 1.
- If any number > n would change n, but we use max so that's handled implicitly; numbers < 1 are out of constraints.
- Complexity: one pass to compute max and counts (or two passes: one for max, one for counts), overall O(m) where m = len(nums) and O(k) extra space for counts (k <= max(nums)).
- Alternative: using a boolean seen set while checking counts could early-fail on duplicates/missing elements.

This is an easy problem; implement straightforwardly and return early when possible.

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def isGood(self, nums: list[int]) -> bool:
        if not nums:
            return False

        n = max(nums)
        # base[n] has length n + 1
        if len(nums) != n + 1:
            return False

        cnt = Counter(nums)
        # n must appear exactly twice
        if cnt.get(n, 0) != 2:
            return False

        # each number from 1 to n-1 must appear exactly once
        for x in range(1, n):
            if cnt.get(x, 0) != 1:
                return False

        return True
```
- Notes:
  - Approach: determine candidate n = max(nums); check length == n+1; use Counter to verify counts: n appears twice, each i in [1..n-1] appears once.
  - Time complexity: O(m) where m = len(nums) (computing max and counting).
  - Space complexity: O(k) for the Counter where k is the number of distinct values (<= m, and <= max(nums)).
  - Implementation details: early returns on length mismatch and wrong counts make this efficient for all valid inputs.