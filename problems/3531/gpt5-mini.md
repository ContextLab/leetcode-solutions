# [Problem 3531: Count Covered Buildings](https://leetcode.com/problems/count-covered-buildings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count buildings that have at least one building in all four cardinal directions (left/right on same row, above/below on same column). The building coordinates are unique. A naive approach that for each building scans all others to check existence in those directions would be O(m^2) for m = number of buildings — too slow for up to 1e5.

Observing structure: "left" and "right" mean there is at least one building with same x and smaller y, and same x and larger y. So for each row (fixed x) if we sort the y positions, any building that is not the first nor the last in that sorted list has both a left and a right neighbor somewhere in that row. Similarly for columns: sort x positions per column (fixed y); any building not first/last has both above and below. So we can mark which coordinates are interior in their row and which are interior in their column. The buildings that are interior in both sets are covered.

This suggests grouping by row and by column, sorting each group's coordinates, marking interior points, and then counting intersection. Complexity will be dominated by sorting the grouped lists (total O(m log m)).

## Refining the problem, round 2 thoughts
- Implementation: use two dicts (defaultdict(list)) rows[x] -> list of ys, cols[y] -> list of xs.
- After filling, sort each list. For each row list with length >= 3, add all ys except first and last to a set of covered-in-row points (store as tuple (x,y)). For columns similarly produce covered-in-col set.
- The answer is the size of intersection of these two sets.
- Edge cases: rows or columns with length < 3 contribute no interior points. Unique coordinates guarantee no duplicates.
- Complexity: building lists O(m), sorting across all groups O(m log m) (sum of Li log Li ≤ m log m), marking interiors O(m), final intersection O(min(|A|,|B|)) ≤ O(m). Space O(m).

## Attempted solution(s)
```python
from collections import defaultdict
from typing import List

class Solution:
    def countCoveredBuildings(self, n: int, buildings: List[List[int]]) -> int:
        # Group by row and by column
        rows = defaultdict(list)  # x -> list of y
        cols = defaultdict(list)  # y -> list of x
        
        for x, y in buildings:
            rows[x].append(y)
            cols[y].append(x)
        
        covered_row = set()
        covered_col = set()
        
        # For each row, mark interior buildings (have both left and right)
        for x, ys in rows.items():
            if len(ys) < 3:
                continue
            ys.sort()
            # all except first and last are interior in row
            for y in ys[1:-1]:
                covered_row.add((x, y))
        
        # For each column, mark interior buildings (have both above and below)
        for y, xs in cols.items():
            if len(xs) < 3:
                continue
            xs.sort()
            # all except first and last are interior in column
            for x in xs[1:-1]:
                covered_col.add((x, y))
        
        # Covered buildings are those interior in both row and column
        return len(covered_row & covered_col)
```
- Notes:
  - Approach groups buildings by row and column and uses sorted order to determine whether a building has at least one neighbor on both sides along that axis.
  - Time complexity: O(m log m) where m = number of buildings (sorting dominates).
  - Space complexity: O(m) to store groups and sets.
  - Implementation details: store coordinates as tuples (x, y) in sets for quick intersection; only rows/columns with length >= 3 can produce interior points.