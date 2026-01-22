# [Problem 1460: Make Two Arrays Equal by Reversing Subarrays](https://leetcode.com/problems/make-two-arrays-equal-by-reversing-subarrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Reversing a subarray is a fairly powerful operation. If I can reverse any contiguous segment, I can certainly reverse a length-2 segment (swap two adjacent elements). Since swapping adjacent elements is enough to generate any permutation (bubble-sort style), it seems plausible that any permutation of arr can be achieved by a sequence of subarray reversals. Therefore the only thing that should matter is whether arr and target have the same multiset of values. If they do, we can reorder arr to match target; if not, it's impossible.

So a quick check is to compare counts of each value (or sort both arrays and compare). That should be sufficient.

## Refining the problem, round 2 thoughts
- Edge cases: lengths are guaranteed equal by the problem statement. Values are small (1..1000) and arrays length up to 1000, so both sorting and counting approaches are efficient.
- Alternative solutions: 
  - Sort both arrays and compare (O(n log n) time).
  - Use a frequency counter (collections.Counter) or a fixed-size frequency array of size 1001 (O(n) time).
- Time/space:
  - Sorting: O(n log n) time, O(1) or O(n) extra depending on sort implementation.
  - Counting: O(n + V) time where V is value range (here <=1000), O(V) space or O(n) for Counter.

I'll implement the simple and idiomatic solution using collections.Counter (clear and concise).

## Attempted solution(s)
```python
from typing import List
from collections import Counter

class Solution:
    def canBeEqual(self, target: List[int], arr: List[int]) -> bool:
        """
        Return True if arr can be transformed to target by reversing subarrays.
        Equivalent condition: arr and target have the same multiset of values.
        """
        return Counter(target) == Counter(arr)
```
- Notes:
  - Approach: Because reversing subarrays allows adjacent swaps (reverse of length 2), any permutation of arr can be achieved. Therefore arr can be made equal to target iff they contain the same elements with the same frequencies.
  - Time complexity: O(n) expected for building the two Counters (n = length of arrays). In worst case with hash overhead still linear on average. Alternatively, sorting would be O(n log n).
  - Space complexity: O(k) where k is number of distinct values (<= n), for the counters. If using a fixed frequency array due to known small value range, space could be O(V) with V = 1001.