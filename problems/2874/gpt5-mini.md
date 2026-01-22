# [Problem 2874: Maximum Value of an Ordered Triplet II](https://leetcode.com/problems/maximum-value-of-an-ordered-triplet-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to maximize (nums[i] - nums[j]) * nums[k] with i < j < k and nums elements are positive. For fixed j, the term (nums[i] - nums[j]) is maximized by choosing the largest nums[i] with i < j. For fixed j and that best i, the product with nums[k] is maximized by choosing the largest nums[k] with k > j (since nums[k] are positive). So it looks like we can precompute prefix maximums (best i for each j) and suffix maximums (best k for each j) and iterate over j to compute candidates. If all candidates are negative we return 0.

## Refining the problem, round 2 thoughts
- Need to be careful that prefix max for j should consider indices strictly before j (i < j), so use prefix_max[j-1].
- Suffix max for j should consider indices strictly after j (k > j), so use suffix_max[j+1].
- Iterate j from 1 to n-2 inclusive.
- Time complexity should be O(n) with O(n) extra space for prefix and suffix arrays; we could reduce space to O(1) by scanning right-to-left while maintaining suffix max, but O(n) space is fine and simpler.
- Edge cases: small n (but n >= 3 per constraints), large values (products up to ~1e12, Python int handles it).
- If every candidate product is negative, return 0.

## Attempted solution(s)
```python
class Solution:
    def maximumTripletValue(self, nums: list[int]) -> int:
        n = len(nums)
        if n < 3:
            return 0

        # prefix_max[i] = max(nums[0..i])
        prefix_max = [0] * n
        prefix_max[0] = nums[0]
        for i in range(1, n):
            prefix_max[i] = max(prefix_max[i - 1], nums[i])

        # suffix_max[i] = max(nums[i..n-1])
        suffix_max = [0] * n
        suffix_max[-1] = nums[-1]
        for i in range(n - 2, -1, -1):
            suffix_max[i] = max(suffix_max[i + 1], nums[i])

        best = -10**30  # sufficiently small sentinel
        # j runs from 1 to n-2 (so i < j and k > j exist)
        for j in range(1, n - 1):
            left_best = prefix_max[j - 1]   # best nums[i] with i < j
            right_best = suffix_max[j + 1]  # best nums[k] with k > j
            diff = left_best - nums[j]
            val = diff * right_best
            if val > best:
                best = val

        return max(0, best)
```
- Approach: Precompute prefix maximums for the best choice of i for each j and suffix maximums for the best choice of k for each j, then evaluate every possible middle index j in O(1) time each.
- Time complexity: O(n) to build prefix and suffix arrays and O(n) to evaluate all j, so overall O(n).
- Space complexity: O(n) extra for prefix and suffix arrays. This can be optimized to O(1) by scanning from right to left and keeping current suffix max while iterating j, but O(n) is clear and simple.