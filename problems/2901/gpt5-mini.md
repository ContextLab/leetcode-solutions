# [Problem 2901: Longest Unequal Adjacent Groups Subsequence II](https://leetcode.com/problems/longest-unequal-adjacent-groups-subsequence-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the longest subsequence of indices in original order such that each adjacent pair (j, i) in the subsequence:
- have different groups,
- words have equal length,
- hamming distance between the two words is exactly 1.

This sounds like a longest-increasing-subsequence (by index) variant with constraints on valid transitions. A straightforward dynamic programming approach: dp[i] = length of longest valid subsequence ending at index i; for each j < i, if transition j -> i is allowed (groups differ, equal length, hamming distance == 1) then dp[i] = max(dp[i], dp[j] + 1). Keep parent pointers to reconstruct one longest sequence. n is up to 1000 and words length <= 10, so O(n^2 * L) with L <= 10 is fine.

## Refining the problem, round 2 thoughts
- We must preserve original order (subsequence), so only consider j < i for transitions.
- Hamming distance check can early-exit when >1 differences to keep it efficient.
- Words are distinct, so dp base is 1 for any single element.
- Edge cases: all words different lengths → answer is any single word; many valid answers if multiple longest subsequences exist — return any.
- Minor optimizations: bucket indices by word length and only compare indices with same length. Worst-case (all same length) still O(n^2), but this avoids needless length checks across different sizes.
- Complexity: time O(n^2 * L) and space O(n).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestSubsequence(self, words: List[str], groups: List[int]) -> List[str]:
        n = len(words)
        # dp[i] = length of longest valid subsequence ending at i
        dp = [1] * n
        parent = [-1] * n

        def hamming_is_one(a: str, b: str) -> bool:
            # assumes len(a) == len(b)
            diff = 0
            for x, y in zip(a, b):
                if x != y:
                    diff += 1
                    if diff > 1:
                        return False
            return diff == 1

        for i in range(n):
            for j in range(i):
                if groups[j] != groups[i] and len(words[j]) == len(words[i]):
                    if hamming_is_one(words[j], words[i]):
                        if dp[j] + 1 > dp[i]:
                            dp[i] = dp[j] + 1
                            parent[i] = j

        # find index with maximum dp value
        best_idx = max(range(n), key=lambda x: dp[x])

        # reconstruct subsequence of words
        res = []
        cur = best_idx
        while cur != -1:
            res.append(words[cur])
            cur = parent[cur]
        res.reverse()
        return res
```
- Approach: Classic DP for longest subsequence with transition allowed only when groups differ, lengths equal and hamming distance exactly 1. Parent pointers used to reconstruct one valid maximum-length subsequence.
- Time complexity: O(n^2 * L) where n = len(words) (≤1000) and L = max word length (≤10). In practice ~10^7 character comparisons worst-case, which is fine.
- Space complexity: O(n) for dp and parent arrays.