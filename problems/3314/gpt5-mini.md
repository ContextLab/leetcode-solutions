# [Problem 3314: Construct the Minimum Bitwise Array I](https://leetcode.com/problems/construct-the-minimum-bitwise-array-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need, for each given prime nums[i], to find the smallest nonnegative integer a such that a OR (a+1) == nums[i], otherwise output -1. A few quick observations:
- nums[i] are small (<= 1000) and there are at most 100 numbers, so a direct search per number is feasible.
- The operation a | (a+1) depends only on a's low bits (how many trailing 1s it has), but deriving a closed-form for every possible output value is a bit fiddly. Given the constraints, brute force search for the minimal a is simple and efficient.
- Note: nums[i] = 2 (the only even prime) is impossible because for any a, a|(a+1) is >= 3? (in practice we will just test and get no hits -> -1).

## Refining the problem, round 2 thoughts
Refine to a straightforward algorithm:
- For each target p in nums, iterate a from 0 up to p (or p+1) and test a | (a+1) == p.
- Once we find the first such a, that's the minimal by construction; otherwise assign -1.
Edge cases:
- p = 2 should return -1 (no a satisfies condition).
- p up to 1000 means checking up to ~1001 candidates per p is cheap.
Time complexity: O(n * M) where M = max(nums) <= 1000, n <= 100 → at most ~100k iterations of a tiny constant-time bit op. Space: O(n) for result.

This direct search is simple, robust, and efficient enough for constraints.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumBitwise(self, nums: List[int]) -> List[int]:
        res = []
        for p in nums:
            found = -1
            # search minimal a such that a | (a+1) == p
            # a cannot be much bigger than p, so iterate 0..p (inclusive)
            for a in range(0, p + 1):
                if (a | (a + 1)) == p:
                    found = a
                    break
            res.append(found)
        return res

# Example usage:
# s = Solution()
# print(s.minimumBitwise([2,3,5,7]))  # [-1,1,4,3]
# print(s.minimumBitwise([11,13,31])) # [9,12,15]
```

- Notes about the approach:
  - We simply brute-force each possible a from 0 to p and check the bitwise condition; the first match is the minimal a.
  - Time complexity: O(n * M) where n = len(nums) and M = max(nums) (M <= 1000). This is well within limits.
  - Space complexity: O(n) for the output list.
  - Implementation detail: iterating up to p is safe because a | (a+1) grows with a and will not produce values much larger than a+1; checking up to p is enough to find a solution if one exists for target p.