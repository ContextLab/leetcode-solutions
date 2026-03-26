# [Problem 3548: Equal Sum Grid Partition II](https://leetcode.com/problems/equal-sum-grid-partition-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to cut the grid once (horizontal between two rows or vertical between two columns) so both sides have equal sums OR can be made equal by discounting (removing) at most one single cell (from either side). If a cell is removed, the remaining cells of that section must stay connected.

A cut produces a rectangular top/bottom (for horizontal) or left/right (for vertical) section. The main checks per cut are:
- If sums are already equal → success.
- Otherwise, compute diff = |sumA - sumB|. We must remove a single cell of value diff from the larger side so sums match. The removed cell must lie inside that side, and removing it must not disconnect the side.

When does removing a single cell disconnect a rectangular subgrid?
- If both dimensions of the rectangle are at least 2, removing any single vertex does NOT disconnect a grid rectangle (grid graphs are 2-vertex-connected when both height and width ≥ 2). So in that case any cell of value diff anywhere in the rectangle is acceptable.
- If one dimension equals 1 (the subgrid is a 1 x W row or H x 1 column), removing a middle cell splits it into two components (disallowed). Only removing an endpoint (leftmost/rightmost in a row or topmost/bottommost in a column) keeps the remainder connected. Also, you cannot remove the only cell if the subgrid has area 1 (that would leave an empty remainder; that is invalid).

So we need to efficiently:
- iterate all possible horizontal and vertical cuts,
- compute sums quickly (prefix sums over rows / cols),
- for a given value diff, determine if there exists a cell with that value inside the required row/column range (or at the allowed endpoints when the subgrid is a single row/column).

We can preprocess maps:
- value -> sorted list of rows where this value appears (for horizontal checks),
- value -> sorted list of cols where this value appears (for vertical checks).
Then binary search to test if a value appears within a row/column interval.

This is O(N log N) preprocessing and O((m+n) log N) checks, where N = m * n ≤ 1e5.

## Refining the problem, round 2 thoughts
Edge cases and careful points:
- When diff == 0 we immediately return True.
- The side from which we remove a cell must have area ≥ 2 to allow removal (else remainder becomes empty).
- If subgrid has height==1 but width≥2, only check the two endpoint cells in that row within the subgrid (column 0 or n-1 in original indexing, or left/right endpoints of that side).
- Similarly, if width==1 but height≥2 (single column), only check topmost/bottommost cells of that side.
- For general-case (min(height,width) >= 2) we just need to know if any occurrence of diff exists in the row-range (horizontal) or col-range (vertical).
- Precompute row sums and col sums and their prefixes to compute sums for each cut in O(1).

Time complexity:
- Build maps and sort lists: O(N log N).
- Evaluate up to (m-1) horizontal + (n-1) vertical cuts; for each we do O(log N) binary searches or O(1) checks. Total O((m+n) log N).
Space: O(N) for mappings plus row/col arrays.

Now the implementation.

