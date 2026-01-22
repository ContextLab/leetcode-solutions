# [Problem 2563: Count the Number of Fair Pairs](https://leetcode.com/problems/count-the-number-of-fair-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count pairs (i, j) with i < j such that nums[i] + nums[j] lies in [lower, upper]. Brute force O(n^2) will be too slow for n up to 1e5. Sorting usually helps for pair-sum range queries. If nums is sorted we can for each element find how many later elements give sums within the bounds. That suggests either binary search for each i (find leftmost and rightmost j) or a two-pointer/window approach. Both yield O(n log n) (binary search per i) or O(n log n) for sort plus O(n) for two-pointer counting. I'll try sorting + binary searches since it's simple and safe; two-pointer counting is slightly more subtle but similar idea.

## Refining the problem, round 2 thoughts
- Sort nums. For each i from 0 to n-1, we need indices j > i with lower - nums[i] <= nums[j] <= upper - nums[i].
- Use bisect_left to find first j >= i+1 with value >= lower - nums[i], and bisect_right to find first index > upper - nums[i]. Add the difference.
- Edge cases: negative values, duplicates — sorting and bisect handle them. Make sure to search starting at i+1 to ensure i < j.
- Complexity: sort O(n log n) + n * O(log n) for bisects -> O(n log n) time, O(1) extra space (or O(n) if counting sort doesn't apply). Using Python bisect from sorted list is straightforward.
- Alternatively, we could count pairs with sum <= upper and subtract pairs with sum < lower (i.e., <= lower-1), using two-pointer counting for O(n) after sorting; both are valid. I'll implement the direct per-i binary search approach.

## Attempted solution(s)
```python
from bisect import bisect_left, bisect_right
from typing import List

class Solution:
    def countFairPairs(self, nums: List[int], lower: int, upper: int) -> int:
        nums.sort()
        n = len(nums)
        ans = 0
        for i in range(n):
            lo = lower - nums[i]
            hi = upper - nums[i]
            # search only in indices > i
            left = bisect_left(nums, lo, i + 1, n)
            right = bisect_right(nums, hi, i + 1, n)
            if right > left:
                ans += (right - left)
        return ans
```
- Notes:
  - Approach: sort the array, then for each i use binary search to count valid j > i such that nums[i] + nums[j] is in [lower, upper].
  - Time complexity: O(n log n) dominated by sorting and n binary searches (each O(log n)).
  - Space complexity: O(1) extra (ignoring input/output), or O(n) if counting the sorted array separately (here we sort in-place).
  - Implementation details: use bisect_left(nums, lo, i+1) and bisect_right(nums, hi, i+1) to ensure j > i. This handles duplicates and negative values correctly.