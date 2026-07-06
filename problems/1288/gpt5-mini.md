# [Problem 1288: Remove Covered Intervals](https://leetcode.com/problems/remove-covered-intervals/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can imagine a naive approach: for each interval check against all others to see if it's covered -> O(n^2). That might pass for n up to 1000 but we can do better. A common trick for interval covering problems is to sort intervals so that potential covering intervals come before those they can cover. If intervals are sorted by start ascending, and when starts tie we put the longer interval (larger end) first, then while scanning left-to-right we can keep track of the largest end seen so far. If the current interval's end is <= max_end encountered, it's covered; otherwise it's not covered and we update max_end. Need to be careful with ties (same start) — sorting end descending ensures the longer interval appears first and will correctly mark shorter ones as covered.

## Refining the problem, round 2 thoughts
Edge cases:
- Intervals with the same start: must order by end descending so the longer one can cover the shorter.
- Intervals are unique per constraints, so exact duplicates need not be specially handled, but the sort rule still handles them.
- Since intervals are half-open [l, r), coverage rule is still c <= a and b <= d; algorithm unaffected.

Time/space:
- Sorting dominates: O(n log n) time, O(log n) to O(n) extra space depending on sort implementation. One-pass scan O(n) time and O(1) extra space beyond input.

Alternative approaches:
- Sweep-line with events (start/end) can also work but is more complex here.
- The sorted-scan approach is simplest and standard.

## Attempted solution(s)
```python
class Solution:
    def removeCoveredIntervals(self, intervals: list[list[int]]) -> int:
        # Sort by start ascending, and for equal starts sort by end descending
        intervals.sort(key=lambda x: (x[0], -x[1]))
        
        remaining = 0
        max_end = -1  # track the largest end seen for intervals that are not covered
        
        for l, r in intervals:
            # If current interval's end is <= max_end, it is covered by a previous interval
            if r <= max_end:
                # covered: skip counting
                continue
            # not covered: count it and update the max_end
            remaining += 1
            max_end = r
        
        return remaining
```
- Notes:
  - Approach: sort by start ascending and end descending, then scan keeping the maximum right endpoint seen. If current interval's right <= max_end, it is covered.
  - Correctness: Sorting ensures any interval that could cover the current one appears earlier (or equal-start longer interval appears first), so max_end correctly identifies coverage.
  - Time complexity: O(n log n) due to sorting, where n = len(intervals). Scanning is O(n).
  - Space complexity: O(1) extra (not counting input and sort's internal space); sort may use O(log n) recursion/auxiliary space.