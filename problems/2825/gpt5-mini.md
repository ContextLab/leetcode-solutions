# [Problem 2825: Make String a Subsequence Using Cyclic Increments](https://leetcode.com/problems/make-string-a-subsequence-using-cyclic-increments/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can perform one operation: pick any set of indices in str1 and increment those characters by one (cyclically). Doing the operation "at most once" just means we may choose to increment some positions (possibly none) exactly once. For each position in str1, after that operation the character is either the original or original+1 (with wrap z->a). So effectively each position can supply either of two characters.

We want str2 to be a subsequence of the resulting string. That suggests a simple greedy scan: walk str1 and try to match characters of str2 in order; at each position of str1 we can match either the original char or its incremented char. If either matches the current needed character in str2, we consume that character and move on. If we reach the end of str2, return True. If we finish str1 without matching all of str2, return False.

I should check if there is any coupling between choices at different indices that could break a greedy approach. But choices are independent (we can pick any subset to increment), so greedily matching earliest possible of str2 is safe.

## Refining the problem, round 2 thoughts
- Edge cases:
  - str2 already a subsequence of str1 (no increments needed) — greedy handles this.
  - Characters may wrap: 'z' increments to 'a' — include modulo logic.
  - Large lengths up to 1e5 — need O(n) time and O(1) extra space.
- Alternative ideas (unnecessary here): modeling as bipartite matching or DP is overkill because of independence per position.
- Complexity: single pass over str1 with pointer over str2 gives O(len(str1) + len(str2)) time (effectively O(len(str1)) since we only move j forward up to len(str2)) and O(1) extra space.

## Attempted solution(s)
```python
class Solution:
    def canMakeSubsequence(self, str1: str, str2: str) -> bool:
        i = 0  # pointer for str1
        j = 0  # pointer for str2
        n1 = len(str1)
        n2 = len(str2)
        while i < n1 and j < n2:
            c = str1[i]
            # compute incremented character (cyclic)
            inc = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
            if c == str2[j] or inc == str2[j]:
                j += 1
            i += 1
        return j == n2
```
- Notes:
  - We scan str1 once and try to greedily match str2 in order. For each str1[i], it can match either its original character or the incremented character.
  - Time complexity: O(n1 + n2) but practically O(n1) since j advances at most n2 times.
  - Space complexity: O(1) additional space.
  - This works because increments are independent per position (we can choose any subset in the single allowed operation), so there is no interference between different matching choices.