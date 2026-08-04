# [Problem 3731: Find Missing Elements](https://leetcode.com/problems/find-missing-elements/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The array contains unique integers and originally contained every integer in some contiguous range. The smallest and largest of that original range are still present in nums, so the full intended range is simply [min(nums), max(nums)]. We need to return the integers in that range that are not present in nums, sorted. 

First idea: compute min and max, then for each value in that inclusive range check if it's in nums. Checking membership repeatedly is easiest/faster with a set. Alternatively, sort nums and scan adjacent pairs to output gaps, but sorting is unnecessary since we only need min, max and membership. Edge cases: if no missing integers, return empty list. nums length is at least 2, values ≤ 100, so range iteration cost is small.

## Refining the problem, round 2 thoughts
- Use a set for O(1) membership checks, iterate from min to max inclusive and collect numbers not in the set. This yields sorted output naturally because we iterate in increasing order.
- Sorting approach would be O(n log n) and needs extra handling, while set + range iteration is O(n + R) where R = max - min.
- Edge cases: if min == max (not possible here because length >= 2 and unique, but if it happened we'd return []), or if all numbers are present, return [].
- Space usage: O(n) for the set. Given constraints (nums.length ≤ 100, values ≤ 100), both time and space are trivial.
- Complexity: time O(n + (max-min)), space O(n).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findMissing(self, nums: List[int]) -> List[int]:
        if not nums:
            return []
        lo, hi = min(nums), max(nums)
        s = set(nums)
        return [x for x in range(lo, hi + 1) if x not in s]
```
- Notes:
  - Approach: compute min and max of nums to get the full intended range, build a set of nums for O(1) membership checks, then iterate the inclusive range and collect any values not present.
  - Time complexity: O(n + R) where n = len(nums) and R = max(nums) - min(nums). In worst case with constraints this is at most O(200) roughly, so effectively linear.
  - Space complexity: O(n) for the set and O(k) for the output list where k is the number of missing integers.