# [Problem 1979: Find Greatest Common Divisor of Array](https://leetcode.com/problems/find-greatest-common-divisor-of-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal chain-of-thought or stream-of-consciousness. I can, however, provide a concise summary of the approach and reasoning:

Summary: Find the minimum and maximum values in the array, then compute their greatest common divisor (GCD). The GCD can be computed efficiently with the Euclidean algorithm (Python's math.gcd is fine). A single pass can find min and max in O(n) time and O(1) extra space; the gcd computation is O(log(min, max)).

## Refining the problem, round 2 thoughts
- Edge cases:
  - If all elements are equal, min == max and gcd(min, max) == that value.
  - Array length is at least 2 per constraints.
  - Values are small (≤ 1000), so arithmetic is cheap.
- Implementation choices:
  - Use built-in math.gcd for clarity and reliability.
  - Determine min and max in one pass to be explicit about O(n) time.
- Complexity:
  - Time: O(n) to find min and max + O(log(min, max)) for gcd, overall O(n).
  - Space: O(1) extra space.

## Attempted solution(s)
```python
from typing import List
import math

class Solution:
    def findGCD(self, nums: List[int]) -> int:
        # Find min and max in one pass
        mn = float('inf')
        mx = float('-inf')
        for x in nums:
            if x < mn:
                mn = x
            if x > mx:
                mx = x
        # Compute gcd of min and max
        return math.gcd(mn, mx)
```
- Notes:
  - The solution does a single pass through nums to get the smallest and largest values, then uses math.gcd to compute the greatest common divisor.
  - Time complexity: O(n) where n = len(nums) for the scan; gcd runs in O(log(min, max)) which is negligible relative to n.
  - Space complexity: O(1) extra space.