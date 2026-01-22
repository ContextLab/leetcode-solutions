# [Problem 1534: Count Good Triplets](https://leetcode.com/problems/count-good-triplets/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks to count triplets (i, j, k) with i < j < k that satisfy three absolute-difference constraints among arr[i], arr[j], arr[k]. It smells like a straightforward brute-force enumeration problem since constraints are small: arr.length <= 100. The naive triple loop (i, j, k) will at most consider ~100^3 = 1,000,000 combinations, which is easily feasible in Python for this problem.

A small optimization is to check the first condition |arr[i] - arr[j]| <= a before iterating over k, so we avoid the innermost loop when the pair (i, j) already fails. But asymptotically it's still O(n^3) in the worst case. No fancy data structures are necessary.

## Refining the problem, round 2 thoughts
- Edge cases: n is guaranteed >= 3 by constraints, so we don't need extra handling for too-short arrays.
- Values can be up to 1000 but that doesn't matter for complexity.
- Alternative approaches: We could try counting using frequency buckets or more advanced indexing for larger constraints, but given n <= 100, the simple solution is preferable for clarity and reliability.
- Time complexity: O(n^3) worst-case (with a small short-circuit optimization that can reduce work in practice). Space complexity: O(1) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countGoodTriplets(self, arr: List[int], a: int, b: int, c: int) -> int:
        n = len(arr)
        count = 0
        # enumerate i < j < k
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                # early check to avoid unnecessary k iterations
                if abs(arr[i] - arr[j]) > a:
                    continue
                for k in range(j + 1, n):
                    if abs(arr[j] - arr[k]) <= b and abs(arr[i] - arr[k]) <= c:
                        count += 1
        return count
```
- Notes:
  - Approach: Triple nested loops enumerating all ordered triplets with i < j < k. We check the first constraint (between i and j) before entering the innermost loop to prune some work.
  - Time complexity: O(n^3) in the worst case, where n = len(arr). With n <= 100, this is acceptable (<= 1e6 triplet checks).
  - Space complexity: O(1) extra space (only counters and loop indices).