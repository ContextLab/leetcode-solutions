# [Problem 1716: Calculate Money in Leetcode Bank](https://leetcode.com/problems/calculate-money-in-leetcode-bank/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a straightforward arithmetic-sum problem. Hercy deposits money each day with a repeating weekly pattern where each week starts at a Monday value that increases by 1 from the previous Monday, and within a week values increase by 1 each day. That suggests we can treat the input as a number of full weeks plus some remaining days. For full weeks, each week's sum is an arithmetic progression (starts at 1, length 7), and each subsequent week shifts that progression up by 1. For remaining days we can compute the partial week's sum similarly. A direct simulation (looping day-by-day) would be simple and fine for n <= 1000, but we can derive a closed-form formula to compute the result in O(1).

## Refining the problem, round 2 thoughts
Let w = n // 7 (number of full weeks) and r = n % 7 (remaining days).
- Sum of a single base week (week 0) is 1+2+...+7 = 28.
- Week i (0-based) starts at 1 + i, so its sum = 7*(1+i) + (0+1+...+6) = 7*(1+i) + 21 = 28 + 7*i.
- Sum over w full weeks = sum_{i=0..w-1} (28 + 7*i) = 28*w + 7*(w*(w-1)/2).
- Remaining r days start at value (1 + w). Their sum = r*(1+w) + sum_{k=0..r-1} k = r*(1+w) + r*(r-1)/2.
Combine these for the final closed-form result. Edge cases: small n (<7) where w=0 handle naturally, r can be 0 as well. Complexity O(1) time, O(1) space. A simulation loop would be O(n) time, O(1) space and is acceptable for the constraints but unnecessary.

## Attempted solution(s)
```python
class Solution:
    def totalMoney(self, n: int) -> int:
        # number of full weeks and remaining days
        w = n // 7
        r = n % 7

        # sum for full weeks:
        #  - each week base sum is 28
        #  - weeks increment by 7*i for week i (0-based)
        full_weeks_sum = 28 * w + 7 * (w * (w - 1) // 2)

        # sum for remaining days:
        #  - each remaining day starts at (1 + w), and increases by 1 each day
        rem_sum = r * (1 + w) + (r * (r - 1) // 2)

        return full_weeks_sum + rem_sum
```
- Notes:
  - Approach: arithmetic closed-form using decomposition into full weeks and leftover days.
  - Time complexity: O(1). All operations are constant-time arithmetic.
  - Space complexity: O(1). Only a few integer variables used.
  - Correctness: validated on the examples (n=4 -> 10, n=10 -> 37, n=20 -> 96). A simple simulation loop would also work and is acceptable given n <= 1000, but the formula is cleaner and constant-time.