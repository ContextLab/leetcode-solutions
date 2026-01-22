# [Problem 904: Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see we can only hold two types of fruit at a time. That suggests maintaining a contiguous window of trees (since we must move right continuously) that contains at most two distinct fruit types. The goal is to maximize the window length. A natural approach is a sliding window with two pointers and a frequency map of the fruit types in the window. Brute force would try every start and extend until a third type appears — O(n^2) — but sliding window can do it in O(n). Also note edge cases like all same type, only two trees, or alternating types.

## Refining the problem, round 2 thoughts
Refinement: use two pointers left and right. Expand right adding fruits[right] to a count map. If map has more than 2 keys, move left forward and decrement counts until we have at most 2 keys. Track the max window size encountered. Since the map holds at most 2 keys, space is effectively O(1). Time is O(n) because each index is visited at most twice (once by right, once by left). Alternative micro-optimizations exist (tracking two fruit types and the last run length without a map), but the map version is simple and clear.

Edge cases:
- fruits length 1 or 2 -> answer is length.
- All same fruit -> answer is length.
- Many distinct fruits -> the algorithm will shrink window appropriately.

Time complexity: O(n). Space complexity: O(1) (map size <= 2).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        # sliding window with counts of fruit types
        left = 0
        counts = {}
        max_fruits = 0
        
        for right, f in enumerate(fruits):
            counts[f] = counts.get(f, 0) + 1
            
            # shrink window until we have at most 2 distinct types
            while len(counts) > 2:
                left_f = fruits[left]
                counts[left_f] -= 1
                if counts[left_f] == 0:
                    del counts[left_f]
                left += 1
            
            # window [left..right] is valid (<= 2 types)
            max_fruits = max(max_fruits, right - left + 1)
        
        return max_fruits
```
- Notes:
  - Approach: standard sliding window maintaining counts of fruit types in the current window; expand right, shrink left when > 2 types.
  - Time complexity: O(n), where n = len(fruits). Each index is processed by right once and moved past by left at most once.
  - Space complexity: O(1) (bounded by 2 distinct fruit types in the map).