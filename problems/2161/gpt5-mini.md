# [Problem 2161: Partition Array According to Given Pivot](https://leetcode.com/problems/partition-array-according-to-given-pivot/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to reorder nums so that elements < pivot come first, then elements == pivot, then elements > pivot. The relative order among elements in the same category must be preserved. That suggests a stable partition. My immediate thought is to collect three lists (less, equal, greater) in one pass and then concatenate them — this preserves order and is simple. Alternatives: try an in-place stable partition, but that's more complicated and unnecessary given constraints. Complexity target O(n) time, O(n) additional space.

## Refining the problem, round 2 thoughts
Edge cases: pivot is guaranteed to be present per constraints. Duplicates must be kept in original relative order. Negative values are irrelevant to logic. Using three lists handles all cases and preserves relative order. Another minor variant is two-pass overwrite of nums (count or first collect indices), but the three-list approach is straightforward and clear. Time O(n), space O(n). For n up to 1e5 this is fine.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        less = []
        equal = []
        greater = []
        
        for x in nums:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            else:
                greater.append(x)
        
        return less + equal + greater
```
- Notes:
  - Approach: single pass to partition elements into three buckets while preserving order, then concatenate.
  - Time complexity: O(n), where n = len(nums), since we visit each element once and concatenation is O(n).
  - Space complexity: O(n) additional space for the three buckets (worst-case one bucket holds all elements). This meets constraints and keeps implementation simple and clear.