## Attempted solution(s)
```python
from collections import defaultdict
from bisect import bisect_left

class Solution:
    def equalSumGridPartition(self, grid: list[list[int]]) -> bool:
        m = len(grid)
        n = len(grid[0])
        N = m * n

        # Row sums and prefix
        row_sums = [sum(row) for row in grid]
        pref_rows = [0] * m
        s = 0
        for i in range(m):
            s += row_sums[i]
            pref_rows[i] = s
        total = s

        # Col sums and prefix
        col_sums = [0] * n
        for j in range(n):
            col_sums[j] = sum(grid[i][j] for i in range(m))
        pref_cols = [0] * n
        s = 0
        for j in range(n):
            s += col_sums[j]
            pref_cols[j] = s

        # Build value -> list of rows and value -> list of cols
        val_to_rows = defaultdict(list)
        val_to_cols = defaultdict(list)
        for i in range(m):
            for j in range(n):
                v = grid[i][j]
                val_to_rows[v].append(i)
                val_to_cols[v].append(j)
        # sort lists for binary search
        for lst in val_to_rows.values():
            lst.sort()
        for lst in val_to_cols.values():
            lst.sort()

        def any_value_in_row_range(val, r0, r1):
            """Return True if value 'val' appears in any row within [r0, r1]."""
            if val not in val_to_rows:
                return False
            rows = val_to_rows[val]
            i = bisect_left(rows, r0)
            return i < len(rows) and rows[i] <= r1

        def any_value_in_col_range(val, c0, c1):
            """Return True if value 'val' appears in any column within [c0, c1]."""
            if val not in val_to_cols:
                return False
            cols = val_to_cols[val]
            i = bisect_left(cols, c0)
            return i < len(cols) and cols[i] <= c1

        # Check horizontal cuts (cut between r and r+1, r = 0..m-2)
        for r in range(m - 1):
            top_sum = pref_rows[r]
            bottom_sum = total - top_sum
            if top_sum == bottom_sum:
                return True
            diff = abs(top_sum - bottom_sum)
            # larger side info
            if top_sum > bottom_sum:
                # larger is top: rows [0..r]
                rs, re = 0, r
                H = r + 1
            else:
                # larger is bottom: rows [r+1..m-1]
                rs, re = r + 1, m - 1
                H = m - (r + 1)
            W = n
            area = H * W
            # cannot remove the only cell of the side (would leave empty remainder)
            if area <= 1:
                continue
            # if both dimensions >= 2, any cell is safe to remove (check existence of value in row range)
            if H >= 2 and W >= 2:
                if any_value_in_row_range(diff, rs, re):
                    return True
            else:
                # one dimension == 1 -> either single row or single column
                if H == 1 and W >= 2:
                    row = rs  # single row index
                    # only endpoints of the row keep connectivity after removal
                    if grid[row][0] == diff or grid[row][n - 1] == diff:
                        return True
                elif W == 1 and H >= 2:
                    col = 0  # single column
                    # endpoints in rows rs and re
                    if grid[rs][col] == diff or grid[re][col] == diff:
                        return True

        # Check vertical cuts (cut between c and c+1, c = 0..n-2)
        for c in range(n - 1):
            left_sum = pref_cols[c]
            right_sum = total - left_sum
            if left_sum == right_sum:
                return True
            diff = abs(left_sum - right_sum)
            if left_sum > right_sum:
                cs, ce = 0, c
                W = c + 1
            else:
                cs, ce = c + 1, n - 1
                W = n - (c + 1)
            H = m
            area = H * W
            if area <= 1:
                continue
            if H >= 2 and W >= 2:
                if any_value_in_col_range(diff, cs, ce):
                    return True
            else:
                # single row (H == 1) or single column (W == 1)
                if W == 1 and H >= 2:
                    col = cs  # single column index
                    # only top/bottom endpoints allowed in that column
                    if grid[0][col] == diff or grid[m - 1][col] == diff:
                        # careful: endpoints must be inside the side range:
                        # if side is left (cs==0) the top endpoint is (0,col) and bottom is (m-1,col),
                        # but we need endpoints within rows [0..m-1], always true; however we should
                        # restrict to endpoints of the side: rows rs..re.
                        # Derive side row-range:
                        rs, re = 0, m - 1
                        # actual endpoints of the side are rows rs and re (full column),
                        # but we must check the specific rows inside this side:
                        # The side's vertical endpoints are rs..re; left/right side covers all rows,
                        # so endpoints are rs and re (0 and m-1). We should check those two positions:
                        if grid[rs][col] == diff or grid[re][col] == diff:
                            return True
                elif H == 1 and W >= 2:
                    row = 0  # single row
                    # endpoints in this row are cs and ce
                    if grid[row][cs] == diff or grid[row][ce] == diff:
                        return True

        return False


# Example usage (LeetCode will call the function in a different format):
# To adapt to LeetCode format:
class Solution_LeetCode:
    def equalSumGridPartition(self, grid: list[list[int]]) -> bool:
        return Solution().equalSumGridPartition(grid)

# On LeetCode you'd implement:
# class Solution:
#     def equalSumGridPartition(self, grid: List[List[int]]) -> bool:
#         ...same code...

```

- Notes about approach:
  - We reduce the problem to checking each possible single straight cut (horizontal or vertical) and then checking whether either sums already match or removing one cell of value equal to the difference from the larger side can make them match while preserving connectivity.
  - Key graph/geometry observation: a rectangular subgrid with both height and width ≥ 2 is 2-vertex-connected, so removing any single cell leaves it connected. Only 1×W or H×1 strips have articulation vertices; in those cases only endpoint removals are allowed.
  - Preprocessing value → sorted rows/cols lists allows O(log N) detection of whether a needed value exists within a row or column interval.
  - Time complexity: O(N log N) preprocessing (building mappings + sorting) + O((m + n) log N) for checking all cuts. Space: O(N).
  - Careful with edge cases: do not allow removal that leaves the section empty (area == 1).