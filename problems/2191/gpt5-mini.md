# [Problem 2191: Sort the Jumbled Numbers](https://leetcode.com/problems/sort-the-jumbled-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to sort nums by their "mapped value" where each digit i is replaced by mapping[i]. The mapped value is an integer obtained by mapping each digit and then interpreting the result as a normal integer (so leading mapped zeros are discarded). The important points: compute mapped value for each number, sort based on that, and preserve original relative order for ties. Python's sort is stable, so a key-based sort should preserve relative order for equal keys. Two straightforward ways to compute mapped values: convert number to string and build a mapped string then int(...) it, or do digit arithmetic to form the mapped integer. Both are easy; arithmetic avoids string allocations but string approach is clearer. Complexity target is O(n * digits) where digits ≤ 10 (since nums[i] < 1e9).

## Refining the problem, round 2 thoughts
Edge cases:
- nums[i] can be 0 — must handle specially; mapping[0] may be 0..9 and mapped value should be mapping[0].
- Leading zeros in the mapped representation should be discarded — forming an integer (via arithmetic or int(mapped_str)) naturally handles that.
- Stability: equal mapped values must keep original order. Using sort with a key is stable in Python (Timsort), so equal keys preserve relative order.

Choice: implement an efficient mapped_value function using arithmetic (no strings) and then return sorted(nums, key=mapped_value). That computes the key once per element. Time complexity O(n * d) where d is number of digits per number (≤ 10). Space complexity O(n) for the sorted output.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def sortJumbled(self, mapping: List[int], nums: List[int]) -> List[int]:
        # helper to compute mapped integer value for a given number
        def mapped_value(x: int) -> int:
            if x == 0:
                return mapping[0]
            val = 0
            place = 1
            while x > 0:
                d = x % 10
                md = mapping[d]
                val += md * place
                place *= 10
                x //= 10
            return val

        # Python's sort is stable, so using key=mapped_value preserves relative order on ties
        return sorted(nums, key=mapped_value)
```
- Notes:
  - Approach: For each num compute its numeric mapped value by replacing each digit with mapping[d] and constructing the resulting integer (handling 0 as a special case). Then sort nums using that mapped integer as the key. Python's sort is stable so equal mapped values preserve input order.
  - Time complexity: O(n * d) where n = len(nums) and d is the number of digits per number (d ≤ 10 because nums[i] < 1e9). So effectively O(n).
  - Space complexity: O(n) for the output (sorted list) plus O(1) extra auxiliary space for computing keys (keys are computed once per element by the sort machinery).