# [Problem 2300: Successful Pairs of Spells and Potions](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need, for each spell, the number of potions such that spell * potion >= success. Naively checking all pairs is O(n*m) which is too slow (n,m up to 1e5). Observing that potions don't depend on spell, so if we sort potions we can binary-search the smallest potion that works for a given spell and then count all potions to the right. For a spell s the minimum required potion strength is ceil(success / s). Use binary search (bisect_left) on sorted potions. Watch out for integer division and large success (up to 1e10) — use integer arithmetic to compute the ceiling.

## Refining the problem, round 2 thoughts
- Sort potions once: O(m log m).
- For each spell, compute required = (success + s - 1) // s (handles ceiling safely).
- Use bisect_left(potions, required) to get first acceptable index; answer is m - idx.
- Edge cases: if required > max(potions) -> 0; if required <= min(potions) -> m. The bisect call handles these automatically.
- Time complexity: O(m log m + n log m). Space: O(1) extra besides output and sorting.
- Alternative: sort spells with indices and use two-pointer from largest potion to count in O(n log n + m log m) or O(n log n + m) if both sorted; but binary-search approach is straightforward and clean.

## Attempted solution(s)
```python
from typing import List
import bisect

class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort()
        m = len(potions)
        res = []
        for s in spells:
            # minimum potion value needed so that s * potion >= success
            # compute ceil(success / s) safely with integers
            if s == 0:
                # constraints say s >= 1, but guard anyway
                res.append(0 if success > 0 else m)
                continue
            required = (success + s - 1) // s  # ceil division
            idx = bisect.bisect_left(potions, required)
            res.append(m - idx)
        return res
```
- Notes:
  - We sort potions once, then for each spell compute the minimal potion required and binary search for its index.
  - Time complexity: O(m log m + n log m) where m = len(potions), n = len(spells).
  - Space complexity: O(1) extra (besides output array and sorting in-place).
  - Implementation detail: Use integer ceil via (success + s - 1) // s to avoid floating-point and to handle large success (up to 1e10).