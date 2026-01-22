# [Problem 2566: Maximum Difference by Remapping a Digit](https://leetcode.com/problems/maximum-difference-by-remapping-a-digit/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We must choose exactly one digit value (0–9) and remap ALL its occurrences to another digit, and we want difference between the largest possible remapped number and the smallest possible remapped number. Since remapping affects all occurrences, the most significant positions matter most.

For maximizing, it makes sense to turn some digit(s) into 9 — increasing the most significant non-9 digit gives the biggest boost. So scan left-to-right, pick the first digit that's not '9', and replace all occurrences of that digit with '9'.

For minimizing, because leading zeroes are allowed, turning the most significant digit value to 0 yields the largest possible drop. So simply replace all occurrences of the first digit (most significant digit) with '0'. That should produce the minimum possible value.

So plan: string-ify the number, form a max candidate by replacing first non-'9' digit with '9' everywhere, form a min candidate by replacing the first character's digit with '0' everywhere, convert both to int and return max - min.

## Refining the problem, round 2 thoughts
Edge cases:
- If the number is all 9s, max candidate equals original (no non-9 digit to change).
- Leading zeros after replacement are allowed; converting to int removes them naturally.
- If the most significant digit is the only digit or appears multiple times, replacing it with 0 handles that uniformly.
- Time/space: working with the string representation (at most 9 characters since num ≤ 1e8) — trivial complexity.

Alternative ideas:
- Could try enumerating all 10×10 remapping pairs and compute best min and max, but that's overkill (100 possibilities) and unnecessary given the simple greedy reasoning.

Complexity:
- Time O(n) where n = number of digits (≤ 9).
- Space O(n) for the string variants.

## Attempted solution(s)
```python
class Solution:
    def maxDiff(self, num: int) -> int:
        s = str(num)
        # Build max: replace all occurrences of the first non-'9' digit with '9'
        max_s = s
        for ch in s:
            if ch != '9':
                max_s = s.replace(ch, '9')
                break
        # Build min: replace all occurrences of the first digit with '0'
        first = s[0]
        min_s = s.replace(first, '0')
        # Convert to int (handles leading zeros) and return difference
        return int(max_s) - int(min_s)
```
- Notes:
  - Approach: greedy, based on positional significance. For max, change the leftmost non-9 digit to 9 (replace all occurrences of that digit). For min, change the most significant digit's value to 0 (replace all occurrences of that digit).
  - Time complexity: O(n) where n is number of digits (string operations and a single pass).
  - Space complexity: O(n) for the temporary strings.