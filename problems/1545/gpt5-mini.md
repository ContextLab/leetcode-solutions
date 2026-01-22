# [Problem 1545: Find Kth Bit in Nth Binary String](https://leetcode.com/problems/find-kth-bit-in-nth-binary-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see S_n is built recursively: S_n = S_{n-1} + "1" + reverse(invert(S_{n-1})). Length grows as 2^n - 1. The middle position is exactly 2^{n-1}. If k equals the middle, answer is '1' immediately. If k is in the left half it is the same as the kth bit of S_{n-1}. If k is in the right half it corresponds to some mirrored position in S_{n-1} but inverted. So we can map k in the right half to a position in S_{n-1} and flip the bit. That suggests a recursive solution, but you can avoid building strings entirely and just recurse/iterate on n and k, tracking how many flips (inversions) are applied.

## Refining the problem, round 2 thoughts
We don't need to construct the string because n ≤ 20 and we can compute index mapping. Using recursion is straightforward (base S1 = '0'). Alternatively an iterative approach keeps a flip parity and reduces (n, k) until we hit n = 1. Each time k > mid we map k to the mirrored index (2^n - k) and toggle flip parity. Time is O(n) and space O(1) (or O(n) if recursion used). Edge cases: when k == mid return '1'. k is guaranteed valid.

## Attempted solution(s)
```python
class Solution:
    def findKthBit(self, n: int, k: int) -> str:
        # iterative approach: reduce (n, k) until base case n == 1
        flip = 0  # parity of inversions (0 = no invert, 1 = invert)
        while n > 1:
            mid = 1 << (n - 1)  # 2^(n-1)
            if k == mid:
                return '1' if flip == 0 else '0'
            if k > mid:
                # map to mirrored position in S_{n-1} and toggle inversion parity
                k = (1 << n) - k
                flip ^= 1
            # move to previous string
            n -= 1
        # n == 1 -> S1 = "0"
        return '1' if flip == 1 else '0'
```
- Approach: Iteratively reduce n while mapping k when it's in the right half; track inversion parity instead of building strings.
- Time complexity: O(n) (at most n iterations), where n ≤ 20.
- Space complexity: O(1) extra space (iterative). Recursive variant would use O(n) call stack.
- Important detail: mid = 2^(n-1) is the exact middle index of S_n (1-based). When k > mid, the mirrored index in S_{n-1} is 2^n - k.