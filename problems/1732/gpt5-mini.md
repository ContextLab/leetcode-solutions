# [Problem 1732: Find the Highest Altitude](https://leetcode.com/problems/find-the-highest-altitude/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is straightforward: we start at altitude 0 and each gain[i] moves us to the next point. The altitudes are just the prefix sums of the gains, starting with 0. So compute cumulative altitude after each gain and track the maximum seen. Edge cases that come to mind: all negatives (max should be 0 at the start), single element arrays, and arrays with all positives.

## Refining the problem, round 2 thoughts
We don't need to store the whole list of altitudes; we can maintain a running sum (current altitude) and a variable for the maximum altitude. Time complexity should be O(n) where n = len(gain), and space complexity O(1) extra beyond input. An alternative is using itertools.accumulate to produce prefix sums, but manual accumulation is clearer and avoids imports. Constraints are small (n <= 100), so any linear solution is fine.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        # Start at altitude 0
        current_alt = 0
        max_alt = 0
        
        # Add each gain and update maximum altitude
        for g in gain:
            current_alt += g
            if current_alt > max_alt:
                max_alt = current_alt
        
        return max_alt
```
- Notes:
  - Approach: iterate through gain, maintain running sum (current altitude) and update the maximum altitude seen.
  - Time complexity: O(n), n = len(gain), because we traverse the array once.
  - Space complexity: O(1) extra space (only two integers used).
  - Important detail: include the starting altitude 0 in consideration — since max_alt is initialized to 0, if all gains are negative the result correctly remains 0.