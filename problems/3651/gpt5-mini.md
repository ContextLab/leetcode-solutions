# [Problem 3651: Minimum Cost Path with Teleportations](https://leetcode.com/problems/minimum-cost-path-with-teleportations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This problem gives a m x n grid where normal moves (right/down) cost the value of the destination cell, and you can teleport up to k times from any cell (i,j) to any cell (x,y) with grid[x][y] <= grid[i][j] at zero cost. We start at (0,0) with cost 0 and want minimal cost to (m-1,n-1).

First thought: model as shortest-path over states (i,j,t) where t teleports used, and run Dijkstra. That is straightforward conceptually, but teleport edges are dense (from a cell we could teleport to many cells), so explicitly creating all teleport edges would be heavy: up to O((mn)^2) edges, too large.

Observe teleport rule depends only on values (grid[x][y] <= grid[i][j]) and not on positions. Teleports go from cells with larger-or-equal value to cells with smaller-or-equal value (directed toward smaller values). This suggests grouping by value and exploiting monotonic structure. Also note m,n <= 80 and k <= 10 so an algorithm O(k * m * n * log(mn)) or O(k * m * n) is fine.

I think we can iteratively compute dp_t = minimum cost to reach each cell using at most t teleports. For t=0 it's just a simple DP on the directed acyclic grid (right/down). For t >= 1, one teleport can be used somewhere: if you teleport to a cell v of value x, the cost to land at v is min_{u with grid[u] >= x} dp_{t-1}[u] (teleport cost 0). So for each value x we can compute the minimum dp_{t-1} among cells with value >= x (a suffix-min over sorted values). After we set the "landing cost" for every cell (the best cost to be at that cell right after using the new teleport), we still need to propagate normal right/down moves (because after teleporting you continue with normal moves). Since right/down moves form a DAG, we can do a standard DP sweep using those landing costs as initial sources. That gives dp_t. Repeat up to k times.

## Refining the problem, round 2 thoughts
Edge cases:
- Teleport landing does not pay the landing cell's value (teleport cost 0). Only normal moves add cost equal to destination cell's value. So landing cost is exactly dp_{t-1}[u] for some u; landing cell's grid value doesn't add to landing cost.
- We must ensure dp_t <= dp_{t-1} (using more teleports cannot make things worse).
- Implementation details: group cells by value (there are at most mn distinct values), sort values descending, then compute running minimum of dp_{t-1} while iterating descending to get for each value the min dp among >= that value.
- For each t-iteration: O(mn) to compute suffix minima (over groups), O(mn) to run right/down DP sweep. Sorting values can be done once in O(mn log mn). Total complexity O(k * m * n + m * n log(mn)) time and O(mn) extra memory.
- m,n up to 80, k up to 10 => worst ~ 10 * 6400 = 64k cell operations per main loop, fine.

Now implement.

## Attempted solution(s)
```python
from collections import defaultdict
import math
from typing import List

class Solution:
    def minCost(self, grid: List[List[int]], k: int) -> int:
        m = len(grid)
        n = len(grid[0])
        size = m * n
        INF = 10**18

        # Flattened helper
        vals = [grid[i][j] for i in range(m) for j in range(n)]
        # Group indices by value
        value_to_cells = defaultdict(list)
        for idx, v in enumerate(vals):
            value_to_cells[v].append(idx)
        # Unique values sorted descending (we need ">= x" suffix minima)
        unique_vals_desc = sorted(value_to_cells.keys(), reverse=True)

        # Helper to run DP on DAG (right/down) given starting cost for each cell
        def propagate_right_down(start_cost):
            # start_cost: list of length size, start_cost[idx] is cost to be at that cell before paying any right/down move costs
            dp = [INF] * size
            for i in range(m):
                for j in range(n):
                    idx = i * n + j
                    # Option: start here (either from teleport landing or from previous dp value)
                    best = start_cost[idx]
                    if i > 0:
                        best = min(best, dp[(i-1) * n + j] + grid[i][j])
                    if j > 0:
                        best = min(best, dp[i * n + (j-1)] + grid[i][j])
                    dp[idx] = best
            return dp

        # t = 0: no teleports, simple right/down DP starting only at (0,0) cost 0
        dp_prev = [INF] * size
        # Build start_cost where only (0,0) has cost 0 (others INF)
        start0 = [INF] * size
        start0[0] = 0
        dp_prev = propagate_right_down(start0)

        # Iteratively allow one more teleport per iteration up to k
        for _ in range(k):
            # Compute running min of dp_prev for cells with value >= x
            running_min = INF
            value_min_ge = {}  # value -> min dp_prev among cells with value >= value
            for v in unique_vals_desc:
                # include all cells of this value into running_min
                for idx in value_to_cells[v]:
                    if dp_prev[idx] < running_min:
                        running_min = dp_prev[idx]
                value_min_ge[v] = running_min

            # best landing cost for each cell after using one teleport now:
            # landing_cost[cell] = min_{u: grid[u] >= grid[cell]} dp_prev[u]  (which equals value_min_ge[grid[cell]])
            landing_cost = [0] * size
            for idx, v in enumerate(vals):
                landing_cost[idx] = value_min_ge[v]

            # Now dp_cur is the result of propagating right/down moves starting from landing_cost.
            dp_cur = propagate_right_down(landing_cost)

            # If no improvement possible (dp_cur equals dp_prev), we can stop early.
            # But dp_cur should be <= dp_prev; if equal for all cells, further teleports won't help.
            improved = False
            for a, b in zip(dp_cur, dp_prev):
                if a < b:
                    improved = True
                    break
            dp_prev = dp_cur
            if not improved:
                break

        return dp_prev[size - 1]


# If you want to run quick local tests:
if __name__ == "__main__":
    sol = Solution()
    print(sol.minCost([[1,3,3],[2,5,4],[4,3,5]], 2))  # expect 7
    print(sol.minCost([[1,2],[2,3],[3,4]], 1))        # expect 9
```

- Notes about the solution approach:
  - We compute dp_t (min cost to reach each cell using up to t teleports) iteratively.
  - dp_0 is computed by a simple DP over the right/down DAG with starting cost 0 at (0,0).
  - To get dp_t from dp_{t-1}, consider using one teleport: landing at any cell v with value x has cost min_{u : grid[u] >= x} dp_{t-1}[u]. We compute this for each distinct value by iterating values in descending order and maintaining a running minimum over dp_{t-1}.
  - Treat these landing costs as starting sources and propagate right/down moves (again a DAG DP). The resulting distances are dp_t.
  - Repeat up to k times; stop early if another teleport iteration yields no improvement.

- Complexity:
  - Time: O(m * n * log(m*n)) to sort values once + O(k * m * n) for k iterations (each iteration does suffix minima and one right/down DP sweep). With constraints m,n <= 80 and k <= 10 this is easily efficient.
  - Space: O(m * n) extra for dp arrays and grouping structures.

This approach avoids explicit heavy teleport graph construction and leverages the value-only dependence of teleports to get an efficient solution.