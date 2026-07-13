# [Problem 1291: Sequential Digits](https://leetcode.com/problems/sequential-digits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need all integers between low and high whose digits increase by exactly 1 each step (like 123, 4567, 6789). A brute force check on every integer in [low, high] would be too slow for large ranges. But I notice sequential-digit numbers are very limited: they must be substrings of "123456789". So a natural approach is to generate all such substrings of various lengths (from the number of digits in low to that in high) and collect those within the range. Another approach is BFS/DFS building numbers digit-by-digit, but the substring approach from the fixed string "123456789" is simpler and straightforward.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- The maximum sequential-digit number is 123456789 (9 digits), so generation is tiny and constant-bounded.
- We should only consider lengths from len(str(low)) to len(str(high)).
- Generation order: if you iterate lengths increasingly and slide left-to-right, numbers come out sorted; we can also sort at the end to be safe.
- Complexity: very small — at most a few dozen numbers are generated.
- Alternative: BFS from digits 1..9 appending next digit until exceed high; complexity similarly tiny.
- Ensure inclusive bounds low and high are handled.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        s = "123456789"
        res = []
        len_low = len(str(low))
        len_high = len(str(high))
        for length in range(len_low, len_high + 1):
            for start in range(0, 9 - length + 1):
                num = int(s[start:start + length])
                if num < low:
                    continue
                if num > high:
                    # since start increases, further starts for this length will only produce larger nums;
                    # but they may still be smaller for larger length, so only break this inner loop.
                    break
                res.append(num)
        return res
```
- Notes:
  - Approach: generate sequential-digit candidates by taking substrings of "123456789" for each relevant length, convert to int, and include if within [low, high].
  - Time complexity: O(1) in practice because the number of candidates is bounded (at most sum_{k=2..9} (10-k) = 36). More generally O((len_high - len_low) * 9) which is tiny.
  - Space complexity: O(1) extra (excluding output). The output size is at most that bounded constant.