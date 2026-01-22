# [Problem 2938: Separate Black and White Balls](https://leetcode.com/problems/separate-black-and-white-balls/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We want all 0s (white) on the left and all 1s (black) on the right. Swapping adjacent balls is the only operation. That sounds like sorting a binary string with adjacent swaps; the minimum number of adjacent swaps needed to achieve all 0s before all 1s should equal the number of inversions where a 1 appears before a 0. So count pairs (i < j) with s[i] = '1' and s[j] = '0'. A direct way: scan from left to right, keep how many 1s we've seen; each time we see a 0 we add that count because each earlier 1 must pass this 0.

## Refining the problem, round 2 thoughts
This approach is O(n) time and O(1) extra space. Edge cases: all 0s or all 1s yield 0. The number of inversions can be as large as O(n^2) in the worst distribution (e.g., half 1s followed by half 0s), but Python integers handle large values. Implementation is straightforward: one pass, maintain ones_count and accumulate answer when encountering '0'. No need for more complex data structures (Fenwick tree, etc.) here because only two values exist.

## Attempted solution(s)
```python
class Solution:
    def minimumMoves(self, s: str) -> int:
        # Count number of inversions where '1' is before '0'
        ones = 0
        swaps = 0
        for ch in s:
            if ch == '1':
                ones += 1
            else:  # ch == '0'
                swaps += ones
        return swaps
```
- Notes:
  - Approach: Count inversions (pairs (i, j) with i < j, s[i] = '1', s[j] = '0'). Each such pair requires one adjacent swap in any optimal sequence, so the sum is the minimum number of swaps.
  - Time complexity: O(n), where n = len(s) — single pass over the string.
  - Space complexity: O(1) extra space (only a couple of counters).
  - Works for all constraints (n up to 1e5). Python integers can hold the result even when it's on the order of n^2.