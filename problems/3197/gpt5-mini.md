# [Problem 3197: Find the Minimum Area to Cover All Ones II](https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need three non-overlapping axis-aligned rectangles (non-zero area) that together cover all 1's in the grid, minimizing the sum of areas. Grid size is up to 30x30, so O(n^4) or slightly higher DP across subrectangles is plausible. A natural approach: dynamic programming over submatrices. For any submatrix we can ask: what's the minimum total area to cover all 1's inside it using exactly k rectangles? Because rectangles are non-overlapping, if we split a submatrix by a horizontal/vertical cut, solutions on the two sides won't overlap. Base case k = 1: we must use a single rectangle to cover all 1's inside the submatrix — the optimal single rectangle is the bounding box of all 1's in that submatrix. For k > 1, try all possible splits and distribute rectangles among the two parts.

We must ensure each rectangle used in the final solution has non-zero area. Because the input guarantees at least 3 ones, the optimal solution will place each rectangle to contain at least one one (otherwise it would waste area). So when distributing rectangles across a split we should only consider splits where both sides contain at least one 1 for any positive number of rectangles assigned to that side.

This yields a memoized DP over states (r1, c1, r2, c2, k). Number of submatrices is O(n^2 * m^2) and k is 3, so number of states is manageable. For each state we try up to O(n+m) splits; total operations remain feasible for n,m ≤ 30.

## Refining the problem, round 2 thoughts
Edge cases:
- A submatrix may contain no 1's. If k == 0, cost = 0; if k > 0 we should treat it as infeasible (return INF) because we don't want to allocate a positive number of rectangles to an empty region (those rectangles would have to have non-zero area but would contain no ones and only increase cost — and in optimal solution each rectangle should contain at least one 1).
- For k == 1 and submatrix contains ones, area equals bounding box area of ones inside that submatrix.
- When splitting and distributing rectangles (for example k=3), allow splits that distribute (1,2) and (2,1), but only if both sides have ones.
- We must compute quickly whether a submatrix has any 1 and also the bounding box of ones inside a submatrix; precompute row-wise and column-wise prefix sums (and a 2D prefix sum for quick emptiness check). When computing bounding box within a submatrix, scan rows (up to 30) and columns (up to 30) which is cheap given state count.

Time/space:
- Number of submatrix states ≈ O(n^2 m^2) ≤ (30^4) ~ 810k; times k (3) ~ 2.4M states considered.
- Each state checks O(n + m) possible splits; overall operations on the order of tens of millions — fine in Python with careful implementation and memoization.
- Memory: memo dictionary keyed by tuples; feasible.

