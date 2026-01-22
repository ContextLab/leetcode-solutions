# [Problem 2463: Minimum Total Distance Traveled](https://leetcode.com/problems/minimum-total-distance-traveled/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The robots and factories lie on a line; each factory has a capacity (limit). We can choose for each robot an initial direction so effectively each robot will end up at some factory (they can pass others that are full). To minimize total distance, it feels natural to sort robots and factories by position and match robots in order to factories in order (some kind of DP / knapsack over factories' capacities). This reminds me of dynamic programming where we process factories one by one and decide how many consecutive robots (from the leftmost remaining) to assign to the current factory. Prefix sums of robot positions will let me compute sum of absolute distances quickly for any block assigned to a factory. Since robot and factory counts ≤ 100, an O(R * M * limit) DP is feasible.

## Refining the problem, round 2 thoughts
- Sort robots ascending and factories ascending by position. After sorting, it's optimal to assign robots in increasing order to factories processed in increasing order (no crossing assignment improvements).
- Use dp[i] = minimum total distance to repair the first i robots after considering some number of factories. For each factory, we try assigning k robots (0..limit) starting from i and update dp[i+k] from dp[i] plus the cost of moving robots[i..i+k-1] to the factory's position.
- Need to compute cost(i, k, pos) = sum_{t=i}^{i+k-1} |robot[t] - pos| efficiently. Precompute prefix sums of robot positions and use binary search within [i, i+k-1] to split robots less-than-or-equal-to pos and greater-than pos; compute left and right parts via prefix sums.
- Time complexity: For R robots and M factories, worst-case O(sum_over_factories(min(limit, R)) * R) ~ O(R * M * R) = O(R^2 * M). With R, M ≤ 100 this is fine.
- Space complexity: O(R) for dp arrays + O(R) for prefix sums.

Edge cases:
- Factories with limit 0 (skip).
- Factories left or right of all considered robots (cost computed correctly via prefix sums).
- Robot can be exactly at factory position (abs = 0) — handle with bisect_right to treat equal positions as left part.

## Attempted solution(s)
```python
import bisect
import math
from typing import List

class Solution:
    def minimumTotalDistance(self, robot: List[int], factory: List[List[int]]) -> int:
        robot.sort()
        factory.sort(key=lambda x: x[0])
        R = len(robot)
        # prefix sums of robot positions
        ps = [0] * (R + 1)
        for i in range(R):
            ps[i+1] = ps[i] + robot[i]

        # dp[i]: min cost to repair first i robots after processing some factories
        INF = 10**30
        dp = [INF] * (R + 1)
        dp[0] = 0

        # For each factory, consider assigning k robots (consecutive from current i)
        for pos, limit in factory:
            # start from current dp; dp2 will be dp after considering this factory
            dp2 = dp[:]  # copying allows "not using this factory" case
            # iterate how many robots already fixed
            for i in range(R + 1):
                if dp[i] >= INF:
                    continue
                # maximum number we can assign to this factory starting at i
                max_k = min(limit, R - i)
                # assign k robots to this factory
                for k in range(1, max_k + 1):
                    l = i
                    r = i + k - 1
                    # find split point m: robots[l..m-1] <= pos, robots[m..r] > pos
                    m = bisect.bisect_right(robot, pos, l, r + 1)
                    # left cost: pos*(m-l) - sum(robot[l..m-1])
                    left_cost = pos * (m - l) - (ps[m] - ps[l])
                    # right cost: sum(robot[m..r]) - pos*(r+1-m)
                    right_cost = (ps[r+1] - ps[m]) - pos * (r + 1 - m)
                    cost = left_cost + right_cost
                    if dp2[i+k] > dp[i] + cost:
                        dp2[i+k] = dp[i] + cost
            dp = dp2

        return dp[R]


# Example usage:
# sol = Solution()
# print(sol.minimumTotalDistance([0,4,6], [[2,2],[6,2]]))  # expected 4
```
- Approach: Sort robots and factories. Use dynamic programming over factories with dp representing how many robots are fixed so far. For each factory, try assigning 0..limit consecutive remaining robots; compute cost for each block using prefix sums and binary search to split around the factory position.
- Time complexity: O(M * R * min(limit, R) * log R) in implementation (the log R from bisect), worst-case O(M * R^2). With R, M ≤ 100 this is easily acceptable.
- Space complexity: O(R) (dp arrays and prefix sums).