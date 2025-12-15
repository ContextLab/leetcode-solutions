# [Problem 2110: Number of Smooth Descent Periods of a Stock](https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I’m sorry — I can’t share my internal chain-of-thought. Instead, here is a concise summary of the approach:

- We want to count all contiguous subarrays where each day (except the first in the subarray) is exactly 1 less than the previous day.
- Equivalent observation: split the array into maximal runs where each adjacent pair differs by -1. For a run of length L, the number of contiguous subarrays inside it is L*(L+1)/2.
- We can compute this in one pass by maintaining the current run length and adding it to the answer at each step.

## Refining the problem, round 2 thoughts
Refinements and edge considerations (concise):
- A single day always counts (run length at least 1).
- When prices[i-1] - prices[i] == 1, extend the current run; otherwise start a new run of length 1.
- Sum run-length contributions incrementally to avoid storing runs explicitly.
- Time complexity O(n), space O(1) beyond input.
- Handle n up to 1e5 — one pass is fine; use 64-bit integer for the answer since sum can be ~ n*(n+1)/2.

## Attempted solution(s)
```python
class Solution:
    def numberOfSmoothDescentPeriods(self, prices: list[int]) -> int:
        # current run length (at least 1 for the current day)
        cur_len = 1
        ans = 0
        for i in range(1, len(prices)):
            if prices[i-1] - prices[i] == 1:
                cur_len += 1
            else:
                # add all subperiods contributed by the previous run
                ans += cur_len * (cur_len + 1) // 2
                cur_len = 1
        # add the last run
        ans += cur_len * (cur_len + 1) // 2
        return ans
```
- Notes:
  - This implementation groups contiguous days where consecutive differences equal -1 into runs. For each run of length L, there are L*(L+1)/2 smooth descent periods.
  - Time complexity: O(n), where n = len(prices).
  - Space complexity: O(1) extra space.
  - Uses integer arithmetic; final answer fits in Python int (arbitrary precision).