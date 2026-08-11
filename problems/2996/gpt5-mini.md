# [Problem 2996: Smallest Missing Integer Greater Than Sequential Prefix Sum](https://leetcode.com/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share my internal chain-of-thought verbatim, but here is a concise, non-sensitive summary of the approach I consider: identify the longest sequential prefix starting at index 0, compute its sum, then find the smallest integer >= that sum that does not appear in the array. The natural implementation is to build a set of elements for O(1) membership checks and increment from the prefix sum until we find a missing value.

## Refining the problem, round 2 thoughts
- Determine the length of the longest sequential prefix: iterate from index 1 while nums[i] == nums[i-1] + 1. The prefix is nums[0..i-1].
- Compute sum of that prefix.
- Build a set of the array values. Starting from the prefix sum, check successive integers until one is not in the set; return that integer.
- Edge cases:
  - Array length 1: prefix is the single element, sum is that element.
  - Entire array can be sequential; then we sum the entire array and search from that sum upward.
- Complexity:
  - Time: O(n + t) where n = len(nums) and t is the number of increments until we find a missing integer. Given problem constraints (nums[i] in [1,50], n <= 50), t is small in practice. In general t ≤ number of distinct integers present above the sum.
  - Space: O(n) for the set.

## Attempted solution(s)
```python
class Solution:
    def smallestMissingValue(self, nums: list[int]) -> int:
        # find length of longest sequential prefix starting at index 0
        n = len(nums)
        i = 1
        while i < n and nums[i] == nums[i - 1] + 1:
            i += 1
        prefix_sum = sum(nums[:i])
        seen = set(nums)
        x = prefix_sum
        while x in seen:
            x += 1
        return x

# Example usage:
if __name__ == "__main__":
    sol = Solution()
    print(sol.smallestMissingValue([1,2,3,2,5]))         # expected 6
    print(sol.smallestMissingValue([3,4,5,1,12,14,13]))  # expected 15
    print(sol.smallestMissingValue([7]))                 # expected 7 if 7 not in array? 
    # Note: for single element [7], prefix sum = 7 and 7 is in array, so result will be 8.
```

- Notes:
  - We compute the longest sequential prefix length by incrementing an index while the +1 relation holds between consecutive elements.
  - The prefix sum is computed using Python's sum on the slice nums[:i].
  - A set of nums allows O(1) membership checks while we increment from the prefix sum until we find a missing integer.
  - Time complexity: O(n + t) where n = len(nums) and t is the count of integers checked after the prefix sum (bounded in the problem by small constants). Space complexity: O(n) for the set.