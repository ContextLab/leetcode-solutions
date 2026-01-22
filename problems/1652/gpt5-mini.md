# [Problem 1652: Defuse the Bomb](https://leetcode.com/problems/defuse-the-bomb/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The array is circular, and for each index we need the sum of either the next k elements (k>0), the previous |k| elements (k<0), or 0s (k==0). Doing this naively for each index would cost O(n*k) which is okay for n up to 100 but can be simplified.

A sliding window or prefix-sum approach is natural because the sums for neighboring indices overlap heavily. With circularity, I can duplicate the array (or use modulo arithmetic) so window slices don't need special wrap logic. Using prefix sums on an extended array makes computing any contiguous slice O(1).

I should handle k==0 as a special case (all zeros). For k>0, sum indices i+1..i+k (mod n). For k<0, sum indices i-|k|..i-1 (mod n). If I center on the middle copy of code concatenated three times, I can safely take slices without worrying about indices going out of bounds.

## Refining the problem, round 2 thoughts
- Use code2 = code + code + code and compute prefix sums prefix where prefix[t] = sum(code2[:t]). For index i (0..n-1) use center = i + n (middle copy).
  - If k > 0: sum = prefix[center + k + 1] - prefix[center + 1] (slice center+1 .. center+k inclusive).
  - If k < 0 (kpos = -k): sum = prefix[center] - prefix[center - kpos] (slice center-kpos .. center-1 inclusive).
- Time complexity: O(n) to build prefix and O(n) to produce result -> O(n).
- Space complexity: O(n) extra for extended array and prefix (3n and 3n+1), so O(n).
- Edge cases: k == 0 -> return [0]*n. n is small but approach generalizes.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def decrypt(self, code: List[int], k: int) -> List[int]:
        n = len(code)
        if k == 0:
            return [0] * n

        # Build extended array to avoid modular arithmetic complications
        code2 = code + code + code  # length 3n
        m = len(code2)
        prefix = [0] * (m + 1)
        for i in range(m):
            prefix[i + 1] = prefix[i] + code2[i]

        res = [0] * n
        for i in range(n):
            center = i + n  # use the middle copy as the "base"
            if k > 0:
                # sum of next k numbers: indices center+1 .. center+k
                left = center + 1
                right_exclusive = center + k + 1
                res[i] = prefix[right_exclusive] - prefix[left]
            else:
                kpos = -k
                # sum of previous kpos numbers: indices center-kpos .. center-1
                left = center - kpos
                right_exclusive = center
                res[i] = prefix[right_exclusive] - prefix[left]

        return res
```
- [Notes: We extend the array by repeating it three times and use prefix sums to compute any required contiguous slice in O(1). For each original index i we treat the copy in the middle (offset by n) as the reference so that previous/next slices never go out of bounds. Time complexity O(n), space O(n). Implementation handles k == 0 as a special case returning zeros.]