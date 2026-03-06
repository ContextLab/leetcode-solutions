# [Problem 1784: Check if Binary String Has at Most One Segment of Ones](https://leetcode.com/problems/check-if-binary-string-has-at-most-one-segment-of-ones/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check whether all the '1's in the binary string form a single contiguous block. The simplest observation: once a '0' appears after seeing '1's, there must not be any more '1's later. So I can scan and detect the first '0' (if any) and then check if there are any '1's after that point. Another quick pattern view: the string should look like 1*0* (some ones then some zeros); equivalently there must be no "01" substring (a 0 followed by a 1) after a 1 segment. A linear scan or simple string operations should be enough.

## Refining the problem, round 2 thoughts
Edge cases: the string could be all ones (no zeros) — that's valid. It could be "10" or "1" which are valid. A violating example is "101" or "1001" (ones separated by zeros). Two practical implementations:
- Find first '0' index and ensure no '1' appears after it.
- Or simply check that the substring "01" does not occur (since "01" signals a 0 followed by a later 1).
Both are O(n) time and O(1) extra space. Given constraints (n <= 100), either is fine. I'll implement the clear find-and-check approach for readability.

## Attempted solution(s)
```python
class Solution:
    def checkOnesSegment(self, s: str) -> bool:
        # find the first '0'
        zero_idx = s.find('0')
        # if there is no '0', all are ones -> valid
        if zero_idx == -1:
            return True
        # ensure there is no '1' after the first zero
        return '1' not in s[zero_idx+1:]
```
- Approach: Find the first occurrence of '0'. If none, return True. Otherwise check the substring after that index; if it contains any '1', return False, else True.
- Time complexity: O(n) where n = len(s) (find and membership check both scan at most n characters).
- Space complexity: O(1) extra space (slicing for membership check uses a view in Python implementation of `in` on substring costs scanning but no significant extra memory; even if a slice is created it's O(n) temporary, but we could avoid slicing by scanning from zero_idx+1 — still overall constant extra storage beyond input).