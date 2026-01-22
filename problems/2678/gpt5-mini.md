# [Problem 2678: Number of Senior Citizens](https://leetcode.com/problems/number-of-senior-citizens/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is straightforward: each string encodes phone (10 chars), gender (1 char), age (2 chars), seat (2 chars) in fixed positions. To count passengers older than 60, I just need to extract the two-character age substring (positions 11 and 12 using 0-based indexing, i.e., s[11:13]) and convert it to an integer, then check > 60. There are no tricky swaps or variable-length fields — fixed positions make slicing reliable and O(1) per string.

## Refining the problem, round 2 thoughts
- Edge cases: ages with leading zeroes (e.g., "05") should parse correctly with int("05") -> 5. All input strings are length 15 so slicing won't go out of bounds.
- The constraints give n up to 100, so performance is trivial, but the approach is linear in number of entries anyway.
- Alternative: iterate characters and build the number manually, but Python int conversion of the two-char substring is simplest and clear.
- Complexity: O(n) time, O(1) extra space (besides output storage). No special data structures needed.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countSeniors(self, details: List[str]) -> int:
        count = 0
        for s in details:
            # age is at indices 11 and 12 (0-based), slice s[11:13]
            age = int(s[11:13])
            if age > 60:
                count += 1
        return count
```
- Notes: We slice the age substring s[11:13], convert to int, and increment when age > 60. Time complexity O(n) for n strings; space complexity O(1) additional. The solution relies on the fixed-format guarantee of each detail string being length 15.