# [Problem 3191: Minimum Operations to Make Binary Array Elements Equal to One I](https://leetcode.com/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see a binary array and an operation that flips any 3 consecutive elements. We want minimum operations to make all elements 1 or report -1. Flipping 3 consecutive is local and deterministic; this suggests a greedy left-to-right approach: when we encounter a 0, we should flip starting at that index to fix it. But flips overlap and earlier flips affect later bits, so I need to account for parity of applied flips at each position.

A naive approach actually applying flips on the array costs O(n * 3) which is fine but if we literally toggle values repeatedly it is OK for n up to 1e5 (still OK) but we should avoid repeated touching of same elements unnecessarily. A common trick is to maintain a running parity of how many flips currently affect the current index, using a difference array or queue to know when a flip's effect ends (after 3 positions). That gives O(n) time and O(n) extra space.

Edge case: if a 0 appears in the last two indices we cannot flip (requires 3 consecutive), so answer is -1.

## Refining the problem, round 2 thoughts
Refine to exact algorithm:
- Iterate i from 0 to n-1.
- Maintain parity (0 or 1) of active flips affecting index i.
- Use an array diff of size n+1 initialized to 0; when we start a flip at i we toggle parity and set diff[i+3] ^= 1 so that when we reach index i+3 we remove that flip's effect (parity toggles back).
- At each i, first parity ^= diff[i] to clear any flips that ended at i. Then the effective value at i is nums[i] ^ parity. If that's 0 and we can start a flip (i <= n-3), we start one; otherwise if it's 0 and i > n-3 we cannot fix it and return -1.
Time complexity O(n), space O(n) for diff array. Could reduce space to O(1) with a circular buffer of size 3, but O(n) is fine and simple.

Corner cases: n is at least 3 by constraints. Ensure diff indexing safe by sizing n+1.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        # diff[i] will be 1 if some flip scheduled at index i-3 ends here (i.e., parity should toggle at i)
        diff = [0] * (n + 1)
        parity = 0  # current parity of flips affecting this index (0 = even flips, 1 = odd flips)
        ops = 0

        for i in range(n):
            # remove effect of flips that end at i
            parity ^= diff[i]
            current = nums[i] ^ parity
            if current == 0:
                # need to flip starting at i, but ensure we have room for 3 elements
                if i > n - 3:
                    return -1
                ops += 1
                parity ^= 1          # starting a flip toggles parity for i, i+1, i+2
                diff[i + 3] ^= 1     # schedule removal of this flip's effect at position i+3

        return ops
```
- Notes:
  - Approach: left-to-right greedy using a difference array to track when a flip's effect ends. If at position i the effective bit is 0 we must flip there (if possible) to make it 1; otherwise impossible.
  - Time complexity: O(n) — we do O(1) work per index.
  - Space complexity: O(n) due to the diff array (can be reduced to O(1) with a size-3 circular buffer if desired).
  - Correctness: Each flip is only started when necessary and only at leftmost possible position to fix that 0; overlapping flips are handled via parity bookkeeping, ensuring minimum flips.