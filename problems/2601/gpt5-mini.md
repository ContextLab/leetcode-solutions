# [Problem 2601: Prime Subtraction Operation](https://leetcode.com/problems/prime-subtraction-operation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can subtract a prime p < nums[i] from each index at most once. The operation only decreases values, so if an element is already <= the previous element in the final strictly increasing array, we cannot fix that by later operations (we can't increase any element). So decisions should be made left-to-right: each element must end up strictly greater than the previous element we fixed.

For each element nums[i] (processing in index order), we can either leave it or subtract one prime (once). To help future elements, it's beneficial to make the current element as small as possible while still being strictly greater than the previous fixed value. So for a given nums[i] and a running prev (value of last fixed element), we want to see if we can subtract a prime p such that new = nums[i] - p > prev. Among all valid p, we should pick the largest p (to minimize new). If no such prime exists and nums[i] <= prev, it's impossible. If no prime can be subtracted (or it's not needed) but nums[i] > prev, we keep nums[i].

We need primes up to at most 1000 (constraint), so precompute primes with a sieve.

## Refining the problem, round 2 thoughts
- Precompute primes up to max(nums) (<= 1000) using sieve of Eratosthenes and store them sorted.
- Let prev = 0 (since nums[i] >= 1, starting prev = 0 is safe).
- For each i:
  - If nums[i] <= prev -> immediate false (can't increase).
  - Else compute limit = nums[i] - prev - 1. We need a prime p <= limit (and also p < nums[i], but limit < nums[i] ensures that).
  - If limit >= 2, pick the largest prime <= limit (binary search on prime list). If found, subtract it.
  - After possible subtraction, check nums[i] > prev (should hold if p chosen ≤ limit). Set prev = nums[i].
- Complexity: sieve O(M log log M) where M = max(nums) ≤ 1000. Iteration O(n log P) with binary search on primes. Both n, M ≤ 1000 — very efficient.

Edge cases:
- nums[i] = 1 or 2: there may be no prime p < nums[i] so no subtraction possible.
- Must ensure p < nums[i]; when we choose p <= limit, limit is nums[i] - prev - 1 so limit < nums[i], so p < nums[i] satisfied.
- Use prev initialized to 0 so first element can be reduced if beneficial.

## Attempted solution(s)
```python
from bisect import bisect_right
from typing import List

class Solution:
    def primeSubOperation(self, nums: List[int]) -> bool:
        if not nums:
            return True

        # Sieve primes up to max(nums) (max constraint is 1000)
        max_val = max(nums)
        limit_sieve = max(2, max_val)  # at least 2 for sieve
        is_prime = [True] * (limit_sieve + 1)
        is_prime[0] = is_prime[1] = False
        p = 2
        while p * p <= limit_sieve:
            if is_prime[p]:
                for multiple in range(p * p, limit_sieve + 1, p):
                    is_prime[multiple] = False
            p += 1
        primes = [i for i, val in enumerate(is_prime) if val]

        prev = 0  # previous fixed value; nums elements are >= 1
        for i in range(len(nums)):
            x = nums[i]
            # If already <= prev, we cannot increase it -> impossible
            if x <= prev:
                return False

            # We want to reduce x as much as possible while keeping new > prev.
            # So need prime p such that p < x and x - p > prev -> p < x - prev
            max_allowed_p = x - prev - 1
            if max_allowed_p >= 2:
                # find largest prime <= max_allowed_p
                idx = bisect_right(primes, max_allowed_p) - 1
                if idx >= 0:
                    p = primes[idx]
                    # p < x is guaranteed because max_allowed_p < x
                    x -= p

            # After possible reduction, must still be > prev
            if x <= prev:
                return False
            prev = x

        return True
```
- Approach: Greedy left-to-right. For each element, if possible, subtract the largest prime p that keeps the element strictly greater than the previous element. This minimizes the current element and makes it easiest for the remaining elements to satisfy strict increase.
- Time complexity: O(M log log M + n log P), where M = max(nums) ≤ 1000 (sieve cost) and P is number of primes ≤ M (binary search per element). Practically O(n + M).
- Space complexity: O(M) for the sieve/primes list.