# [Problem 1545: Find Kth Bit in Nth Binary String](https://leetcode.com/problems/find-kth-bit-in-nth-binary-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The string S_n is defined recursively: S_n = S_{n-1} + "1" + reverse(invert(S_{n-1})). The length of S_n is 2^n - 1, so there's a clear middle position at 2^{n-1}. The middle bit is always "1" for n>1 (S_1 = "0"). If k is before the middle, it's just the kth bit of S_{n-1}. If k is after the middle, it's located in reverse(invert(S_{n-1})), so it corresponds to some position in S_{n-1} but inverted. That suggests a recursion: map k to a smaller problem and invert when we cross into the mirrored-inverted half. Depth is at most n <= 20, so recursion is safe.

## Refining the problem, round 2 thoughts
Map precisely: length L_n = 2^n - 1, mid = 2^{n-1}. If k == mid -> "1". If k < mid -> findKthBit(n-1, k). If k > mid -> position in reversed part maps to index j = L_n - k + 1 = 2^n - k (this j is in [1, 2^{n-1}-1], a valid index for S_{n-1}). The bit at k is invert(findKthBit(n-1, j)). Implement recursive solution directly or iterative loop tracking parity of inversion. Complexity is O(n) time and O(n) stack (n <= 20), constant extra space otherwise.

Edge cases: n=1 (only "0"), k=1; k exactly equals middle; largest n=20 but recursion depth small.

## Attempted solution(s)
```python
class Solution:
    def findKthBit(self, n: int, k: int) -> str:
        # recursive approach
        def helper(n: int, k: int) -> str:
            if n == 1:
                return '0'
            mid = 1 << (n - 1)  # 2^(n-1)
            if k == mid:
                return '1'
            if k < mid:
                return helper(n - 1, k)
            # k > mid: map to mirrored index in S_{n-1}
            j = (1 << n) - k  # 2^n - k
            bit = helper(n - 1, j)
            return '1' if bit == '0' else '0'
        return helper(n, k)
```
- Notes on approach:
  - We use the recursive structure of S_n. The middle is always '1' for n>1. If k is in the first half we recurse directly. If k is in the mirrored-inverted second half, we map to the mirrored index in S_{n-1} and invert the result.
  - Time complexity: O(n) because each recursive call reduces n by 1 and n <= 20.
  - Space complexity: O(n) due to recursion call stack. Iterative approach could reduce auxiliary stack usage but is unnecessary here given constraints.