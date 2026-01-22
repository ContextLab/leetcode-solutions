# [Problem 3330: Find the Original Typed String I](https://leetcode.com/problems/find-the-original-typed-string-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count how many different original strings could have produced the final displayed word if Alice may have "long-pressed" (pressed too long and produced extra repeated characters) at most once. The final word consists of runs of identical characters. If a run has length k, the intended count for that run could be any value from 1 to k, but only one run (at most) can have been affected by a long press (i.e., be larger in the final output than intended). If no long press happened at all, the intended string is exactly the final word.

So possible original strings = 1 (no long press) + sum over runs of how many smaller intended counts that run could have had (k-1 for a run of length k). That simplifies to 1 + sum(k_i - 1) = 1 + (total length) - (number of runs).

## Refining the problem, round 2 thoughts
Edge cases:
- Single-character word: groups = 1, length = n, formula still works.
- All characters different: each run length = 1, sum(k_i-1) = 0 -> only 1 possible original (no long press).
- All same character: one run, answer = 1 + n - 1 = n (we can have intended counts 1..n).

Time complexity: need a single pass to count number of runs and length (length is given). O(n) time and O(1) extra space.

## Attempted solution(s)
```python
class Solution:
    def countPossibleOriginals(self, word: str) -> int:
        """
        Return the number of possible original intended strings that could have
        produced 'word' if Alice may have long-pressed at most one key.
        """
        n = len(word)
        # count number of consecutive-character groups
        groups = 1  # word length >= 1 by constraints
        for i in range(1, n):
            if word[i] != word[i - 1]:
                groups += 1
        # formula: 1 (no long press) + sum(k_i - 1) = 1 + n - groups
        return 1 + n - groups
```
- Notes:
  - Approach: count consecutive-character groups and apply the derived formula 1 + n - groups.
  - Time complexity: O(n), where n = len(word).
  - Space complexity: O(1) extra space.