## Attempted solution(s)
```python
from functools import lru_cache
import sys

def solve(grid):
    # Entry helper so we can run locally or on LeetCode style platform
    n = len(grid)
    m = len(grid[0])
    INF = 10**12

    # rowPrefix[r][c] = number of ones in row r in columns [0..c-1]
    rowPrefix = [[0] * (m + 1) for _ in range(n)]
    # colPrefix[c][r] = number of ones in column c in rows [0..r-1]
    colPrefix = [[0] * (n + 1) for _ in range(m)]
    # 2D prefix sum for quick submatrix emptiness check
    ps = [[0] * (m + 1) for _ in range(n + 1)]

    for r in range(n):
        for c in range(m):
            rowPrefix[r][c+1] = rowPrefix[r][c] + grid[r][c]
            colPrefix[c][r+1] = colPrefix[c][r] + grid[r][c]
            ps[r+1][c+1] = ps[r+1][c] + ps[r][c+1] - ps[r][c] + grid[r][c]

    def hasAny(r1, c1, r2, c2):
        # inclusive coordinates
        return (ps[r2+1][c2+1] - ps[r1][c2+1] - ps[r2+1][c1] + ps[r1][c1]) > 0

    def bboxArea(r1, c1, r2, c2):
        # returns minimal bounding box area that covers all ones inside submatrix,
        # or 0 if no ones
        if not hasAny(r1, c1, r2, c2):
            return 0
        # find topmost row with any 1 in [c1..c2]
        for rr in range(r1, r2 + 1):
            if rowPrefix[rr][c2+1] - rowPrefix[rr][c1] > 0:
                minR = rr
                break
        # find bottommost row
        for rr in range(r2, r1 - 1, -1):
            if rowPrefix[rr][c2+1] - rowPrefix[rr][c1] > 0:
                maxR = rr
                break
        # find leftmost col
        for cc in range(c1, c2 + 1):
            if colPrefix[cc][r2+1] - colPrefix[cc][r1] > 0:
                minC = cc
                break
        # find rightmost col
        for cc in range(c2, c1 - 1, -1):
            if colPrefix[cc][r2+1] - colPrefix[cc][r1] > 0:
                maxC = cc
                break
        return (maxR - minR + 1) * (maxC - minC + 1)

    sys.setrecursionlimit(10000)

    @lru_cache(None)
    def dp(r1, c1, r2, c2, k):
        # minimal total area to cover all ones in submatrix [r1..r2][c1..c2] using exactly k rectangles
        # rectangles must be non-overlapping and have non-zero areas.
        if r1 > r2 or c1 > c2:
            return 0 if k == 0 else INF
        if not hasAny(r1, c1, r2, c2):
            # if there are no ones:
            return 0 if k == 0 else INF  # can't place meaningful rectangles here
        if k == 1:
            # single rectangle — bounding box area of all ones in this submatrix
            return bboxArea(r1, c1, r2, c2)

        res = INF
        # horizontal splits
        for mid in range(r1, r2):
            # Only consider splits where both sides have at least one 1 when receiving >=1 rectangles.
            top_has = hasAny(r1, c1, mid, c2)
            bot_has = hasAny(mid+1, c1, r2, c2)
            if not (top_has and bot_has):
                continue
            # distribute k rectangles between the two parts; each side must get at least 1
            for t in range(1, k):
                left_cost = dp(r1, c1, mid, c2, t)
                if left_cost >= INF:
                    continue
                right_cost = dp(mid+1, c1, r2, c2, k - t)
                if right_cost >= INF:
                    continue
                cand = left_cost + right_cost
                if cand < res:
                    res = cand

        # vertical splits
        for mid in range(c1, c2):
            left_has = hasAny(r1, c1, r2, mid)
            right_has = hasAny(r1, mid+1, r2, c2)
            if not (left_has and right_has):
                continue
            for t in range(1, k):
                left_cost = dp(r1, c1, r2, mid, t)
                if left_cost >= INF:
                    continue
                right_cost = dp(r1, mid+1, r2, c2, k - t)
                if right_cost >= INF:
                    continue
                cand = left_cost + right_cost
                if cand < res:
                    res = cand

        return res

    ans = dp(0, 0, n-1, m-1, 3)
    return ans

# Use the solve function as the core solution entry expected by LeetCode:
class Solution:
    def minimumArea(self, grid: list[list[int]]) -> int:
        return solve(grid)

# If running locally to test:
if __name__ == "__main__":
    s = Solution()
    print(s.minimumArea([[1,0,1],[1,1,1]]))  # expected 5
    print(s.minimumArea([[1,0,1,0],[0,1,0,1]]))  # expected 5
```

- Notes about the approach:
  - We use a DP over submatrices (r1,c1,r2,c2) and an exact rectangle count k in that submatrix.
  - Base case k==1: area is the bounding box of all 1's inside the submatrix. If submatrix has no 1's and k>0, return INF (invalid), while if k==0 return 0.
  - For k>1: try all horizontal and vertical cuts; require both sides to contain ones when they receive ≥1 rectangles. Distribute rectangle counts between sides (for k=3 that's t=1 or 2).
  - We memoize results with lru_cache to avoid recomputation.
- Complexity:
  - Number of submatrix states is O(n^2 m^2), and k is a small constant (3). For each state we try up to O(n + m) splits. Overall time complexity about O(k * n^2 * m^2 * (n + m)), which is acceptable for n,m ≤ 30.
  - Space complexity dominated by memoization table O(n^2 m^2 * k) plus prefix arrays.
- Implementation details:
  - 2D prefix sums and row/column prefix sums are used for quick emptiness checks and efficient detection of whether a row/column segment contains any 1.
  - bboxArea scans up to O(n + m) rows/cols to find the tight bounding box within a submatrix — cheap given constraints.
  - We ensure that rectangles used in the DP each cover at least one 1 (by forbidding giving rectangles to empty partitions), which is safe since input contains at least 3 ones and optimal solution will assign each rectangle to at least one 1.