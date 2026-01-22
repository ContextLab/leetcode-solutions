# [Problem 2210: Count Hills and Valleys in an Array](https://leetcode.com/problems/count-hills-and-valleys-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count hills and valleys where an index i is a hill if the closest non-equal neighbors on both sides are smaller, and a valley if they are larger. Equal adjacent elements belong to the same hill/valley, so if I treat each equal run as one entity I won't double-count. One straightforward idea: collapse consecutive equal elements (compress the array by removing consecutive duplicates) and then for each remaining element (except first/last) check if it's strictly greater than both neighbors (hill) or strictly less than both neighbors (valley). That should satisfy the "closest non-equal neighbor" requirement because consecutive equals are merged.

## Refining the problem, round 2 thoughts
Edge cases:
- If after collapsing consecutive duplicates the array length < 3, there can't be any hills/valleys.
- Collapsing must only remove consecutive duplicates, not all duplicates across the array.
Complexity: single pass to compress O(n), single pass to count O(n) => O(n) time, O(n) extra worst-case for compressed array (but in-place counting without extra array is possible by skipping equals when searching neighbors; compress approach is simpler and clear).
Space O(n) worst-case for compressed array (but bounded by original n ≤ 100, trivial).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countHillValley(self, nums: List[int]) -> int:
        # Compress consecutive equal elements
        compressed = []
        for x in nums:
            if not compressed or compressed[-1] != x:
                compressed.append(x)
        # If less than 3 elements, can't have hill/valley
        if len(compressed) < 3:
            return 0
        count = 0
        # Check each middle element
        for i in range(1, len(compressed) - 1):
            if compressed[i] > compressed[i - 1] and compressed[i] > compressed[i + 1]:
                count += 1
            elif compressed[i] < compressed[i - 1] and compressed[i] < compressed[i + 1]:
                count += 1
        return count
```
- Notes:
  - Approach: collapse consecutive equal elements into a compressed array, then count elements (except endpoints) that are strictly greater than both neighbors (hill) or strictly less than both neighbors (valley).
  - Time complexity: O(n) where n = len(nums) — one pass to compress and one pass to count.
  - Space complexity: O(n) worst-case for the compressed array (can be O(1) extra if you instead search left/right non-equal neighbors on the fly, but compression is simpler and sufficient given constraints).
  - This handles edge cases where equals form plateaus correctly by treating a plateau as a single candidate.