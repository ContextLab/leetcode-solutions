# [Problem 2161: Partition Array According to Given Pivot](https://leetcode.com/problems/partition-array-according-to-given-pivot/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to reorder nums so that values < pivot come first, then values == pivot, then values > pivot. The relative order among values in the "< pivot" group and among values in the "> pivot" group must be preserved. That suggests a stable partition. The simplest approach that preserves order is to collect elements into three separate lists (less, equal, greater) while iterating once through nums, then concatenate them. That is O(n) time and uses O(n) extra space. I could try an in-place stable partition, but that’s more complex (requires shifting elements or multiple passes) and not necessary given constraints (n up to 1e5) — extra O(n) memory is fine.

## Refining the problem, round 2 thoughts
Edge cases: nums length minimum is 1 and pivot is guaranteed to be present, so we don't need to handle "pivot not found." Negative values are allowed but irrelevant to the method. The three-list approach keeps original relative order within groups automatically because we append in a single left-to-right pass. Time complexity: single pass O(n). Space complexity: O(n) additional (three lists whose total length is n). This is simple, clear, and efficient enough. An alternative would be to do two passes: first count sizes to build an output array and place elements in appropriate ranges while maintaining indices — also O(n) time and O(n) space but slightly more code. In-place stable partitioning is possible but unnecessary here.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        less = []
        equal = []
        greater = []
        
        # Single pass: distribute elements into three lists to preserve relative order
        for x in nums:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            else:
                greater.append(x)
        
        # Concatenate the lists: less, then equal, then greater
        return less + equal + greater
```
- Notes:
  - Approach: single-pass stable partition using three lists (less, equal, greater) and concatenation.
  - Time complexity: O(n), where n = len(nums), because we traverse nums once and concatenate lists (concatenation is O(n) overall).
  - Space complexity: O(n) extra space for the three lists (their total size is n).