# [Problem 781: Rabbits in Forest](https://leetcode.com/problems/rabbits-in-forest/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The question asks for the minimum number of rabbits consistent with answers where answers[i] is how many other rabbits share the same color as rabbit i. If a rabbit answers r, that means there are r+1 rabbits of that color total. Multiple rabbits giving the same r could belong to the same color-group(s). For a given r, if k rabbits answered r, then they could form one or more groups of size (r+1). To minimize total rabbits we want to pack them into as few full groups as possible, but if k is not a multiple of (r+1) we still must count an entire extra group. So for each r we need ceil(k / (r+1)) groups, contributing groups * (r+1) rabbits. Summing across distinct r gives the minimum total.

I should count frequencies of answers and for each value compute groups = (count + r) // (r+1) (integer ceil) and contribute groups*(r+1).

Edge cases: r = 0 => group size 1, groups = count. answers may be large but length <= 1000. Implementation straightforward with Counter.

## Refining the problem, round 2 thoughts
- Use collections.Counter to get counts of each response value.
- For each response value r with frequency c:
  - group_size = r + 1
  - groups_needed = (c + group_size - 1) // group_size  (integer ceiling)
  - add groups_needed * group_size to result
- Complexity: O(n) time and O(m) extra space (m = number of distinct answers ≤ n).
- All answers are non-negative and < 1000, so no overflow concerns.
- Example check: answers=[1,1,2] → counts: 1:2 → group_size=2 → groups=1 → add 2. 2:1 → group_size=3 → groups=1 → add 3 → total 5.
- Example [10,10,10] → group_size=11, count=3 → groups=1 → add 11.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def numRabbits(self, answers: List[int]) -> int:
        freq = Counter(answers)
        total = 0
        for r, c in freq.items():
            group_size = r + 1
            groups = (c + group_size - 1) // group_size  # ceil(c / group_size)
            total += groups * group_size
        return total
```
- Notes:
  - Approach: Count frequency of each answer r. Each distinct r implies groups of size r+1. The minimum number of groups to cover count c is ceil(c/(r+1)). Total rabbits contributed is groups*(r+1). Sum for all r.
  - Time complexity: O(n) where n = len(answers) to build the counter and iterate over keys.
  - Space complexity: O(m) for the counter where m is the number of distinct answer values (m ≤ n).
  - Handles r = 0 correctly since group_size = 1 and groups = c.