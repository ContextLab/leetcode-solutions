# [Problem 2406: Divide Intervals Into Minimum Number of Groups](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to split intervals into groups where intervals inside a group do not intersect (intersection includes touching at endpoints). This is essentially coloring intervals so that overlapping intervals get different colors. For interval graphs the minimum number of colors equals the maximum number of intervals that overlap at any point (the clique number). So the answer should be the maximum number of intervals covering any single point.

How to compute maximum overlap? Classic sweep-line: turn each interval into events (start +1, end -1) and scan accumulating active intervals. Because intervals are inclusive, two intervals [a,b] and [b,c] overlap — so the end event needs to be processed after a start at the same coordinate. Easiest way: treat end event at right+1 with -1 so that the inclusive end is handled correctly.

Alternatively could sort starts and ends and use two pointers with careful comparison (advance end pointer when end < start).

So I'll implement the event-based sweep with (left, +1) and (right+1, -1), sort events by position and accumulate to find the max active count.

## Refining the problem, round 2 thoughts
Edge cases:
- Many intervals starting/ending at same positions — summing deltas at same position is fine.
- Inclusive end semantics: using right+1 for the -1 avoids tricky tie-breaking.
- Constraints: up to 1e5 intervals, endpoints up to 1e6, so sorting O(n log n) is fine and right+1 stays within int range.

Complexity:
- Time: O(n log n) for sorting 2n events.
- Space: O(n) to store events.

I'll write a clean Python solution with the LeetCode signature minGroups.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minGroups(self, intervals: List[List[int]]) -> int:
        # Build events: +1 at left, -1 at right+1 (inclusive intervals)
        events = []
        for l, r in intervals:
            events.append((l, 1))
            events.append((r + 1, -1))
        events.sort()  # sorts by position, then by delta (but deltas at same pos will be summed)

        cur = 0
        ans = 0
        i = 0
        n = len(events)
        # accumulate events; compress same-position events by summing deltas
        while i < n:
            pos = events[i][0]
            delta_sum = 0
            while i < n and events[i][0] == pos:
                delta_sum += events[i][1]
                i += 1
            cur += delta_sum
            if cur > ans:
                ans = cur
        return ans
```
- Notes:
  - Approach: sweep-line with events; using (right + 1, -1) ensures inclusive endpoints count as overlapping.
  - Time complexity: O(n log n) due to sorting 2n events.
  - Space complexity: O(n) for events array.
  - This computes the maximum number of intervals covering any point, which equals the minimum number of groups needed.