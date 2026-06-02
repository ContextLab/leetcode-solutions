# [Problem 3633: Earliest Finish Time for Land and Water Rides I](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to pick exactly one land ride and one water ride, in either order, and minimize the finish time. Each ride can start at its opening time or any later time; starting later than the earliest opening never helps because durations are positive, so for a chosen order we should always start each ride as early as possible (either at its opening time or immediately after finishing the previous ride). That suggests enumerating pairs of (land i, water j) and computing two finish times: land->water and water->land, taking the minimum over all pairs.

Because n,m ≤ 100, an O(n*m) pairwise check is cheap and straightforward.

## Refining the problem, round 2 thoughts
Edge cases: single-element arrays (n=1 or m=1) handled naturally by the loops. Times and durations are positive integers so no complications of zero or negative durations. Implementation detail: compute finish time of first ride, then start second at max(secondStartTime, firstFinish), then add its duration. Do both orders for each pair and keep global minimum. Time complexity O(n*m), space O(1). This is simple and optimal for constraints.

## Attempted solution(s)
```python
from typing import List
import math

class Solution:
    def earliestFinishTime(self, landStartTime: List[int], landDuration: List[int],
                           waterStartTime: List[int], waterDuration: List[int]) -> int:
        """
        For each pair (i, j) compute finish time for order:
          - land i then water j
          - water j then land i
        Return the minimum finish time found.
        """
        ans = math.inf
        n = len(landStartTime)
        m = len(waterStartTime)
        for i in range(n):
            l_start = landStartTime[i]
            l_duration = landDuration[i]
            l_finish = l_start + l_duration
            for j in range(m):
                w_start = waterStartTime[j]
                w_duration = waterDuration[j]

                # land -> water
                start_water = max(w_start, l_finish)
                finish_land_then_water = start_water + w_duration
                if finish_land_then_water < ans:
                    ans = finish_land_then_water

                # water -> land
                finish_water = w_start + w_duration
                start_land = max(l_start, finish_water)
                finish_water_then_land = start_land + l_duration
                if finish_water_then_land < ans:
                    ans = finish_water_then_land

        return int(ans)
```
- Approach: brute-force over all pairs, compute both possible orders, and keep the minimum finish time.
- Time complexity: O(n * m) where n = len(landStartTime), m = len(waterStartTime).
- Space complexity: O(1) extra space.
- Important detail: always starting a chosen ride as soon as possible (its opening time or right after previous finish) is optimal because waiting longer only increases finish time.