# [Problem 868: Binary Gap](https://leetcode.com/problems/binary-gap/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks for the largest distance between two consecutive 1s in the binary representation of n. First thought: convert n to its binary string via bin(n)[2:] and scan for '1' positions — that's straightforward and easy to implement. Alternatively, I can iterate over bits using bitwise operations which avoids creating a string and is slightly more direct/efficient. Edge cases: numbers that have only one '1' (like powers of two) should return 0. Consecutive ones have distance 1. The binary length is at most ~30 bits (since n <= 1e9), so any approach linear in number of bits is fine.

## Refining the problem, round 2 thoughts
Using bitwise scanning: maintain the index of the previous '1' seen (initialized to -1 or None). Iterate bit positions i = 0,1,... while n > 0: if (n & 1) == 1 and previous != -1 compute gap = i - previous and update max_gap; then set previous = i. Right-shift n each iteration and increment i. This uses O(1) extra space and O(log n) time. With the string approach, you would collect indices of '1's and take max difference between consecutive indices — simpler to reason about but slightly less "bitwise". Both are correct; I'll implement the bitwise approach. Confirm edge cases: if no previous '1' was seen or only one '1' total, max_gap remains 0.

## Attempted solution(s)
```python
class Solution:
    def binaryGap(self, n: int) -> int:
        prev = -1
        max_gap = 0
        index = 0
        while n:
            if n & 1:
                if prev != -1:
                    max_gap = max(max_gap, index - prev)
                prev = index
            n >>= 1
            index += 1
        return max_gap
```
- Notes:
  - Approach: bitwise scan from least-significant to most-significant bit, tracking last seen '1' index and updating the maximum difference when encountering a new '1'.
  - Time complexity: O(log n) — we examine each bit once (log2(n) bits).
  - Space complexity: O(1) — only a few integer variables used.
  - Implementation detail: Using n >>= 1 and an index counter avoids building the binary string and keeps the code concise and efficient.