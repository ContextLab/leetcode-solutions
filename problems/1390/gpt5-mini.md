# [Problem 1390: Four Divisors](https://leetcode.com/problems/four-divisors/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want to find numbers in the array that have exactly 4 divisors and sum those divisors. Numbers with exactly four divisors are typically either:
- product of two distinct primes p * q (divisors: 1, p, q, p*q), or
- a cube of a prime p^3 (divisors: 1, p, p^2, p^3).

A straightforward approach is to enumerate divisors for each number up to sqrt(n) and count them; if more than 4 divisors are discovered we can stop early. Given constraints (nums.length <= 1e4, nums[i] <= 1e5), checking up to sqrt(1e5) ~ 316 per number is fine.

Alternative would be to precompute primes and detect p*q or p^3 via factorization, but a simple divisor enumeration with early exit is simpler to implement and sufficiently fast.

## Refining the problem, round 2 thoughts
Refinements and details:
- We should handle n = 1 (only 1 divisor) separately or let the divisor loop handle it — it won't have 4 divisors.
- Use math.isqrt to iterate only up to integer sqrt(n) and avoid floating-point issues.
- When i divides n, add both i and n//i unless they're equal (perfect square), in which case add only once.
- Early exit once the divisor count exceeds 4 to save work.
- After scanning, only add the divisor sum to the global answer if count == 4.

Time complexity: O(N * sqrt(M)) where N = len(nums) and M = max(nums). With N <= 1e4 and sqrt(M) <= 316 this is ~3.16e6 iterations in worst case — plenty fast.
Space complexity: O(1) extra space.

## Attempted solution(s)
```python
import math
from typing import List

class Solution:
    def sumFourDivisors(self, nums: List[int]) -> int:
        total = 0
        for n in nums:
            if n <= 1:
                continue
            div_sum = 0
            count = 0
            root = math.isqrt(n)
            for i in range(1, root + 1):
                if n % i == 0:
                    j = n // i
                    if i == j:
                        count += 1
                        div_sum += i
                    else:
                        count += 2
                        div_sum += i + j
                    if count > 4:
                        break
            if count == 4:
                total += div_sum
        return total
```
- Approach: For each number iterate i from 1..sqrt(n); when i divides n add the pair (i and n//i), handle square root specially to avoid double-counting. Stop early if divisor count exceeds 4. If after the loop the count is exactly 4, add the computed divisor sum to the running total.
- Time complexity: O(N * sqrt(M)) where N = len(nums), M = max(nums) (<= 1e5). In worst case this is about 1e4 * 316 ≈ 3.16e6 divisor checks.
- Space complexity: O(1) extra space.
- Implementation details: math.isqrt is used for accurate integer square root. Early termination (when count > 4) avoids unnecessary work for numbers with many divisors. This method correctly handles both forms (p*q and p^3) because it simply counts divisors.