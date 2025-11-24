# [Problem 1018: Binary Prefix Divisible By 5](https://leetcode.com/problems/binary-prefix-divisible-by-5/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check for each prefix treated as a binary number whether it's divisible by 5. The naive way would be to compute the integer value of each prefix and test % 5, but prefix values grow exponentially with length and could become large (though Python can handle big ints, it's wasteful). Observing modular arithmetic: if current prefix value is v, and next bit is b, new value is v' = 2*v + b. So I can just keep v mod 5 and update v = (2*v + b) % 5. Then check v == 0. That is O(1) work per element and avoids large numbers.

## Refining the problem, round 2 thoughts
Edge cases: leading zeros (e.g., [0,0,...]) should produce True for any prefix that equals 0. The modulo approach handles that naturally. Complexity: single pass O(n) time, O(n) output space. No tricky corner cases beyond ensuring we update remainder correctly. Alternative would be to build full integers or use bit shifting, but remainder tracking is simplest and most efficient.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def prefixesDivBy5(self, nums: List[int]) -> List[bool]:
        res: List[bool] = []
        rem = 0  # current prefix value modulo 5
        for bit in nums:
            rem = (rem * 2 + bit) % 5
            res.append(rem == 0)
        return res
```
- Notes:
  - Approach: maintain remainder rem = current_prefix % 5, update rem = (2*rem + bit) % 5 for each incoming bit, and record whether rem == 0.
  - Time complexity: O(n), where n = len(nums), since we do O(1) work per element.
  - Space complexity: O(n) for the output list (plus O(1) extra for rem).
  - This avoids constructing large integers and uses modular arithmetic to stay efficient.