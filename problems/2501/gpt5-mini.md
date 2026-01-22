# [Problem 2501: Longest Square Streak in an Array](https://leetcode.com/problems/longest-square-streak-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need a subsequence which after sorting becomes a chain x, x^2, x^4, ... of length >= 2. Sorting requirement means the relative order in the original array doesn't matter — we only need the required values to exist in nums. So duplicates don't help unless they are distinct values in the chain. This suggests treating membership via a set.

A simple approach: for each distinct number x, follow the chain x -> x^2 -> x^4 ... as long as the next value exists in the set and count length. That gives the length of a square-streak starting at x. To avoid repeated work, memoize lengths for numbers already computed. Also can prune starts that are themselves squares of another number present (they will be covered when starting from the smaller root), but memoization already prevents duplicate work.

Be careful about large values when squaring repeatedly — Python handles big ints but membership checks will fail once the value exceeds any present numbers (since we check set membership).

## Refining the problem, round 2 thoughts
- Use set(nums) for O(1) membership. Use a dp dict mapping value -> length of chain starting at that value.
- For each distinct x not memoized, iterate repeatedly squaring while the value is in the set and not yet memoized, save the path, then backfill dp values for the path in reverse.
- Final answer is max(dp.values()), but we must return -1 if that max < 2.
- Time complexity: each distinct value is processed at most once in the path-building and then assigned a dp value; total work linear in number of distinct values and number of links between them. For nums[i] <= 1e5, chains are short.
- Space complexity: O(n) for set and dp.
- Edge cases: duplicates in input don't change existence; if no chain length >= 2 exists return -1.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestSquareStreak(self, nums: List[int]) -> int:
        nums_set = set(nums)
        dp = {}  # dp[x] = length of chain starting at x (including x)
        
        for x in nums_set:
            if x in dp:
                continue
            path = []
            cur = x
            # Walk forward while we have the number and haven't computed dp for it
            while cur in nums_set and cur not in dp:
                path.append(cur)
                cur = cur * cur
            # base is 0 if cur not in dp (meaning next doesn't exist), or dp[cur] if computed
            base = dp.get(cur, 0)
            # backfill dp for the path
            for v in reversed(path):
                base += 1
                dp[v] = base
        
        if not dp:
            return -1
        max_len = max(dp.values())
        return max_len if max_len >= 2 else -1
```
- Notes:
  - Approach: Build a set for membership, then for each distinct number follow its square-chain until a missing number or a previously computed dp value is reached. Backfill lengths for all nodes in the traversed path.
  - Time complexity: O(n) amortized over distinct values (each distinct value is visited/assigned once). Each step involves O(1) operations; chain lengths are short for the given constraints.
  - Space complexity: O(n) for the set and dp dictionary.
  - Implementation details: Using set ignores duplicates which do not affect existence checks; dp avoids recomputing overlapping chains. Return -1 if no chain of length >= 2 exists.