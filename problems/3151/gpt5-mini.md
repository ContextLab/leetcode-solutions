# [Problem 3151: Special Array I](https://leetcode.com/problems/special-array-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is straightforward: a "special" array requires every adjacent pair to have different parity (one even, one odd). So for each adjacent pair nums[i-1], nums[i], their parity (nums[i] % 2) must differ. Immediate approach: scan the array once and compare parities of consecutive elements. If any pair has same parity, return False; if the loop finishes, return True. A single-element array trivially satisfies the condition.

## Refining the problem, round 2 thoughts
Edge cases:
- Length 1: return True.
- All numbers within small bounds but that doesn't change the approach.
Alternative approaches (not necessary here):
- Build a parity array and check adjacent entries, but that's equivalent and uses extra space.
- Use XOR of parities: (a%2) ^ (b%2) == 1 means different parity. But simple equality comparison of (a%2) == (b%2) is enough.

Time complexity: O(n) where n = len(nums). Space complexity: O(1) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def isSpecialArray(self, nums: List[int]) -> bool:
        # Check consecutive elements for differing parity
        for i in range(1, len(nums)):
            if (nums[i] % 2) == (nums[i-1] % 2):
                return False
        return True
```
- Notes: The solution iterates once through the list and compares parity of each element with its predecessor. If any two adjacent elements have the same parity, the array is not special. Time complexity O(n), space complexity O(1). The modulo operation is constant-time and values are within given constraints.