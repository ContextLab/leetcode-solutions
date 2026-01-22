# [Problem 2444: Count Subarrays With Fixed Bounds](https://leetcode.com/problems/count-subarrays-with-fixed-bounds/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count contiguous subarrays whose minimum equals minK and maximum equals maxK. Brute force (examining all subarrays and checking min/max) is O(n^2) and too slow for n up to 1e5. Observing constraints, elements outside [minK, maxK] break any valid subarray — such elements partition the array into independent segments. Within a valid segment (all elements in [minK, maxK]), we must count subarrays that contain at least one minK and at least one maxK. This suggests a linear scan maintaining last positions of minK, maxK, and the most recent invalid element, and counting how many valid subarrays end at each index.

## Refining the problem, round 2 thoughts
- Maintain three pointers/indices while scanning:
  - lastBad: index of the most recent element < minK or > maxK (i.e., element that invalidates any subarray including it).
  - lastMin: most recent index where nums[i] == minK.
  - lastMax: most recent index where nums[i] == maxK.
- For each position i, any subarray ending at i is valid iff it starts strictly after lastBad and the subarray includes at least one minK and one maxK. The earliest start that satisfies both is at index min(lastMin, lastMax). So number of valid subarrays ending at i is max(0, min(lastMin, lastMax) - lastBad).
- Edge case minK == maxK: updates to lastMin and lastMax will be the same index when nums[i] == that value; formula still works (counts subarrays that include at least one occurrence of that value).
- Time O(n), space O(1). Use a 64-bit capable accumulator (Python int is fine).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        lastBad = -1       # most recent index of an invalid element (<minK or >maxK)
        lastMin = -1       # most recent index where nums[i] == minK
        lastMax = -1       # most recent index where nums[i] == maxK
        res = 0

        for i, val in enumerate(nums):
            # If this value is invalid, mark lastBad
            if val < minK or val > maxK:
                lastBad = i
            # Update last positions of minK and maxK
            if val == minK:
                lastMin = i
            if val == maxK:
                lastMax = i
            # Count valid subarrays ending at i:
            # they must start after lastBad and include at least one minK and maxK,
            # so earliest valid start is 0..min(lastMin,lastMax) but must be > lastBad
            valid_starts = min(lastMin, lastMax) - lastBad
            if valid_starts > 0:
                res += valid_starts

        return res
```
- Approach: Single pass tracking last invalid index, last index of minK, and last index of maxK. For each ending index i, add max(0, min(lastMin, lastMax) - lastBad) to the result.
- Time complexity: O(n), where n = len(nums) — each element processed once.
- Space complexity: O(1) extra space.
- Notes: This handles the case minK == maxK naturally. The algorithm exploits partitioning by invalid elements and counts subarrays by number of valid start positions for each end index.