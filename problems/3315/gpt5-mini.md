# [Problem 3315: Construct the Minimum Bitwise Array II](https://leetcode.com/problems/construct-the-minimum-bitwise-array-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want to find, for each prime p, the smallest nonnegative x such that x OR (x+1) = p, otherwise return -1. Try to inspect small x values and their OR with x+1 to see a pattern:

- 0 | 1 = 1
- 1 | 2 = 3
- 2 | 3 = 3
- 3 | 4 = 7
- 4 | 5 = 5
- 5 | 6 = 7
- 6 | 7 = 7
- 7 | 8 = 15
...

I notice a pattern: if x has r trailing 1 bits (bits 0..r-1 are 1) and bit r is 0, then x+1 sets bit r to 1 and clears the trailing r ones, so the OR becomes x with bit r set to 1. If r is the number of trailing ones in x, the OR equals x + 2^r. Let k = r+1, then p = x | (x+1) = x + 2^r = x + 2^{k-1}. Rearranging yields x = p - 2^{k-1}. Also from the bit-structure constraints you find p+1 must be divisible by 2^k for some k >= 1. So p+1 must be even; if p+1 is odd (i.e., p = 2), there's no solution.

So it looks like if we let t = v2(p+1) (the exponent of 2 dividing p+1), any k in [1..t] yields a candidate x = p - 2^{k-1}. To minimize x, pick largest k, i.e. k = t. So x = p - 2^{t-1}. If t = 0 (p+1 odd), no solution -> -1.

This gives a simple, efficient computation.

## Refining the problem, round 2 thoughts
Edge cases:
- p = 2: p+1 = 3 has v2 = 0 -> no solution -> -1 (matches expected).
- For any other prime p (odd), p+1 is even, so t >= 1 and there is a solution.
- Compute t efficiently by extracting the lowest set bit of (p+1): lowbit = (p+1) & -(p+1) = 2^t. If lowbit == 1 => t=0 => -1; otherwise ans = p - (lowbit >> 1).

Time complexity: O(n) with O(1) work per element (bit ops). Space complexity: O(n) result.

I'll implement a clear Python function and also provide a class wrapper (LeetCode style) and a small test block.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def constructMinimumBitwiseArray(self, nums: List[int]) -> List[int]:
        """
        For each prime p in nums, return the minimal x such that x | (x+1) == p,
        or -1 if no such x exists.
        Observed formula:
            Let v = p + 1, lowbit = v & -v = 2^t.
            If lowbit == 1 (t == 0) -> no solution (return -1).
            Else minimal x = p - 2^(t-1) = p - (lowbit >> 1).
        """
        res = []
        for p in nums:
            v = p + 1
            lowbit = v & -v  # lowest set bit value = 2^t
            if lowbit == 1:
                res.append(-1)
            else:
                res.append(p - (lowbit >> 1))
        return res

# Standalone helper if preferred:
def construct_minimum_bitwise_array(nums: List[int]) -> List[int]:
    sol = Solution()
    return sol.constructMinimumBitwiseArray(nums)

# Example usage / quick test:
if __name__ == "__main__":
    examples = [
        ([2,3,5,7], [-1,1,4,3]),
        ([11,13,31], [9,12,15]),
        ([2], [-1]),
        ([3], [1]),
    ]
    for inp, expected in examples:
        out = construct_minimum_bitwise_array(inp)
        print(f"nums = {inp} -> {out} (expected {expected})")
```

- Approach notes:
  - Key observation: If x has r trailing ones then x | (x+1) = x + 2^r. Let k = r+1, so p+1 must be divisible by 2^k. Maximizing k (i.e., using the full 2-adic valuation t = v2(p+1)) minimizes x, giving x = p - 2^{t-1}.
  - We compute the lowest set bit of p+1 with v & -v to get 2^t; if that equals 1 then t=0 and no valid x exists.
- Complexity:
  - Time: O(n) where n = len(nums). Each number is handled in O(1) using constant-time bit operations.
  - Space: O(n) for the output array.