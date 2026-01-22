# [Problem 2134: Minimum Swaps to Group All 1's Together II](https://leetcode.com/problems/minimum-swaps-to-group-all-1s-together-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to group all 1's together in a circular binary array with the minimum number of swaps. Swapping two positions can move a 1 inside a target block and a 0 outside it. If there are k ones total, then in any contiguous block of length k (considering the array circularly) the number of zeros in that block tells how many swaps are needed to make that block all ones (each zero must be swapped with a one outside). So the problem reduces to finding, over all circular windows of length k, the minimum number of zeros (or equivalently the maximum number of ones). A sliding window over a doubled array (or using modulo indices) will let me check all n possible windows in O(n).

## Refining the problem, round 2 thoughts
Edge cases:
- If k = 0 or k = 1 (no ones or just one one), answer is 0 because no swaps needed.
- If k = n (all ones), also 0.
Implementation details:
- Compute k = sum(nums).
- Use an extended array (nums concatenated with itself) or maintain circular indices to slide a window of length k across n starting positions.
- For efficiency, keep a running count of ones in the current window and update by subtracting the leaving element and adding the entering element.
Time/space:
- Time O(n).
- Space O(n) if using explicit doubled array, or O(1) extra if using modulo indexing. Doubled array is simpler and still within limits (n <= 1e5 -> 2n <= 2e5).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        n = len(nums)
        k = sum(nums)
        # If there are 0 or 1 ones, or all are ones, no swaps needed.
        if k <= 1 or k == n:
            return 0
        
        # Extend the array to handle circular windows
        ext = nums + nums  # length 2n
        
        # Initial window [0, k)
        curr_ones = sum(ext[:k])
        min_zeros = k - curr_ones
        
        # Slide window starting positions 1..n-1
        for i in range(1, n):
            # Remove ext[i-1], add ext[i+k-1]
            curr_ones += ext[i + k - 1] - ext[i - 1]
            zeros = k - curr_ones
            if zeros < min_zeros:
                min_zeros = zeros
        
        return min_zeros
```
- Notes:
  - Approach: Count total ones k. Slide a window of length k across the circular array (implemented by duplicating nums). The minimum zeros in any such window is the answer because each zero inside the target block requires one swap with a one outside.
  - Time complexity: O(n) — we compute sum once and then update the sliding window n-1 times.
  - Space complexity: O(n) due to the duplicated array (could be reduced to O(1) by using modulo indexing instead of creating ext).