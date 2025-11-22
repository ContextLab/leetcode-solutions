# [Problem 3190: Find Minimum Operations to Make All Elements Divisible by Three](https://leetcode.com/problems/find-minimum-operations-to-make-all-elements-divisible-by-three/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We only care about each number modulo 3. For a number x, let r = x % 3:
- If r == 0, it's already divisible by 3 (cost 0).
- If r == 1, we can subtract 1 (cost 1) or add 2 (cost 2) — best is 1.
- If r == 2, we can add 1 (cost 1) or subtract 2 (cost 2) — best is 1.

So each element with remainder 1 or 2 costs exactly 1 operation. That suggests the answer is simply the count of elements with remainder != 0. I briefly wondered if operations could be shared or paired to reduce cost, but operations act on single elements independently (add/subtract 1 to any element), so there's no sharing advantage.

## Refining the problem, round 2 thoughts
- Edge cases: small arrays, all already divisible by 3 -> answer 0. Works fine.
- Alternative expression: sum(min(r, 3-r) for each remainder r) which reduces here to counting nonzero remainders since min(1,2)=1 and min(2,1)=1.
- Time complexity: O(n) where n = len(nums).
- Space complexity: O(1) extra (ignoring input), only a counter required.
- Implementation detail: use generator expression to count nums with x % 3 != 0 for succinctness.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        # Each element with remainder 1 or 2 needs exactly 1 operation to become divisible by 3.
        return sum(1 for x in nums if x % 3 != 0)
```
- Notes:
  - Approach: Count how many elements have remainder 1 or 2 modulo 3. Each such element requires one +1 or -1 operation.
  - Time complexity: O(n), single pass over the array.
  - Space complexity: O(1) extra (generator uses constant extra memory).