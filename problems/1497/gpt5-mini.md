# [Problem 1497: Check If Array Pairs Are Divisible by k](https://leetcode.com/problems/check-if-array-pairs-are-divisible-by-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to pair up numbers so each pair sums to a multiple of k. The sum a + b is divisible by k iff (a % k) + (b % k) ≡ 0 (mod k). So numbers group by remainder modulo k, and each remainder r must pair with remainder (k - r) (with special cases for r = 0 and when k is even, r = k/2). This suggests counting remainders and checking counts match complementary remainders. Negative numbers are fine as Python's x % k yields non-negative remainder when k > 0.

## Refining the problem, round 2 thoughts
- Build frequency map of remainders r = num % k.
- For r = 0, the count must be even because 0 pairs with 0.
- If k is even, remainder k/2 pairs with itself, so its count must also be even.
- For other r, freq[r] must equal freq[k-r].
- Time O(n + k), space O(k) (or O(min(n,k)) if using sparse map).
- Edge cases: k = 1 (all remainders 0), negative numbers (handled by %), large k relative to n (sparse counts).

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def canArrange(self, arr: List[int], k: int) -> bool:
        # Count remainders
        freq = Counter((num % k) for num in arr)
        
        # Remainder 0 must have even count
        if freq[0] % 2 != 0:
            return False
        
        # If k is even, remainder k/2 must have even count
        if k % 2 == 0 and freq[k // 2] % 2 != 0:
            return False
        
        # Check complementary remainders for r in 1 .. (k-1)
        # Only need to iterate r from 1 to floor((k-1)/2) (i.e., 1..(k//2))
        # For odd k, range(1, (k+1)//2) covers 1..k//2
        for r in range(1, (k + 1) // 2):
            if freq[r] != freq[k - r]:
                return False
        
        return True
```
- Approach: Count remainders and verify pairing constraints: remainder 0 and (when k even) remainder k/2 need even counts; other remainders must match counts with their complements.
- Time complexity: O(n + k) due to counting and at most iterating up to ~k/2 remainders. Practically O(n) when k is O(n) or smaller.
- Space complexity: O(min(n, k)) for the remainder frequency map.