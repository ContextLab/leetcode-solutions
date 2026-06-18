# [Problem 1344: Angle Between Hands of a Clock](https://leetcode.com/problems/angle-between-hands-of-a-clock/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the smaller angle between hour and minute hands. The minute hand moves 360 degrees in 60 minutes -> 6 degrees per minute. The hour hand moves 360 degrees in 12 hours -> 30 degrees per hour, but it also moves as minutes pass: that's 30 degrees per hour + 0.5 degrees per minute (30/60). So hour angle = (hour % 12) * 30 + minutes * 0.5, minute angle = minutes * 6. Then take absolute difference and ensure we return the smaller of that and 360 - that. Watch out for hour == 12 mapping to 0. Minutes range 0..59. Return value should be float; the problem accepts small floating errors.

## Refining the problem, round 2 thoughts
Edge cases: hour = 12 should be treated as 0. minutes = 0 should produce multiples of 30. When difference > 180 we must use 360 - diff to get the smaller angle. Precision: using floats with simple arithmetic is fine; problem allows 1e-5 tolerance. Complexity is trivial: O(1) time and O(1) space. There's no need for simulation or iterative approaches. Implementation should be concise; wrap in LeetCode's class Solution with method angleClock.

## Attempted solution(s)
```python
class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        # Normalize hour to 0-11
        hour = hour % 12
        # Minute hand: 6 degrees per minute
        minute_angle = minutes * 6.0
        # Hour hand: 30 degrees per hour + 0.5 degrees per minute
        hour_angle = hour * 30.0 + minutes * 0.5
        # Absolute difference
        diff = abs(hour_angle - minute_angle)
        # Return the smaller angle
        if diff > 180.0:
            diff = 360.0 - diff
        return diff
```
- Notes:
  - Approach: compute angles of each hand directly using constant-rate relations, then return the minimal angular separation.
  - Correctness: hour mapped to 0..11 handles 12 properly. Using 0.5 deg per minute for the hour hand accounts for fractional movement.
  - Time complexity: O(1). Space complexity: O(1).
  - Floating-point precision is adequate for the required 1e-5 tolerance.