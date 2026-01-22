# [Problem 1304: Find N Unique Integers Sum up to Zero](https://leetcode.com/problems/find-n-unique-integers-sum-up-to-zero/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to return n unique integers whose sum is 0. The simplest idea that comes to mind is to use symmetric pairs: for every positive integer k include both k and -k. Those pairs sum to zero, so picking m such pairs gives 2m numbers summing to 0. If n is odd, I can also include 0 to reach an odd count while keeping the sum 0. This yields a straightforward construction that guarantees uniqueness and correctness.

Other ideas: pick the first n-1 arbitrary distinct integers and make the last one the negative of their sum (must ensure it's distinct). That also works but needs a small check to avoid collision. The symmetric pairs approach is simpler and clean.

## Refining the problem, round 2 thoughts
- Edge cases: n = 1 should return [0]. The pair approach handles this (no pairs, then include 0).
- For even n, just produce n/2 pairs (k, -k). For odd n, produce (n-1)/2 pairs and include 0.
- Complexity is linear: O(n) time and O(n) extra space to hold the array.
- Alternative: produce numbers from -(n//2) to n//2 skipping or including 0 appropriately; but explicit pairing is clear and easy.
- No overflow concerns given constraints (n <= 1000).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def sumZero(self, n: int) -> List[int]:
        res = []
        # Add pairs (i, -i)
        for i in range(1, n // 2 + 1):
            res.append(i)
            res.append(-i)
        # If n is odd, include 0
        if n % 2 == 1:
            res.append(0)
        return res
```
- Notes:
  - Approach: build n//2 symmetric pairs (i, -i). If n is odd, append 0.
  - Correctness: pairs sum to 0; adding 0 doesn't change sum. All values are unique.
  - Time complexity: O(n) — we perform a constant amount of work per output element.
  - Space complexity: O(n) — the returned list of n integers.