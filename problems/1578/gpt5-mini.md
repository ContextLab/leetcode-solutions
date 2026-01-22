# [Problem 1578: Minimum Time to Make Rope Colorful](https://leetcode.com/problems/minimum-time-to-make-rope-colorful/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to remove balloons so no two adjacent colors are the same, minimizing total removal time. When two consecutive balloons have the same color, I must remove at least one of them. For a run (group) of identical colors, I can keep exactly one balloon and remove the rest. Which one to keep? The one with the largest neededTime, because that minimizes sum of removed times. So for each contiguous group of equal characters, sum the group's removal times and subtract the maximum in that group (or equivalently add all but the max). That suggests a linear scan grouping identical colors and computing group sums and maxes. I can also do a greedy pairwise approach: walk left-to-right, keep the index of the kept balloon in the current same-color streak; when encountering a same-colored balloon, remove the cheaper of the current and previous (accumulate that cost) and keep the more expensive one for possible future comparisons.

## Refining the problem, round 2 thoughts
Edge cases: single-character string (n=1) => 0 cost. Many repeated same characters in a row: need to ensure we don't remove more than necessary. Time/space: need O(n) time, O(1) extra space. Both the group-sum-minus-max approach and the pairwise greedy approach meet that. The pairwise approach can be implemented with a "prev index" that points to the balloon we keep within the current group. When colors[i] == colors[prev], we add min(neededTime[i], neededTime[prev]) to the total and update prev to the index of the balloon with larger neededTime so that the kept one persists. When colors differ, reset prev = i.

This is simple, single-pass, no extra arrays, handles all constraints (n up to 1e5).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minCost(self, colors: str, neededTime: List[int]) -> int:
        n = len(colors)
        if n <= 1:
            return 0

        total = 0
        prev = 0  # index of the balloon we are currently keeping in the ongoing same-color streak

        for i in range(1, n):
            if colors[i] == colors[prev]:
                # need to remove one of the two; remove the cheaper one
                if neededTime[i] < neededTime[prev]:
                    total += neededTime[i]
                    # prev stays the same (we keep prev)
                else:
                    total += neededTime[prev]
                    prev = i  # keep the current one (larger or equal)
            else:
                # different color: start a new streak
                prev = i

        return total
```
- Notes:
  - Approach: single-pass greedy. For each pair in the same-color group, remove the one with smaller removal time and keep the larger to potentially compare with the next balloon in the group.
  - Time complexity: O(n), where n = len(colors), because we scan once.
  - Space complexity: O(1) extra space (only a few variables used).
  - Implementation details: We use an index `prev` to remember which balloon in the current contiguous same-color group we are keeping; when we encounter another balloon of the same color we add the smaller neededTime to the answer and update `prev` to the index with the larger neededTime. This correctly handles groups of arbitrary length.