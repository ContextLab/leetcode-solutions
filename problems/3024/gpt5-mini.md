# [Problem 3024: Type of Triangle](https://leetcode.com/problems/type-of-triangle/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share stream-of-consciousness or internal chain-of-thought. Here is a concise summary of the approach instead:
- Sort the three side lengths so we can check the triangle inequality simply as a + b > c.
- If they do not satisfy that inequality, return "none".
- Otherwise classify by equality: all equal -> "equilateral", exactly two equal -> "isosceles", none equal -> "scalene".

## Refining the problem, round 2 thoughts
I won’t provide internal step-by-step reasoning, but a brief, focused refinement:
- Edge cases: degenerate triangle where a + b == c is not allowed (return "none").
- No special handling needed for constraints since nums.length == 3 and values are positive.
- Sorting three values is trivial; an alternative is checking three inequalities directly without sorting, but sorting keeps the code simple and readable.
- Time/space: constant work for fixed-size input (O(1) time and O(1) extra space).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def triangleType(self, nums: List[int]) -> str:
        # Sort sides to simplify the triangle inequality check
        a, b, c = sorted(nums)
        # Check triangle inequality (strict)
        if a + b <= c:
            return "none"
        # Classify by equality
        if a == b == c:
            return "equilateral"
        if a == b or b == c or a == c:
            return "isosceles"
        return "scalene"
```
- Notes:
  - Approach: sort the sides, check a + b > c, then classify by equality counts.
  - Time complexity: O(1) for this problem (sorting three elements is constant-time). If generalized to n sides, sorting would be O(n log n).
  - Space complexity: O(1) extra space (ignoring input).