# [Problem 1829: Maximum XOR for Each Query](https://leetcode.com/problems/maximum-xor-for-each-query/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks for a k (< 2^maximumBit) for each query such that XOR of all current nums plus k is maximized. "Maximized" for a XOR result with an upper bound on k's bit-width means we want the result to be as many 1 bits as possible up to maximumBit — i.e., we want the XOR result to be the mask of all 1s of length maximumBit. If current overall XOR is cur, then choose k = cur ^ mask to make (cur ^ k) == mask.

We need answers after successive removals of the last element. That suggests maintaining the XOR of the current array and updating it when removing the last element. Precompute total XOR of the whole array (cur), then for each query (starting with full array) compute k = cur ^ mask, append it, then "remove" the last element by XOR-ing cur with nums[last] to update cur for the next query. Iterate from the last index down to the first.

This is O(n) time and O(1) extra space aside from the answer list.

## Refining the problem, round 2 thoughts
Edge cases:
- maximumBit up to 20 ensures mask fits in Python int easily.
- nums values are already guaranteed < 2^maximumBit.
- The array length n can be up to 1e5, so O(n) is fine; anything quadratic would be too slow.
- Make sure the outputs are in query order: the first output corresponds to the full array, then after each removal. Iterating from last index down and appending answers yields the correct order (first append corresponds to full array). No extra reversal is needed if we iterate from i = n-1 down to 0 and append answers in that order.

Alternative considerations:
- Could compute prefix XORs and then derive answers, but the simpler approach uses the running total XOR and updates by XOR-ing the removed element. This is simplest and minimal extra space.

Time complexity: O(n). Space complexity: O(n) for the output list.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def getMaximumXor(self, nums: List[int], maximumBit: int) -> List[int]:
        # mask of maximumBit ones: e.g., maximumBit=3 -> mask = 0b111 = 7
        mask = (1 << maximumBit) - 1
        
        # total XOR of all elements in nums
        total = 0
        for v in nums:
            total ^= v
        
        res: List[int] = []
        # For each query starting with full array, compute k = total ^ mask,
        # then remove last element by total ^= nums[i].
        for i in range(len(nums) - 1, -1, -1):
            res.append(total ^ mask)
            total ^= nums[i]
        
        return res
```
- Approach: Compute mask = (1 << maximumBit) - 1 (all ones for maximumBit). Maintain the XOR of the current array (starting with XOR of all nums). For each query (starting with full array), the optimal k is current_xor ^ mask; then update current_xor by removing the last element (current_xor ^= nums[last]). Iterate from last index down to first and append answers.
- Time complexity: O(n) where n = len(nums). We compute the total XOR in O(n) and iterate once more in O(n).
- Space complexity: O(n) for the result list. Extra auxiliary space is O(1).
- Implementation details: Iterating from the last element down ensures the appended answers are in the required query order (first entry corresponds to full array).