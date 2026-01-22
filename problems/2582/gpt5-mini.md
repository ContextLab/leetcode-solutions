# [Problem 2582: Pass the Pillow](https://leetcode.com/problems/pass-the-pillow/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The pillow moves along the line 1 → 2 → ... → n, then back n → n-1 → ... → 1, repeating. That looks like a periodic motion. One naive approach is to simulate second-by-second, but since time ≤ 1000 and n ≤ 1000 simulation would be fine. However, there's an obvious pattern: the movement repeats every 2*(n-1) seconds (go to the end and back). So we can use modulo arithmetic to find the position without simulating each step. Need to handle the forward and backward segments carefully (and the case where time is exactly a multiple of the period).

## Refining the problem, round 2 thoughts
Let period = 2*(n-1). Compute r = time % period. If r is in [0, n-1], the pillow is on the forward pass at position 1 + r (with r=0 meaning it's at person 1). If r is in (n-1, period-1], it's on the backward pass; the distance past the end is r - (n-1) and the position is n - (r - (n-1)). Edge cases: n = 2 (period = 2) works fine; time exactly a multiple of period gives r = 0 → position 1. Complexity: O(1) time and O(1) space.

## Attempted solution(s)
```python
class Solution:
    def passThePillow(self, n: int, time: int) -> int:
        # period of a full forward+backward cycle
        period = 2 * (n - 1)
        r = time % period
        if r <= (n - 1):
            return 1 + r
        else:
            # on the backward pass
            return n - (r - (n - 1))
```
- Notes:
  - Approach: Use the periodicity of the motion (period = 2*(n-1)) and compute the remainder r = time % period to determine where in the cycle we are. If r <= n-1 we're moving forward from person 1; otherwise we're moving backward from person n.
  - Time complexity: O(1).
  - Space complexity: O(1).
  - Works for all constraints (2 <= n <= 1000, 1 <= time <= 1000).