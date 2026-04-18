# [Problem 3783: Mirror Distance of an Integer](https://leetcode.com/problems/mirror-distance-of-an-integer/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[We need to compute abs(n - reverse(n)). The reverse of an integer is just its digits reversed; leading zeros from the reversed string should be dropped (so reverse(10) -> 1). The simplest approach is to convert to string, reverse it, convert back to int, and take the absolute difference. Alternatively, we can reverse digits numerically with division/modulo to avoid extra string memory. Given constraints (n up to 1e9) either approach is trivial in performance. Edge cases: single-digit numbers (reverse is itself), numbers ending with zeros (leading zeros after reverse should be ignored).]

## Refining the problem, round 2 thoughts
[I'll implement the straightforward string-based solution for clarity and brevity: s = str(n); rev = int(s[::-1]); return abs(n - rev). This handles leading zeros automatically because int("01") -> 1. Time complexity is proportional to the number of digits d (d = floor(log10 n) + 1), so O(d). Space complexity is O(d) for the string. If desired, a numeric reversal would use O(1) extra space and the same time complexity; both are fine given constraints. Confirm that n >= 1 so no zero/negative input weirdness.]

## Attempted solution(s)
```python
class Solution:
    def mirrorDistance(self, n: int) -> int:
        s = str(n)
        rev = int(s[::-1])
        return abs(n - rev)
```
- Notes:
  - Approach: convert to string, reverse, convert back to int to drop any leading zeros, then take absolute difference.
  - Time complexity: O(d) where d is the number of digits in n (d = O(log10 n)). For given constraints this is effectively constant-time.
  - Space complexity: O(d) due to the string and reversed string. A numeric reversal would reduce extra space to O(1) if needed.