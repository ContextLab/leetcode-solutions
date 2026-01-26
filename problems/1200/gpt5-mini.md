# [Problem 1200: Minimum Absolute Difference](https://leetcode.com/problems/minimum-absolute-difference/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need all pairs [a, b] (a < b) whose difference equals the minimum absolute difference among any two elements in arr. My first thought is sorting: if arr is sorted, the minimum difference must occur between some pair of adjacent elements — because for any non-adjacent pair there is at least one element between them that creates a smaller or equal gap by the triangle inequality. So sort arr, scan adjacent differences to find the global minimum, then collect all adjacent pairs with that difference. Sorting is O(n log n) which is fine for n up to 1e5. Since values are bounded (-1e6..1e6) an alternative counting-sort / bucket approach could yield O(n + range) but not necessary here.

## Refining the problem, round 2 thoughts
We should consider edge cases: n is at least 2 per constraints, and elements are distinct so we won't see zero differences except if duplicates were allowed (they're not). After sorting, we do a single pass to compute minDiff, then another pass to collect pairs (or do both in one pass by updating when we find a smaller diff and resetting results). Keep memory usage minimal: output size may be up to n-1 pairs in worst case. Time complexity dominated by sort: O(n log n). Space complexity aside from output is O(1) (or O(n) if counting sort or if we consider the sort in-place requiring O(log n) stack for Timsort).

I'll implement a single-pass after sort that both updates minDiff and maintains result: when we find a smaller diff, reset result to just this pair; when equal, append.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        # Sort the array first
        arr.sort()
        n = len(arr)
        # Initialize minDiff to a large value
        minDiff = float('inf')
        res: List[List[int]] = []
        # Single pass to find minDiff and build result
        for i in range(1, n):
            diff = arr[i] - arr[i-1]
            if diff < minDiff:
                minDiff = diff
                res = [[arr[i-1], arr[i]]]
            elif diff == minDiff:
                res.append([arr[i-1], arr[i]])
        return res
```
- Notes:
  - Approach: sort the array and examine only adjacent pairs. When a smaller difference is found, reset the result list; when equal, append the pair.
  - Time complexity: O(n log n) due to sorting (n = len(arr)). The single scan is O(n).
  - Space complexity: O(1) extra space ignoring the output (or O(n) if counting the output). Sorting in Python (Timsort) uses O(n) worst-case auxiliary but typically O(log n) stack; overall this is acceptable for n up to 1e5.
  - This solution is simple, efficient, and handles the constraints directly.