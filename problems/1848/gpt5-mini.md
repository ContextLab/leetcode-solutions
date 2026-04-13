# [Problem 1848: Minimum Distance to the Target Element](https://leetcode.com/problems/minimum-distance-to-the-target-element/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find an index i where nums[i] == target and minimize abs(i - start). The simplest idea: scan the array, whenever nums[i] equals target compute distance = abs(i - start) and keep the minimum. Since constraints are small (n <= 1000), a single linear pass is perfectly fine.

Another thought: because we only care about distance from start, we could expand outwards from start (check start, start-1, start+1, start-2, start+2, ...) and stop as soon as we find target — that would let us potentially stop early. Both approaches are O(n) worst-case. The linear scan is simpler to implement and clear.

Edge cases: if nums[start] == target answer is 0; target is guaranteed to appear at least once so no need to handle "not found".

## Refining the problem, round 2 thoughts
Refinements and alternatives:
- Linear scan: O(n) time, O(1) extra space — simple and robust.
- Expand-from-start (two pointers with increasing radius): may find an answer faster on average, but still O(n) worst-case and slightly more bookkeeping.
- Because target exists, we can short-circuit on distance 0 immediately.

Time complexity: O(n). Space complexity: O(1).

I'll implement the straightforward linear scan solution using the LeetCode signature getMinDistance.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def getMinDistance(self, nums: List[int], target: int, start: int) -> int:
        min_dist = float('inf')
        for i, val in enumerate(nums):
            if val == target:
                dist = abs(i - start)
                if dist < min_dist:
                    min_dist = dist
                    if min_dist == 0:  # can't do better than 0
                        return 0
        return min_dist
```
- Notes:
  - Approach: single linear pass over nums, track the smallest absolute difference between the index and start for indices where nums[i] == target.
  - Time complexity: O(n), where n = len(nums).
  - Space complexity: O(1) extra space.
  - Implementation detail: early return if we find distance 0 (i == start) since it's the minimal possible.