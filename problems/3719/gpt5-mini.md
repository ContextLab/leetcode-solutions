# [Problem 3719: Longest Balanced Subarray I](https://leetcode.com/problems/longest-balanced-subarray-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the longest subarray where the number of distinct even values equals the number of distinct odd values. Distinctness makes sliding-window tricky because adding/removing elements can change "distinct count" non-monotonically (duplicates). A straightforward thought is brute-force checking every subarray and counting distinct evens/odds. With n up to 1500, O(n^2) or O(n^2 * small factor) is acceptable. I can fix a left index i, expand right j while maintaining two sets (evens and odds) for that window — adding each element once per starting i — giving O(n^2) set operations overall. That should be simple and efficient enough.

I briefly considered more advanced prefix/difference tricks (like mapping prefixes of distinct counts to indices) but handling "distinct in subarray" from global prefix distinct counts is messy because whether a value is counted in a subarray depends on whether its previous occurrence is inside or outside the subarray (last-occurrence bookkeeping), which complicates and is unnecessary given constraints.

## Refining the problem, round 2 thoughts
Refine to this algorithm:
- For each start index i from 0..n-1:
  - Initialize empty sets evens and odds.
  - For j from i..n-1:
    - Add nums[j] to the appropriate set (based on parity).
    - If sizes equal, update max length.
This is O(n^2) time and O(n) auxiliary space in the worst case (sets for a given start). Edge cases: duplicates — sets handle them naturally. If all elements are same parity, no balanced subarray; result remains 0. Complexity is fine for n<=1500.

Alternative: one could try to optimize with last-occurrence tracking and prefix encodings to attempt O(n) or O(n log n), but that's overkill here.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestBalancedSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        best = 0
        for i in range(n):
            evens = set()
            odds = set()
            # Expand j from i to end, update sets, check equality of distinct counts
            for j in range(i, n):
                x = nums[j]
                if x % 2 == 0:
                    evens.add(x)
                else:
                    odds.add(x)
                if len(evens) == len(odds):
                    best = max(best, j - i + 1)
        return best
```
- Notes:
  - Approach: Fix left endpoint and expand right endpoint while maintaining two sets of distinct evens and odds for the current window. Whenever their sizes match, window is balanced; update answer.
  - Time complexity: O(n^2) — for each start i we scan to the end, performing O(1) amortized set insertions; total insertions across all starts is O(n^2).
  - Space complexity: O(n) worst-case for the sets used for a given start (distinct values in a window). Overall auxiliary space is O(n) (not counting input).