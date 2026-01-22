# [Problem 2302: Count Subarrays With Score Less Than K](https://leetcode.com/problems/count-subarrays-with-score-less-than-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The score of a subarray = sum(subarray) * length(subarray). nums contains only positive integers. When we extend a subarray by adding an element on the right, both sum and length strictly increase, so the score strictly increases as we extend to the right. That suggests a two-pointer / sliding-window approach where for each right index we maintain the smallest left index such that the window's score < k. For a fixed right, once we find the smallest left that satisfies the condition, all starts between that left and right produce valid subarrays ending at right. So we can iterate right from 0..n-1, expand sum, then advance left while score >= k, and add (right - left + 1) to the answer.

Because nums are positive, the window property (monotonicity of score when expanding) holds and r and l each move at most n steps -> O(n). Need to be careful with large values (k up to 1e15) but Python ints handle that.

## Refining the problem, round 2 thoughts
- Edge cases:
  - If k is very small (e.g., k <= min(nums)), many windows will be invalid and left will quickly move past right; the loop handles that (r-l+1 becomes 0).
  - Single-element subarrays are valid when nums[i] < k/1 -> just nums[i] < k.
- Alternative approaches: one could binary-search the maximal right for each left using prefix sums (O(n log n)), but two-pointer is simpler and O(n).
- Complexity: each index visited once by r and once by l -> O(n) time, O(1) extra space (aside from input).
- Implementation details:
  - Keep running sum variable.
  - While loop condition: sum * window_len >= k -> shrink from left.
  - For each r, after shrinking, add current window length to answer.
  - Use Python integers (no overflow concerns).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        left = 0
        cur_sum = 0
        ans = 0

        for right in range(n):
            cur_sum += nums[right]
            # Shrink from left while score >= k
            while left <= right and cur_sum * (right - left + 1) >= k:
                cur_sum -= nums[left]
                left += 1
            # All subarrays ending at right with start in [left..right] are valid
            ans += (right - left + 1)
        return ans
```
- Notes:
  - Approach: sliding window / two pointers exploiting that nums[i] > 0 so score increases when extending the window to the right. For each right index, after shrinking left to restore score < k (if needed), there are (right - left + 1) valid subarrays ending at right.
  - Time complexity: O(n) — each index is visited by left and right at most once.
  - Space complexity: O(1) extra space (only counters and running sum).