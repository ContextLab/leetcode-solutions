# [Problem 744: Find Smallest Letter Greater Than Target](https://leetcode.com/problems/find-smallest-letter-greater-than-target/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The array is sorted and we need the smallest letter strictly greater than target. Sounds like binary search for the first element > target. Because letters wrap around (if none greater, return letters[0]), we should handle that by returning the first element when the binary search reaches the end. A linear scan would work but is O(n); binary search gives O(log n). Need to be careful about duplicates (many equal letters) — we want strictly greater so when letters[mid] <= target move right.

## Refining the problem, round 2 thoughts
- Use binary search to find the first index where letters[idx] > target.
- Typical pattern: lo = 0, hi = n (notice hi = n allows us to detect "not found" when lo == n), while lo < hi: mid = (lo + hi)//2; if letters[mid] > target: hi = mid else lo = mid + 1. After loop, if lo == n then wrap to letters[0], else letters[lo].
- Alternatively, Python's bisect module (bisect_right) could be used: idx = bisect_right(letters, target); return letters[idx % n].
- Time complexity O(log n), space O(1).
- Edge cases: all letters <= target (wrap), duplicates of letters equal to target.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def nextGreatestLetter(self, letters: List[str], target: str) -> str:
        n = len(letters)
        lo, hi = 0, n  # hi is n to allow detecting wrap-around when lo == n
        while lo < hi:
            mid = (lo + hi) // 2
            if letters[mid] > target:
                hi = mid
            else:
                lo = mid + 1
        # if lo == n, no letter > target found -> wrap to first element
        return letters[lo] if lo < n else letters[0]
```
- Notes:
  - Approach: binary search for the first index with letters[idx] > target.
  - Time complexity: O(log n) where n = len(letters).
  - Space complexity: O(1).
  - Implementation detail: using hi = n and returning letters[0] when lo == n handles the wrap-around requirement.