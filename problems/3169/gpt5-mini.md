# [Problem 3169: Count Days Without Meetings](https://leetcode.com/problems/count-days-without-meetings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count how many days from 1..days have no meeting. Meetings are given as intervals [start, end] inclusive and they may overlap. days can be up to 1e9 so I cannot build a boolean array. The classic approach is to compute the total number of days covered by the union of intervals, then subtract from days.

So I should merge overlapping (or contiguous) intervals after sorting by start and sum lengths. Watch out for inclusivity: length of [s,e] is (e - s + 1). Sorting O(n log n) is fine for up to 1e5 intervals. Edge cases: intervals may cover entire range => answer 0. Also intervals may be adjacent; merging or not merging must still count correctly (merging adjacent into one interval is safe).

## Refining the problem, round 2 thoughts
Refinement: sort meetings by start. Initialize current interval to first sorted interval. Iterate through remaining intervals:
- If next.start > current_end: they are disjoint — add current length to covered and start a new current interval.
- Else (next.start <= current_end): they overlap (or touch) — extend current_end = max(current_end, next.end).

After loop, add the last current interval length. Result = days - covered (clamp to >=0 though it should never be negative given constraints).

Time complexity O(n log n) due to sorting. Space complexity O(1) extra (ignoring input sort space) or O(n) if sorting creates a new list.

Edge cases: single meeting, meetings cover full range, meetings all disjoint, meetings entirely nested.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countDaysWithoutMeetings(self, days: int, meetings: List[List[int]]) -> int:
        # Sort meetings by start day
        meetings.sort(key=lambda x: x[0])
        
        covered = 0
        cur_start, cur_end = meetings[0]
        
        for s, e in meetings[1:]:
            if s > cur_end:
                # disjoint interval -> add current and start new
                covered += (cur_end - cur_start + 1)
                cur_start, cur_end = s, e
            else:
                # overlap -> extend current end if needed
                if e > cur_end:
                    cur_end = e
        
        # add the final interval
        covered += (cur_end - cur_start + 1)
        
        # days without meetings
        return days - covered if days >= covered else 0
```
- Notes:
  - Approach: sort intervals and merge overlapping intervals to compute the total number of covered days, then subtract from total days.
  - Time complexity: O(n log n) for sorting n = len(meetings), plus O(n) for the merge pass.
  - Space complexity: O(1) extra (not counting input and sort overhead).
  - Implementation details: intervals are inclusive so each interval length is end - start + 1. We treat intervals with s > cur_end as disjoint; intervals with s <= cur_end overlap and we extend cur_end. The final result is days - covered; it should be >= 0 by constraints, but code protects against negative by clamping to 0.