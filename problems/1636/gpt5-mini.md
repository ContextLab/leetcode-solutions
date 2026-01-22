# [Problem 1636: Sort Array by Increasing Frequency](https://leetcode.com/problems/sort-array-by-increasing-frequency/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to sort nums primarily by frequency (ascending). If frequencies are equal, then by value in decreasing order. First thing that comes to mind is counting frequencies (Counter/dictionary) and then sorting. There are two straightforward ways:
- Sort the original list with a custom key that uses the frequency map.
- Or sort the distinct values by the desired ordering and then expand each value by its count.

Sorting the original list directly with key=(frequency, -value) should produce the desired order since Python's sort is stable and will compare these tuples lexicographically. Need to be careful with negative numbers, but using -value handles decreasing order regardless of sign.

## Refining the problem, round 2 thoughts
Edge cases:
- Single-element array or all elements equal -> trivial.
- Negative values -> using -value in the key still correctly orders by decreasing numeric value.
- Small input size (n <= 100) so O(n log n) sorting is fine. Memory usage is minimal.

Alternatives: building buckets by frequency is possible but overkill here. I'll go with counting and a single sort of the list using the frequency map.

Time complexity: O(n log n) for the sort (n = len(nums)). Building the frequency map is O(n). Space complexity: O(n) for the frequency map and result.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        freq = Counter(nums)
        # Sort each element by (frequency ascending, value descending)
        return sorted(nums, key=lambda x: (freq[x], -x))

# Example usage:
if __name__ == "__main__":
    s = Solution()
    print(s.frequencySort([1,1,2,2,2,3]))        # [3,1,1,2,2,2]
    print(s.frequencySort([2,3,1,3,2]))          # [1,3,3,2,2]
    print(s.frequencySort([-1,1,-6,4,5,-6,1,4,1]))  # [5,-1,4,4,-6,-6,1,1,1]
```
- Approach: count frequencies with Counter, then sort the original array with a custom key: (frequency, -value). This ensures increasing frequency and, for ties, decreasing values.
- Time complexity: O(n log n) due to sorting (n = len(nums)). Building the Counter is O(n).
- Space complexity: O(n) for the frequency map and the output (sorted list).
- Implementation details: Using -x in the key works correctly for negative and positive integers to produce decreasing numeric order when frequencies tie.