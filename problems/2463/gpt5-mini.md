# [Problem 2463: Minimum Total Distance Traveled](https://leetcode.com/problems/minimum-total-distance-traveled/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have robots at various positions and factories with positions and capacity limits. Each robot must be assigned to some factory; it will move in whichever direction to reach its assigned factory and the cost for that robot is the absolute distance to the factory. We can set each robot's initial moving direction arbitrarily, so effectively each robot can go to any factory and cost is |robot_pos - factory_pos| (no collisions or interactions change costs). The only constraint is the per-factory capacity.

This is an assignment problem on a line with capacities. Sorting robots and factories by position should help because robots assigned to earlier factories will be a prefix of the sorted robots when we process factories left-to-right (we can enforce an ordering: assign robots in increasing order to factories in increasing order). That suggests dynamic programming: dp[i][j] = min cost to repair first i robots using first j factories. Because R,F ≤ 100, an O(R * F * limit) DP is feasible. We can implement it in one-dimensional DP over number of robots processed and iterate factories.

Compute incremental cost of assigning the next k robots to the current factory by summing absolute distances; since sizes are small we can incrementally accumulate cost rather than complex prefix-sum handling.

## Refining the problem, round 2 thoughts
- Sort robots ascending and factories ascending by position.
- Use DP where dp[i] is min cost to repair first i robots after processing some factories; for each factory we build ndp by trying to assign k robots (0..limit and within remaining robots) starting from each possible i.
- For each i, maintain incremental cost when adding one more robot to this factory: cost += abs(robot[i+k-1] - factory_pos).
- Initialize dp[0] = 0 and dp[>0] = inf. After processing all factories the answer is dp[R].
- Edge cases: some factories may have limit 0 (we just skip assigning any robots to them). The input promises a feasible assignment (so dp[R] will be finite).
- Complexity: there are at most R robots and F factories and each factory can assign up to its limit (≤ R); overall complexity O(F * R * max_limit) ≤ O(F * R^2) which with 100 each is fine (~1e6 iterations). Space O(R).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumTotalDistance(self, robot: List[int], factory: List[List[int]]) -> int:
        robot.sort()
        # sort factories by position
        factory.sort(key=lambda x: x[0])
        R = len(robot)
        INF = 10**30
        # dp[i] = min cost to repair first i robots after processing some factories
        dp = [INF] * (R + 1)
        dp[0] = 0

        for pos, limit in factory:
            ndp = [INF] * (R + 1)
            for i in range(R + 1):
                if dp[i] == INF:
                    continue
                # option: assign 0 robots from i to this factory
                if dp[i] < ndp[i]:
                    ndp[i] = dp[i]
                # try assigning k robots starting at index i
                cost = 0
                maxk = min(limit, R - i)
                for k in range(1, maxk + 1):
                    cost += abs(robot[i + k - 1] - pos)
                    # update ndp for i+k robots assigned after using this factory
                    if dp[i] + cost < ndp[i + k]:
                        ndp[i + k] = dp[i] + cost
            dp = ndp

        return dp[R]
```
- Notes on approach:
  - We sort robots and factories by position so we can process factories left-to-right and assign robots in order. The DP enforces that assignments to factories respect robot ordering: when processing factory j we only consider assigning a contiguous block of next robots.
  - The inner loop incrementally computes the cost of assigning 1 more robot to the current factory, keeping the implementation simple and efficient for the given constraints.

- Complexity:
  - Time: O(F * R * L) where L is average limit (worst-case L = R), so worst-case O(F * R^2). For R,F ≤ 100 this is easily within limits (~1e6 iterations).
  - Space: O(R) for dp arrays.