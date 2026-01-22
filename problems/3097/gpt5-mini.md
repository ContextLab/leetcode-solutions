# [Problem 3097: Shortest Subarray With OR at Least K II](https://leetcode.com/problems/shortest-subarray-with-or-at-least-k-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This asks for the shortest contiguous subarray whose bitwise OR is >= k (numeric comparison). My first thought was to treat it like "cover all bits in k" (i.e., track bits that k requires). But numeric comparison isn't the same as "contain all bits set in k": a subarray OR could be >= k by having a higher bit set even if some bits of k are missing (e.g., k = 2 (10b) and OR = 4 (100b) => 4 >= 2). So we must check numeric OR >= k, not just superset of k's bits.

However, bitwise OR across a sliding window has the monotonic property when expanding the window (OR never decreases), and when removing elements we can track bit counts to know when a bit disappears from the window. That suggests a two-pointer / sliding-window approach with per-bit counts and a maintained current OR value. We can expand right pointer, update counts and curr_or; whenever curr_or >= k, try to shrink from left while maintaining curr_or >= k to minimize length.

Because numbers are non-negative and bit-length is bounded (~30 bits for given constraints), recomputing/updating per bit is O(1) per element (constant factor ~30), so overall O(n * bits) ~ O(n).

## Refining the problem, round 2 thoughts
- Handle k == 0: since any non-empty subarray will have OR >= 0, answer is 1 immediately.
- To update OR efficiently when shrinking window, maintain counts per bit: count[b] = how many elements in current window have bit b set. If count[b] transitions 0 -> 1, set that bit in curr_or. If count[b] transitions 1 -> 0, clear that bit.
- Determine number of bits to track using max(nums) and k to avoid unnecessary iterations: bits = max(max(nums), k).bit_length(), but handle the case all zeros (bit_length = 0) by taking at least 1.
- Complexity: O(n * bits) time, O(bits) extra space. With bits <= 31 (per constraints), this is linear in practice.
- Edge cases: all zeros, no subarray meeting requirement (return -1), single-element satisfying, etc.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        if k == 0:
            return 1  # any non-empty subarray works
        
        n = len(nums)
        # Determine number of bits to track based on max value among nums and k
        max_val = max(max(nums) if nums else 0, k)
        bits = max_val.bit_length()
        if bits == 0:
            bits = 1
        
        counts = [0] * bits
        curr_or = 0
        ans = float('inf')
        l = 0
        
        for r in range(n):
            x = nums[r]
            # add nums[r] bits
            for b in range(bits):
                if (x >> b) & 1:
                    counts[b] += 1
                    if counts[b] == 1:
                        curr_or |= (1 << b)
            # try to shrink while condition satisfied
            while curr_or >= k and l <= r:
                ans = min(ans, r - l + 1)
                y = nums[l]
                for b in range(bits):
                    if (y >> b) & 1:
                        counts[b] -= 1
                        if counts[b] == 0:
                            curr_or &= ~(1 << b)
                l += 1
        
        return -1 if ans == float('inf') else ans
```

- Notes about the solution approach:
  - We use a sliding window [l..r]. As r increases, we OR in nums[r] by increasing per-bit counts and setting bits in curr_or when count goes from 0 -> 1.
  - While curr_or >= k, we attempt to shrink l greedily, removing bits by decrementing per-bit counts and clearing bits in curr_or when count becomes 0.
  - Because bit operations are bounded by the bit-length (<= ~31), each element contributes a constant amount of work, giving effectively O(n) time for constraints in the problem.
- Complexity:
  - Time: O(n * B) where B = bit-length of max(nums, k) (<= ~31) => effectively O(n).
  - Space: O(B) for the counts array and O(1) extra variables.