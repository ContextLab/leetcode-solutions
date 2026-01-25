# [Problem 1984: Minimum Difference Between Highest and Lowest of K Scores](https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The goal is to pick k numbers so the range (max - min) among them is minimized. That suggests picking k numbers that are "close" in value. If the array is sorted, any optimal k-subset will appear as a contiguous window in the sorted array (if it didn't, you could replace values to tighten the window). So sort nums and slide a window of size k computing nums[i+k-1] - nums[i] and take the minimum. Edge cases: k = 1 (difference 0), k = len(nums) (difference max-min). Sorting dominates time.

## Refining the problem, round 2 thoughts
- Confirm that optimal solution is contiguous in sorted order: yes, because for any k elements you can reorder them; the max and min are extremes and to minimize that difference you want elements as clustered as possible — sorting and taking contiguous k gives minimal possible span.
- Complexity: sorting O(n log n), then one pass O(n) to check windows. Space: O(1) extra if sorting in place (or O(n) for sorted copy).
- Constraints small (n <= 1000) so this is perfectly efficient.
- Handle trivial case k == 1 early to return 0 (though algorithm already handles it).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minDifference(self, nums: List[int], k: int) -> int:
        # If k == 1, difference is always 0
        if k <= 1:
            return 0
        
        nums.sort()
        n = len(nums)
        # If k equals n, whole range is the answer
        if k == n:
            return nums[-1] - nums[0]
        
        min_diff = float('inf')
        # Slide a window of size k
        for i in range(0, n - k + 1):
            diff = nums[i + k - 1] - nums[i]
            if diff < min_diff:
                min_diff = diff
        
        return min_diff
```
- Notes:
  - Approach: sort nums and examine every contiguous window of length k; the minimum span across these windows is the answer.
  - Time complexity: O(n log n) due to sorting, plus O(n) for scanning windows => O(n log n) overall.
  - Space complexity: O(1) extra (or O(n) if counting the sort implementation's auxiliary space), in-place sort used.
  - Important detail: the property that an optimal k-subset appears as a contiguous block in sorted order is why this greedy sliding-window after sorting is correct.