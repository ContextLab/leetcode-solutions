# [Problem 2401: Longest Nice Subarray](https://leetcode.com/problems/longest-nice-subarray/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I'm thinking: naive solution would test every subarray and check all pairs for bitwise AND == 0, but that's O(n^2) subarrays and O(k^2) per check — too slow for n up to 1e5. The condition "bitwise AND of every pair in subarray is 0" means no two numbers in the subarray share a common set bit. That suggests tracking which bits are present in the current window. A sliding window (two pointers) seems natural: expand right while the new number doesn't share a bit with the current window; otherwise move left until it no longer conflicts. We can keep an integer mask representing OR of bits in the window. To remove numbers from the left, I need a correct way to update the mask; if the window is always "nice" before adding the new number, then each set bit in mask corresponds to exactly one element in the window, so XORing mask with nums[left] will clear those bits safely. That allows O(n) time.

## Refining the problem, round 2 thoughts
Refinements / checks:
- Why is mask ^= nums[l] safe when removing left? Because before adding the new element, the window satisfied the "nice" property — so no bit is set in more than one element inside it. Therefore each set bit in mask belongs to exactly one element; removing that element removes those bits from mask, and XOR clears exactly those bits.
- Edge cases: single-element arrays are fine. Large numbers have up to ~30 bits (nums[i] <= 1e9), so integer bit operations are safe.
- Alternative would be to keep a bit count array[0..30], decrement counts when removing left, and clear mask bit when count becomes 0. That uses more bookkeeping but is also correct.
- Complexity: each element is added once and removed at most once => O(n) time, O(1) extra space (mask and pointers).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestNiceSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        left = 0
        mask = 0  # OR of bits present in current window
        best = 0

        for right in range(n):
            num = nums[right]
            # If conflict (some bit already present), shrink from left
            while (mask & num) != 0:
                # remove nums[left] bits from mask; safe because window before adding num is "nice"
                mask ^= nums[left]
                left += 1
            # Now safe to include num
            mask |= num
            best = max(best, right - left + 1)

        return best
```
- Notes:
  - Approach: two-pointer sliding window with a rolling bitmask `mask` storing the OR of bits present in the current window. For each new element `num` at right, while `mask & num` != 0 (conflict), remove the leftmost element by XORing its bits out of `mask` and increment `left`. Then include `num` by ORing it into `mask`. Update maximum window length.
  - Correctness detail: before adding `num`, the current window is "nice", so no bit is present in more than one element. Thus XORing `mask` with `nums[left]` safely clears exactly the bits contributed by `nums[left]`.
  - Time complexity: O(n). Each element enters the window once and leaves at most once.
  - Space complexity: O(1) extra space (mask and pointer variables).