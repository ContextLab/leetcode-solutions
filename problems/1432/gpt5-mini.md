# [Problem 1432: Max Difference You Can Get From Changing an Integer](https://leetcode.com/problems/max-difference-you-can-get-from-changing-an-integer/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to perform two independent digit-replacement operations on the same number and maximize the difference between the two results. Intuitively, to maximize the difference I want one result as large as possible and the other as small as possible.

For making the number as large as possible: turning digits into 9 helps. Replacing every occurrence of some digit x with 9 should increase the number; the best choice is to pick the leftmost digit that is not already 9 and replace all its occurrences with 9 (that maximizes higher-place contributions).

For making the number as small as possible: I must avoid creating a leading zero. If the first digit is not '1', turning that digit to '1' (all occurrences) is best because lowering the most significant digit yields the largest decrease without making it zero. If the first digit is '1', I cannot turn it to '0' (would be invalid), so I should look for a digit later in the number to change to '0' (first occurrence of a digit not '0' or '1', replace all its occurrences with '0') — this reduces the number as much as possible while keeping a valid leading digit. If there's none to replace, then I cannot reduce the number further.

Edge cases: single-digit numbers, numbers already all 9s or all 1/0 patterns, and ensuring replacement of all occurrences, not just first.

## Refining the problem, round 2 thoughts
Algorithm:
- Convert number to string s.
- Compute a (maximized):
  - Find the first character in s not equal to '9'. If none, a = num.
  - Otherwise replace all occurrences of that character with '9' and parse to int.
- Compute b (minimized):
  - If s[0] != '1': replace all occurrences of s[0] with '1' -> parse to int.
  - Else (s[0] == '1'): scan s from left to right (starting at index 1) for the first character not in {'0','1'}. If found, replace all occurrences of that character with '0'. If not found, b = num.
- Return a - b.

Time complexity: O(n) for scanning and replacements where n is number of digits (<= 10). Space complexity: O(n) for string manipulations.

Now I'll implement this cleanly in Python.

## Attempted solution(s)
```python
class Solution:
    def maxDiff(self, num: int) -> int:
        s = str(num)
        # Maximize: replace first non-'9' digit (if any) with '9' everywhere
        ch_max = None
        for ch in s:
            if ch != '9':
                ch_max = ch
                break
        if ch_max is None:
            a = num
        else:
            a = int(s.replace(ch_max, '9'))

        # Minimize: careful with leading zero constraint
        # If first digit is not '1', replace all occurrences of first digit with '1'
        if s[0] != '1':
            b = int(s.replace(s[0], '1'))
        else:
            # first digit is '1', find first digit (from index 1) not in {'0','1'}
            ch_min = None
            for ch in s[1:]:
                if ch != '0' and ch != '1':
                    ch_min = ch
                    break
            if ch_min is None:
                b = num
            else:
                b = int(s.replace(ch_min, '0'))

        return a - b
```
- Notes:
  - The solution converts the integer to string to perform digit-wise inspection and global replacements.
  - Replacements use str.replace to change all occurrences of the chosen digit.
  - Time complexity: O(n) where n is number of digits (n <= 10 given constraints, effectively constant). Each replace is O(n).
  - Space complexity: O(n) for string copies.
  - Handles edge cases: single-digit numbers, numbers already maximal/minimal, and prevents creating leading zeros by special-casing the first digit.