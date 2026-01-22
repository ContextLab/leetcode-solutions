# [Problem 976: Largest Perimeter Triangle](https://leetcode.com/problems/largest-perimeter-triangle/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share my internal stream-of-consciousness. Instead, here's a concise summary of the straightforward approach that comes to mind:

- Key observation: for three side lengths to form a non-degenerate triangle, the sum of the two smaller sides must be greater than the largest side (triangle inequality).
- To maximize perimeter, it's natural to consider the largest lengths first: sort the array in descending order and check consecutive triples. The first triple that satisfies the triangle inequality yields the maximum perimeter.

## Refining the problem, round 2 thoughts
I won't provide internal chain-of-thought, but here are clear refinements and considerations:

- Sorting in descending order lets us check triples (nums[i], nums[i+1], nums[i+2]) so the first valid triple encountered has the maximum possible perimeter.
- Edge cases: if no triple satisfies the triangle inequality, return 0. Arrays have at least length 3 by constraints.
- Alternatives: sort ascending and iterate from the end; or use counting sort / frequency array if optimizing for the value range (nums[i] ≤ 1e6) and very large n, but standard sort is fine for n ≤ 1e4.
- Complexity: sorting dominates — O(n log n) time and O(1) extra space (or O(n) depending on sorting implementation).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        # Sort in descending order so that we check largest possible perimeters first.
        nums.sort(reverse=True)
        # Check every consecutive triple; first valid one gives the largest perimeter.
        for i in range(len(nums) - 2):
            a, b, c = nums[i], nums[i+1], nums[i+2]
            # triangle inequality for non-degenerate triangle: sum of two smaller > largest
            if b + c > a:
                return a + b + c
        return 0
```
- Notes:
  - Approach: sort descending and check consecutive triplets for b + c > a.
  - Time complexity: O(n log n) due to sorting (n = len(nums)). The subsequent scan is O(n).
  - Space complexity: O(1) additional space beyond input (or O(n) if the language's sort uses extra space).