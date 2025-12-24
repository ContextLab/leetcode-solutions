# [Problem 3074: Apple Redistribution into Boxes](https://leetcode.com/problems/apple-redistribution-into-boxes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have n packs each with some number of apples, but apples from a single pack can be split across multiple boxes. That means we don't need to worry about pack-level placement constraints — only the total number of apples matters. So we just need enough total box capacity to hold all apples.

Given m boxes with capacities, we want the minimum number of boxes whose capacities sum to at least the total apples. That suggests sorting boxes by capacity descending and taking the largest boxes until their sum >= total apples. That should give the minimum number of boxes because using any smaller box instead of a chosen larger one cannot reduce the count.

Edge cases: total apples may be zero (not in constraints since apple[i] >= 1), or one big box already enough. Problem statement guarantees it's possible (sum(capacity) >= sum(apple)).

## Refining the problem, round 2 thoughts
No need for complex DP or knapsack because packs are splittable. The greedy choice — pick largest boxes first — is optimal. Proof sketch: if a solution uses k boxes, replacing any used box with a larger unused box only increases capacity; to minimize k we should always pick the largest available capacities. Time complexity driven by sorting capacities: O(m log m). Space complexity O(1) extra (aside from input and sorting).

We should just:
- compute total_apples = sum(apple)
- sort capacity descending
- accumulate capacities until accumulated >= total_apples
- return count used

Edge cases to consider:
- Already the largest box suffices.
- Need all boxes.
- Small m,n up to 50 so any reasonable approach is fine.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumBoxes(self, apple: List[int], capacity: List[int]) -> int:
        total_apples = sum(apple)
        # Sort capacities descending
        capacity.sort(reverse=True)
        acc = 0
        for i, c in enumerate(capacity):
            acc += c
            if acc >= total_apples:
                return i + 1
        # Problem guarantees it's possible, but return all boxes as fallback
        return len(capacity)
```
- Notes:
  - Approach: sort capacities in descending order and take the largest boxes until their sum is >= total apples.
  - Time complexity: O(m log m + n) where m = len(capacity), n = len(apple). Sorting dominates: O(m log m).
  - Space complexity: O(1) extra (in-place sort), or O(m) if counting the sort's auxiliary memory.