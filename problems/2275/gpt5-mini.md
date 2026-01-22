# [Problem 2275: Largest Combination With Bitwise AND Greater Than Zero](https://leetcode.com/problems/largest-combination-with-bitwise-and-greater-than-zero/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the largest subset (combination) of elements whose bitwise AND is > 0. Brute-forcing all subsets is impossible for n up to 1e5. The AND being > 0 means at least one bit position remains 1 after AND-ing every element in the chosen subset. That implies every element in the chosen subset must have that specific bit set. So any viable subset must be entirely drawn from the numbers that have some particular bit = 1. Therefore the maximum possible size is at most the count of numbers that have that bit. Conversely, taking all numbers that have a particular bit set yields an AND that keeps that bit set (so > 0). So the answer is simply the maximum count among bit positions of how many numbers have that bit.

## Refining the problem, round 2 thoughts
- We don't need to consider combinations mixing bits because the AND must preserve at least one common 1-bit across all chosen numbers.
- Given candidates[i] ≤ 1e7, bits up to 24 are sufficient (2^24 = 16777216 > 1e7). To be safe and simple, iterate up to 31 or 32 bits.
- Edge cases: single element arrays (answer 1), identical values (counts add up), presence of zero (if zero allowed it would not contribute to any bit count).
- Time complexity: O(n * B) where B = number of bits checked (≈ 31) → effectively O(n). Space complexity: O(B) extra (constant).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def largestCombination(self, candidates: List[int]) -> int:
        # We'll count how many numbers have each bit set.
        # Use 32 bits to be safe for the given constraints.
        bit_counts = [0] * 32
        for num in candidates:
            # For each bit position, increment if it's set in num.
            # Using a loop over fixed bits is simple and fast here.
            for b in range(32):
                if (num >> b) & 1:
                    bit_counts[b] += 1
        # The largest combination size is the maximum count among bits.
        return max(bit_counts) if bit_counts else 0
```
- Notes:
  - Approach: count occurrences of each bit among all numbers, answer = max count.
  - Time complexity: O(n * B) where n = len(candidates) and B = number of bits checked (we used 32) → effectively O(n).
  - Space complexity: O(B) extra space (constant, here 32 integers).
  - This is efficient for n up to 1e5 and values up to 1e7.