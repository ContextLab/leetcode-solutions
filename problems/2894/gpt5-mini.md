# [Problem 2894: Divisible and Non-divisible Sums Difference](https://leetcode.com/problems/divisible-and-non-divisible-sums-difference/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Brute force idea: iterate 1..n, accumulate two sums depending on divisibility by m. That would work given constraints (n <= 1000), but there's a direct formula using arithmetic series sums that is cleaner and O(1).

Observations:
- Total sum S of 1..n is n*(n+1)/2.
- Let k = n // m be the count of multiples of m in [1..n].
- Sum of multiples of m is m * (1 + 2 + ... + k) = m * k*(k+1)/2.
- num1 (non-divisible sum) = S - sum_div, num2 = sum_div. So result = (S - sum_div) - sum_div = S - 2*sum_div.

Edge cases: m > n (k = 0 -> sum_div = 0), m = 1 (all numbers divisible -> result = -S).

## Refining the problem, round 2 thoughts
- Use integer arithmetic with // to avoid any floating operations.
- Complexity becomes O(1) time and O(1) space.
- Python handles large integers safely; given constraints it's trivial anyway.
- Confirm formula correctness with examples:
  - Example 1: n=10, m=3 -> S=55, k=3, sum_div=3*(3*4/2)=18 -> ans=55-36=19 matches.
  - Example 2: n=5, m=6 -> k=0 sum_div=0 ans=15.
  - Example 3: n=5, m=1 -> k=5 sum_div=15 ans=55-30= -15? Wait recalc: S=15 not 55; sum_div=15, ans=15-30=-15 matches.

## Attempted solution(s)
```python
class Solution:
    def differenceOfSums(self, n: int, m: int) -> int:
        # Total sum from 1 to n
        total = n * (n + 1) // 2
        # Count of multiples of m in [1..n]
        k = n // m
        # Sum of multiples of m: m * (1 + 2 + ... + k) = m * k*(k+1)//2
        sum_div = m * k * (k + 1) // 2
        # num1 - num2 = (total - sum_div) - sum_div = total - 2*sum_div
        return total - 2 * sum_div
```
- Notes:
  - Approach: Use arithmetic series formulas to compute sums in O(1) time.
  - Time complexity: O(1).
  - Space complexity: O(1).
  - Implementation details: Use integer division (//) to keep values integral; Python's integers handle any size needed given constraints.