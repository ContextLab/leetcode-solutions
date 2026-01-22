# [Problem 2294: Partition Array Such That Maximum Difference Is K](https://leetcode.com/problems/partition-array-such-that-maximum-difference-is-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimum number of subsequences such that in each subsequence the max minus min ≤ k. A subsequence preserves original relative order, but grouping elements is only constrained by including each element exactly once in some subsequence.

My first thought: if we only care about values (max and min), elements that fall within any interval of length k can be put into the same group. Sorting the values makes it easy to see contiguous blocks of numbers that fit within a window of size k. Greedily take as many elements as possible whose values are within k of the first element in the current group; once we hit a value that is more than k away, we must start a new group. That suggests sorting and a single pass.

I briefly worried whether sorting (which changes order) could violate the subsequence order constraint. But the subsequence constraint only requires that within a chosen group we keep the original order of those elements; it doesn't prevent us from deciding groups based on value ranges. For any value-based partition (e.g., take all elements with values in [a,a+k] into a group), the relative order of those elements in the original array is preserved when we form that subsequence. So sorting is only used to determine groups; we can then pick the original-order subsequences corresponding to those groups.

## Refining the problem, round 2 thoughts
Refinement:
- Sort nums ascending.
- Maintain the start value of the current subsequence (the minimum in that group after sorting). Iterate through sorted nums; if current value - start > k, start a new subsequence with start = current value and increment count.
- Return the count of subsequences.

Edge cases:
- k = 0: groups must contain equal values only, so each distinct block of equal values can be grouped but values that differ require new groups.
- All values within k of each other -> answer 1.
- Single element -> answer 1.

Complexity:
- Sorting dominates: O(n log n) time, O(1) extra space (or O(n) if the language's sort is not in-place). Alternate approach: counting sort / bucket counting is possible since nums[i] ≤ 1e5; that would give O(n + M) time where M = maxValue, but sorting is simpler and fine for constraints up to 1e5.

This greedy is optimal because we always extend the current subsequence as much as possible; delaying starting a new subsequence cannot reduce the total number of subsequences.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def partitionArray(self, nums: List[int], k: int) -> int:
        if not nums:
            return 0
        nums.sort()
        count = 1  # at least one subsequence
        start = nums[0]
        for x in nums:
            if x - start > k:
                count += 1
                start = x
        return count
```
- Notes:
  - Approach: sort the array, then greedily form subsequences by taking the longest possible block starting from the current minimum such that max - min ≤ k. When an element exceeds that window, start a new subsequence.
  - Time complexity: O(n log n) due to sorting (n = len(nums)).
  - Space complexity: O(1) extra (not counting sort space or in-place sort overhead). An alternative is counting sort (O(n + M)) since nums[i] ≤ 10^5, but the sort-based solution is concise and efficient enough for constraints.