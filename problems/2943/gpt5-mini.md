# [Problem 2943: Maximize Area of Square Hole in Grid](https://leetcode.com/problems/maximize-area-of-square-hole-in-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can remove some bars from the given horizontal and vertical removable lists. Removing bars merges adjacent 1x1 cells into larger rectangular holes. To get a square hole of side k we need a vertical gap of at least k (between two remaining horizontal bars) and a horizontal gap of at least k (between two remaining vertical bars). Horizontal removals and vertical removals are independent, so we can maximize the horizontal gap and vertical gap separately and then the achievable square side is the minimum of those two maxima.

Which removals produce the largest gap between two remaining bars? Removing a set of consecutive bar indices creates the largest contiguous gap. Since only bars in hBars (or vBars) are removable and their count is small (<=100), the only way to create a large gap is to remove a consecutive run of indices inside the removable list. If you have a run of k consecutive removable horizontal bars at positions x..x+k-1, then the nearest fixed bars are at x-1 and x+k and the gap (number of cells between them) is (x+k)-(x-1) = k+1. Thus the maximum possible vertical span equals (maximum length of consecutive run in hBars) + 1. Same for vertical bars.

So the side length of the largest square = min(max_run_h + 1, max_run_v + 1), area = square of that.

## Refining the problem, round 2 thoughts
- hBars and vBars values are distinct and in [2, n+1] / [2, m+1], so ends (1 and n+2, and 1 and m+2) are always fixed — endpoints of runs are well-defined.
- We only need to find the longest consecutive sequence in each removable list. Sort each list (O(L log L)) and scan to find the longest consecutive run.
- Complexity: sorting O(L log L) where L <= 100, trivial. Space O(1) extra.
- Edge cases: lists of length 1 -> run length 1 -> gap = 2 -> area = 4 (if both sides >=2). Works with examples.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxSquare(self, n: int, m: int, hBars: List[int], vBars: List[int]) -> int:
        # helper to compute maximum gap (number of cells) obtainable by removing consecutive bars in arr
        def max_gap_from_removables(arr: List[int]) -> int:
            arr = sorted(arr)
            # longest run of consecutive integers in arr
            max_run = 1
            cur_run = 1
            for i in range(1, len(arr)):
                if arr[i] == arr[i-1] + 1:
                    cur_run += 1
                else:
                    if cur_run > max_run:
                        max_run = cur_run
                    cur_run = 1
            if cur_run > max_run:
                max_run = cur_run
            # removing a run of length k yields a gap of k+1 cells (between the fixed bars around the run)
            return max_run + 1

        h_gap = max_gap_from_removables(hBars)
        v_gap = max_gap_from_removables(vBars)
        side = min(h_gap, v_gap)
        return side * side
```
- Notes:
  - We sort each removable-bars list and find the longest chain of consecutive indices; the obtained gap (cells merged vertically/horizontally) equals chain length + 1.
  - Answer is min(horizontal_gap, vertical_gap)^2 because we need both dimensions to be at least the same side length for a square hole.
  - Time complexity: O(a log a + b log b), where a = len(hBars), b = len(vBars). Since both ≤ 100, this is extremely fast.
  - Space complexity: O(1) extra (besides sorting which may use O(a) / O(b) temporarily).