# [Problem 1509: Minimum Difference Between Largest and Smallest Value in Three Moves](https://leetcode.com/problems/minimum-difference-between-largest-and-smallest-value-in-three-moves/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can change at most 3 elements to any values. Intuitively, to minimize the range (max - min) after up to 3 changes, you'd want to "remove" up to three outliers from the ends (either the largest values or the smallest values) by changing them to something inside the remaining range. Sorting the array makes the extremes easy to examine. After sorting, changing 3 elements is equivalent to ignoring any 3 elements from the two ends in all possible distributions (i smallest removed, 3-i largest removed). There are only 4 distributions (i = 0..3) to check. Also, small arrays (length <= 4) can always be made equal in <=3 moves, so result is 0.

## Refining the problem, round 2 thoughts
- Sort the array: O(n log n).
- For n <= 4, return 0 immediately.
- For n > 4, consider i = 0..3, where we change i smallest elements and (3-i) largest elements. The remaining largest after these changes will be at index n-4+i, and the remaining smallest at index i. Compute difference arr[n-4+i] - arr[i] and take min over i.
- Edge cases: negative numbers, duplicates — sorting handles these. Make sure indices are correct (prove: removing i smallest and 3-i largest leaves highest at index n-1-(3-i) = n-4+i).
- Alternative: selection algorithm to get the few required order-statistics without full sort, but sorting is simple and efficient for constraints (n up to 1e5).
- Complexity: time O(n log n) due to sort, space O(1) extra (or O(n) if sort uses extra memory).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minDifference(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 4:
            return 0
        
        nums.sort()
        res = float('inf')
        # Try removing i smallest and (3-i) largest, for i = 0..3
        for i in range(4):
            left = nums[i]
            right = nums[n - 4 + i]
            res = min(res, right - left)
        return res
```
- Notes:
  - Approach: sort and check the 4 possibilities corresponding to distributing up to 3 changes between smallest and largest elements.
  - Time complexity: O(n log n) from sorting.
  - Space complexity: O(1) extra (besides the space used by sort), or O(n) if the sort implementation requires extra memory.
  - Important detail: handle n <= 4 early — you can change up to 3 elements to make all elements equal, so the minimum difference is 0.