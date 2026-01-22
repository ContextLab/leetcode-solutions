# [Problem 3347: Maximum Frequency of an Element After Performing Operations II](https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I'm looking at the rules: we can pick up to numOperations distinct indices, and at each picked index add any integer in [-k, k]. That means an element a can be converted to a target value x iff |a - x| <= k (and converting consumes one operation unless the element already equals x). The frequency of x after operations equals:
- the number of elements already equal to x (no operations needed), plus
- up to numOperations elements among those with |a - x| <= k but a != x.

So for a given target x, the maximum achievable frequency is min(original_count(x) + numOperations, number_of_elements_within_[x-k, x+k]). We can pick any integer x, but if x isn't present originally, original_count(x) = 0 and the best we can do is <= numOperations. Thus it's enough to consider targets x that are values present in nums (they give a nonzero base count and can only be better).

I can sort nums and efficiently count how many elements lie in [x-k, x+k] using binary search (bisect) or a sliding window. Complexity should be O(n log n) due to sorting and binary searches.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- k = 0: only elements equal to x count; operations can't change other values to x — correct handled since interval [x, x] only contains exact equals.
- numOperations = 0: answer is simply the maximum original frequency.
- Large values up to 1e9 don't matter because we only use comparisons and sorting.
- Duplicate values: use Counter to get original frequency for each candidate x; use the full sorted array for range counting (bisect_left/right).
- Complexity: sort O(n log n), for each distinct value do 2 bisects O(log n) → O(m log n) where m ≤ n. Overall O(n log n) time, O(n) space.

I'll implement with Python's bisect and Counter. This is simple and robust.

## Attempted solution(s)
```python
from collections import Counter
from bisect import bisect_left, bisect_right
from typing import List

class Solution:
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        """
        For each value v present in nums, count how many elements lie in [v-k, v+k].
        The best achievable frequency for target v is:
            min(freq[v] + numOperations, count_in_range)
        Return the maximum over all present values v.
        """
        n = len(nums)
        if n == 0:
            return 0

        nums_sorted = sorted(nums)
        freq = Counter(nums_sorted)
        ans = 0

        # Iterate over distinct values only (freq keys)
        for v, f in freq.items():
            left = bisect_left(nums_sorted, v - k)
            right = bisect_right(nums_sorted, v + k)
            count_in_range = right - left
            possible = min(f + numOperations, count_in_range)
            if possible > ans:
                ans = possible

            # early exit: if ans reaches n, can't do better
            if ans == n:
                break

        return ans
```
- Notes on approach: We only consider targets equal to existing values because a target not present has base count 0 and thus cannot exceed numOperations, while targets present may combine base count with conversions. For a target v, elements that can be made equal to v are exactly those within [v-k, v+k]; we can convert at most numOperations of them (excluding those already equal).
- Time complexity: O(n log n) due to sorting + O(m log n) bisects (m = number of distinct values, m ≤ n). Space complexity: O(n) for sorting and the Counter.