# [Problem 2154: Keep Multiplying Found Values by Two](https://leetcode.com/problems/keep-multiplying-found-values-by-two/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to repeatedly check if the current value "original" appears in nums; if it does, double original and continue. A straightforward way is to search the array each time, but that would be O(n) per check and could be wasteful. Using a hash set of nums gives O(1) average membership checks, so we can loop while original is in the set and double it. The process must terminate because values grow exponentially (and constraints limit nums values), and Python handles big integers anyway.

## Refining the problem, round 2 thoughts
- Build a set from nums for fast membership tests.
- Loop: while original in set: original *= 2.
- Edge cases: if original is not present initially, we return original immediately. Duplicates in nums don't matter because set handles membership. The number of doublings is limited (values in nums are <= 1000, but even without that bound the loop is finite as values grow).
- Time complexity: O(n) to build the set, plus O(k) membership checks where k is number of successful doublings (k is small, at most ~log(max_value/original)). Space: O(n) for the set.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findFinalValue(self, nums: List[int], original: int) -> int:
        seen = set(nums)
        while original in seen:
            original *= 2
        return original
```
- Approach: Convert nums to a set for O(1) membership checks and repeatedly double original while it's present in the set.
- Time complexity: O(n + k) where n = len(nums) to build the set and k is the number of successful doublings (typically small). In worst-case terms k <= log(max_possible_value/original), but with given constraints this is tiny.
- Space complexity: O(n) for the set.
- Implementation details: Uses Python's set for fast membership; Python integers can grow arbitrarily large so no overflow concerns.