# [Problem 2574: Left and Right Sum Differences](https://leetcode.com/problems/left-and-right-sum-differences/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to compute for each index i the sum of elements to the left and the sum of elements to the right, then take the absolute difference. The straightforward way is to build prefix sums (leftSum array) and suffix sums (rightSum array) and then compute answer[i] = |leftSum[i] - rightSum[i]|. But I can avoid storing both full arrays: if I know the total sum of the array and keep a running left cumulative sum, rightSum at index i is total - left - nums[i]. That gives a single-pass after computing total (or even in one pass if I compute total first). Edge cases: single element (n=1) should return [0]. Complexity target: O(n) time, O(n) output space, O(1) extra space.

## Refining the problem, round 2 thoughts
I'll implement the approach: compute total = sum(nums). Initialize left = 0. For each i from 0..n-1, right = total - left - nums[i]. answer[i] = abs(left - right). Then update left += nums[i]. This is clean and avoids separate suffix array. Consider constraints: n up to 1000, nums[i] up to 1e5 — sums fit in Python int easily. Time complexity O(n), space complexity O(n) for the output array (plus O(1) extra). Alternative is building prefix and suffix arrays explicitly which is also O(n) and fine here, but the single-pass with total is slightly more space-efficient and simpler.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def leftRigthDifference(self, nums: List[int]) -> List[int]:
        total = sum(nums)
        left = 0
        n = len(nums)
        ans = [0] * n
        for i, val in enumerate(nums):
            right = total - left - val
            ans[i] = abs(left - right)
            left += val
        return ans
```
- Notes:
  - Approach: compute total sum, maintain left cumulative sum while iterating. Right sum at index i is total - left - nums[i]. Compute absolute difference and update left.
  - Time complexity: O(n) — one pass to sum plus one pass to build answer (summing and answer-building could be combined but still O(n) overall).
  - Space complexity: O(n) for the returned answer array; O(1) additional auxiliary space.
  - Handles edge cases like n = 1 correctly (returns [0]).