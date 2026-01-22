# [Problem 2900: Longest Unequal Adjacent Groups Subsequence I](https://leetcode.com/problems/longest-unequal-adjacent-groups-subsequence-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the longest subsequence of words such that for any two consecutive chosen words, their group bits differ (no two consecutive 0s or 1s). Because groups are binary (0/1), this is essentially choosing a subsequence of indices whose group values alternate.

This looks like a simple greedy: scan left-to-right and pick an element whenever its group differs from the last picked group's value. Intuitively picking earlier elements can't hurt because earlier picks give more opportunities to alternate later. So start from the first element and take every index that flips the group bit relative to the last chosen one.

We should confirm no tricky cases where skipping an early element helps you get a longer alternating chain later — but with only two values, taking the earliest instance of a value only increases future choices, never reduces them.

So algorithm: pick words[0], last_group = groups[0]; for i from 1..n-1: if groups[i] != last_group: append words[i], last_group = groups[i]. Return the built list.

## Refining the problem, round 2 thoughts
- Edge cases: n >= 1 per constraints, so we always pick at least one word.
- If all groups are the same, the longest alternating subsequence length is 1 (we pick any single word; picking the first is fine).
- Complexity: single pass O(n) time, O(n) extra space for the result (worst-case when it alternates every position). Memory besides input is O(n) for the output.
- This greedy is optimal because whenever you choose an element earlier when possible, you don't prevent any future valid picks — you only allow more potential alternations. There are only two possible values, so you never gain by skipping a possible flip.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestAlternatingSubsequence(self, words: List[str], groups: List[int]) -> List[str]:
        """
        Greedy: pick the first word, then whenever groups[i] differs from the last picked group,
        pick words[i]. This yields the longest alternating subsequence.
        """
        n = len(words)
        if n == 0:
            return []
        res = [words[0]]
        last = groups[0]
        for i in range(1, n):
            if groups[i] != last:
                res.append(words[i])
                last = groups[i]
        return res
```
- Notes: The solution scans the arrays once. Time complexity O(n), space complexity O(n) for the returned subsequence in the worst case. The greedy choice of always taking the first available differing group is optimal because groups are binary and earlier picks never reduce future possibilities for alternation.