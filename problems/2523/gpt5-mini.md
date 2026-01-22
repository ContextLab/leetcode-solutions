# [Problem 2523: Closest Prime Numbers in Range](https://leetcode.com/problems/closest-prime-numbers-in-range/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the two primes in [left, right] with the smallest difference. The straightforward approach is to generate all primes in the interval and scan adjacent primes to find the smallest gap. For generating primes up to right, a classic Sieve of Eratosthenes is efficient since right ≤ 10^6. Trial division per number would be too slow in the worst case. Edge cases: intervals with fewer than two primes should return [-1, -1]. Also handle left < 2 since primes start at 2.

## Refining the problem, round 2 thoughts
- Use a boolean sieve of length right+1 to mark primes in O(right log log right) time and O(right) space.
- Iterate from max(left, 2) to right, collect primes on the fly and check difference with previous prime to keep the current minimum. Because we scan in ascending order, ties in gap are automatically resolved by taking the earliest pair (smallest num1).
- Complexity: time O(right log log right) for sieve + O(right) for scan; space O(right). For right up to 1e6 this is fine.
- Edge cases: if no primes or only one prime in range → return [-1, -1].

## Attempted solution(s)
```python
import math
from typing import List

class Solution:
    def closestPrimes(self, left: int, right: int) -> List[int]:
        # Ensure we handle left < 2
        if right < 2:
            return [-1, -1]
        left = max(left, 2)
        
        n = right
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        
        limit = math.isqrt(n)
        for i in range(2, limit + 1):
            if is_prime[i]:
                step = i
                start = i * i
                for j in range(start, n + 1, step):
                    is_prime[j] = False
        
        prev = -1
        best = [-1, -1]
        min_gap = float('inf')
        
        for x in range(left, right + 1):
            if is_prime[x]:
                if prev != -1:
                    gap = x - prev
                    if gap < min_gap:
                        min_gap = gap
                        best = [prev, x]
                        # If gap == 1 it's the smallest possible, we could break,
                        # but primes are odd except 2; minimal gap is 1 only for (2,3).
                        if min_gap == 1:
                            break
                prev = x
        
        return best
```
- Notes:
  - We use the Sieve of Eratosthenes to mark primes up to right.
  - Then we scan the range [max(left,2), right] and track the previous prime to compute consecutive gaps; the minimal gap and corresponding pair are updated as we go.
  - Time complexity: O(right log log right) for the sieve (practically O(right)) plus O(right) scan → overall O(right).
  - Space complexity: O(right) for the boolean array.
  - Correctly handles left < 2 and returns [-1, -1] when fewer than two primes are present.