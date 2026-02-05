# [Problem 3379: Transformed Array](https://leetcode.com/problems/transformed-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a circular array and for each index i we should move nums[i] steps (right for positive, left for negative) and set result[i] to the value at the landing index. This is independent per index, so we don't mutate nums as we go. The circular movement suggests using modulo arithmetic to wrap indices. If nums[i] is 0, result[i] is 0 (which also matches taking the value at the landing index i). Steps may be larger than array length, so we should reduce steps modulo n.

A straightforward approach: for each i compute target = (i + nums[i]) % n and set result[i] = nums[target]. Python's % handles negative values in the desired wrap-around way.

## Refining the problem, round 2 thoughts
- No need for any fancy data structures, just an output array of same length.
- Handle negative nums and large steps via modulo.
- Edge cases: n == 1 (works fine), nums[i] == 0 (either special-case or handled by same formula).
- Time complexity should be O(n), space O(n) for the output.
- Confirm: we must not change nums during computation (independent actions) — so always read from the original nums.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def transformedArray(self, nums: List[int]) -> List[int]:
        """
        Compute the transformed array as described:
        For each i, move nums[i] steps from i in the circular array and set result[i]
        to the value at the landing index.
        """
        n = len(nums)
        result = [0] * n
        for i, step in enumerate(nums):
            # compute landing index with wrap-around; Python's % handles negatives properly
            target = (i + step) % n
            result[i] = nums[target]
        return result

# Example usage:
if __name__ == "__main__":
    sol = Solution()
    print(sol.transformedArray([3, -2, 1, 1]))  # [1, 1, 1, 3]
    print(sol.transformedArray([-1, 4, -1]))    # [-1, -1, 4]
```
- Notes:
  - The core idea is using modulo arithmetic: target = (i + nums[i]) % n. This naturally handles positive, negative, and large-step values.
  - Time complexity: O(n), since we visit each index exactly once.
  - Space complexity: O(n) for the result array (plus O(1) extra).
  - We do not mutate the input nums while computing results, matching the "independent actions" requirement.