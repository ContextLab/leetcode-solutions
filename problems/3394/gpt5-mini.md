# [Problem 3394: Check if Grid can be Cut into Sections](https://leetcode.com/problems/check-if-grid-can-be-cut-into-sections/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to determine if we can make two horizontal cuts (or two vertical cuts) so that the grid is partitioned into three bands and each band contains at least one rectangle and no rectangle is split by a cut. A cut at coordinate c (horizontal: y=c, vertical: x=c) is invalid if any rectangle spans across c (i.e., start < c < end). Because rectangles don't overlap in the plane, that doesn't mean their projections on x or y can't overlap; a horizontal cut applies across the entire width, so any rectangle whose y-interval contains the cut would be split. So the problem reduces to partitioning the set of axis-intervals (y-intervals for horizontal cuts, x-intervals for vertical cuts) into three contiguous groups along that axis such that cuts appear between intervals and do not lie inside any interval.

A natural approach: project rectangles to intervals on the axis, sort by start, compute prefix maximum of ends. A valid cut between index i and i+1 exists when prefix_max[i] <= start[i+1] (no interval crosses that boundary). We need two such cut positions producing three non-empty groups, i.e., find i < j such that cuts after i and after j both valid. Brute-force nested search would be O(m^2) (m = number of rectangles) — too slow for 1e5. But we can precompute a boolean array of valid cut positions and a suffix OR to check quickly if a second cut exists after a chosen first cut. Do this for both axes.

## Refining the problem, round 2 thoughts
Edge cases:
- Must ensure at least one rectangle per section => require at least 3 rectangles overall.
- Sort by start; groups are contiguous in that ordering.
- A cut at exactly a rectangle end or start is allowed (because it's not strictly inside).
- For performance, we must avoid nested loops: precompute can_cut_at[k] for all k (k is cut between k and k+1) and suffix_has_cut for O(1) queries.

Complexity:
- Sorting intervals O(m log m).
- Single linear pass to compute prefix_max, can_cut_at, suffix_has_cut, and test possible first cuts: O(m).
- Do this twice (x and y projections), so overall O(m log m).

I'll implement a helper check_axis that returns True if we can split along that axis, and call it for y (horizontal cuts) and x (vertical cuts). If either returns True, answer is True.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def cutGrid(self, n: int, rectangles: List[List[int]]) -> bool:
        """
        Return True if we can make two horizontal or two vertical cuts to split
        the grid into three sections where each section contains at least one
        rectangle and no rectangle is cut.
        """
        m = len(rectangles)
        if m < 3:
            return False

        def check_axis(intervals: List[tuple]) -> bool:
            # intervals: list of (start, end)
            m = len(intervals)
            if m < 3:
                return False
            intervals.sort(key=lambda x: x[0])  # sort by start
            starts = [s for s, e in intervals]
            ends = [e for s, e in intervals]

            # prefix_max_end[i] = max ends among intervals[0..i]
            prefix_max = [0] * m
            cur_max = -1
            for i in range(m):
                if ends[i] > cur_max:
                    cur_max = ends[i]
                prefix_max[i] = cur_max

            # can_cut_at[i] is True if we can cut between i and i+1
            # i ranges 0..m-2
            can_cut_at = [False] * (m - 1)
            for i in range(m - 1):
                # cut between i and i+1 is valid if no interval crosses it:
                # prefix_max[i] <= starts[i+1]
                if prefix_max[i] <= starts[i + 1]:
                    can_cut_at[i] = True

            # suffix_has_cut[k] = True if there exists a cut position j >= k
            # (j up to m-2) where can_cut_at[j] is True. We'll need to query for
            # existence of a second cut after the first cut.
            suffix_has_cut = [False] * (m - 1)
            if m - 2 >= 0:
                suffix_has_cut[m - 2] = can_cut_at[m - 2]
                for idx in range(m - 3, -1, -1):
                    suffix_has_cut[idx] = can_cut_at[idx] or suffix_has_cut[idx + 1]

            # Need two cuts: choose first cut at i (0..m-3), which requires can_cut_at[i],
            # and require there exists a second cut j >= i+1 (so suffix_has_cut[i+1] True).
            for i in range(0, m - 2):
                if can_cut_at[i] and suffix_has_cut[i + 1]:
                    return True
            return False

        # Build interval lists for y (horizontal cuts) and x (vertical cuts)
        y_intervals = [(r[1], r[3]) for r in rectangles]  # (start_y, end_y)
        x_intervals = [(r[0], r[2]) for r in rectangles]  # (start_x, end_x)

        return check_axis(y_intervals) or check_axis(x_intervals)
```

- Notes about the approach:
  - We project rectangles onto an axis and sort by the interval start. If prefix_max_end[i] <= start[i+1] then cutting between i and i+1 does not split any interval.
  - Precomputing can_cut_at and a suffix OR array avoids nested loops and makes the check linear after sorting.
  - Time complexity: O(m log m) for sorting + O(m) for the checks on each axis => O(m log m) overall.
  - Space complexity: O(m) for arrays used (prefix_max, can_cut_at, suffix_has_cut).