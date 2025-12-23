# [Problem 2054: Two Best Non-Overlapping Events](https://leetcode.com/problems/two-best-non-overlapping-events/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share step-by-step chain-of-thought, but here's a concise summary of the approach: sort events by start time, keep an array of start times and values in that order, build a suffix maximum array of values to quickly get the best event value starting at or after any time, and for each event binary-search the earliest event that can start after the current event's end (end + 1). Combine current event's value with the best possible following event value (if any) and keep the maximum across all events. Also consider taking a single event (the global max value).

## Refining the problem, round 2 thoughts
- Important detail: times are inclusive, so a following event must start >= end + 1. That is handled by searching for start >= end + 1.
- Sorting by start time lets us binary search on start times to find the first non-overlapping candidate.
- Precompute suffix maximums of the values in start-sorted order so each query to find the best following event is O(1) after binary search.
- Time complexity: O(n log n) for sorting + O(n log n) for n binary searches = O(n log n). Space complexity: O(n) for arrays and suffix max.
- Alternative approaches: sort by end time and use a segment tree / ordered map; or sweep-line with best-so-far; but the start-sort + suffix-max + binary search is simple and efficient for constraints up to 1e5.

## Attempted solution(s)
```python
from bisect import bisect_left
from typing import List

class Solution:
    def maxTwoEvents(self, events: List[List[int]]) -> int:
        # Sort events by start time
        events.sort(key=lambda e: e[0])
        starts = [e[0] for e in events]
        values = [e[2] for e in events]
        n = len(events)
        
        # Suffix max of values: best value among events[i:]
        suffix_max = [0] * n
        suffix_max[-1] = values[-1]
        for i in range(n - 2, -1, -1):
            suffix_max[i] = max(values[i], suffix_max[i + 1])
        
        ans = 0
        # Also track best single event
        ans = max(values)
        
        # For each event, try to pair it with the best non-overlapping event that starts after its end
        for i, (s, e, v) in enumerate(events):
            # Find first index with start >= e + 1 (since inclusive end)
            j = bisect_left(starts, e + 1)
            if j < n:
                ans = max(ans, v + suffix_max[j])
            # also single event already considered
        return ans
```
- Notes:
  - Approach: sort events by start time, precompute suffix max of values, for each event binary-search the earliest next event that starts at or after end+1 and combine values.
  - Time complexity: O(n log n) due to sorting and binary searches.
  - Space complexity: O(n) for arrays and suffix max.
  - Handles edge cases where no compatible second event exists (j == n).