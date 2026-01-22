# [Problem 2206: Divide Array Into Equal Pairs](https://leetcode.com/problems/divide-array-into-equal-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness thoughts, but here is a concise summary of the approach instead:

- Count occurrences of each value in nums.
- For nums to be dividable into equal pairs, every value must appear an even number of times (so they can be grouped into pairs).
- So return True iff every count is even.

## Refining the problem, round 2 thoughts
- Edge cases: smallest allowed arrays (length 2) — simply check the two elements are equal. If all values have even counts, the grouping is always possible because identical elements can be paired arbitrarily.
- Complexity: one linear pass to build counts and another to check parity: O(n) time, O(k) extra space where k is number of distinct values (k ≤ n, and constrained by value range).
- Alternatives: sorting and checking adjacent pairs also works (O(n log n) time), but counting is simpler and optimal here.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def divideArray(self, nums: List[int]) -> bool:
        counts = Counter(nums)
        for c in counts.values():
            if c % 2 != 0:
                return False
        return True
```
- Approach: Use a frequency counter and verify every frequency is even.
- Time complexity: O(n), where n = len(nums).
- Space complexity: O(k), k = number of distinct elements (k ≤ n).