# [Problem 1356: Sort Integers by The Number of 1 Bits](https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to sort integers by the number of 1 bits in their binary representation, with ties broken by numeric value. First thought: compute the popcount (number of 1s) for each integer and use that as the primary key in sorting and the integer itself as the secondary key. Python's built-in sorted supports a key function that can return a tuple (popcount, value). For popcount we can use bin(x).count('1') or int.bit_count() (if available). Since arr length ≤ 500 and values ≤ 10^4, computing popcounts on the fly is cheap. Another idea is bucket-sort by popcount because maximum popcount is small (~14), but built-in sort is simple and efficient here.

## Refining the problem, round 2 thoughts
Edge cases: duplicates — stable sorting or explicit tie-break ensures order by value. Zero should have popcount 0. We should ensure complexity is acceptable: sorted is O(n log n) comparisons, and each key computation is O(1) (bin length ~14 bits), so overall fine. Alternative: precompute popcounts in a dict to avoid repeated computation for identical values, but not necessary given small constraints. Could also use bucket sort since popcounts range is limited (0..14), yielding O(n) time, but built-in sorted is simpler and readable.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def sortByBits(self, arr: List[int]) -> List[int]:
        # Use Python's sorted with a key: (popcount, value)
        # bin(x).count('1') computes the number of 1 bits.
        return sorted(arr, key=lambda x: (bin(x).count('1'), x))
```
- Notes:
  - Approach: Compute popcount for each integer and sort by the tuple (popcount, integer). Python's sorted is stable and supports tuple keys, so ties are resolved by the integer naturally.
  - Time complexity: O(n log n) comparisons where n = len(arr). Each key computation (bin(x).count('1')) is O(k) where k is number of bits (k ≤ 14 for arr[i] ≤ 10^4), so effectively O(n log n).
  - Space complexity: O(n) extra for the output (sorted returns a new list) and small overhead for key computation tuples.
  - Implementation details: Could use x.bit_count() instead of bin(x).count('1') on Python versions that support it (slightly faster). For very large ranges, a bucket sort by popcount (0..max_bits) could be used to get linear time, but unnecessary given constraints.