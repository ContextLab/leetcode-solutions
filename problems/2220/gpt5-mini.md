# [Problem 2220: Minimum Bit Flips to Convert Number](https://leetcode.com/problems/minimum-bit-flips-to-convert-number/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimum number of single-bit flips to turn start into goal. Flipping a bit toggles it; so each position where start and goal differ requires at least one flip. Conversely, flipping exactly those differing positions achieves conversion. That suggests counting differing bit positions. A natural operation to highlight differing bits is XOR: start ^ goal has 1s exactly where bits differ. So count the number of 1s (the popcount / Hamming weight) in start ^ goal. Implementation can use built-in popcount (int.bit_count()) or fallback to bin(...).count('1') or a loop with x &= x-1.

## Refining the problem, round 2 thoughts
- Edge cases: start == goal -> XOR is 0 -> 0 flips. start or goal zero handled naturally.
- Input bounds up to 1e9 (~30 bits), so any popcount method is efficient.
- Time complexity: O(b) where b is number of bits considered (<= 30), effectively constant.
- Space complexity: O(1).
- Multiple implementations possible: builtin bit_count (fast and clean), bin.count, or Kernighan's bit trick.

## Attempted solution(s)
```python
class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        """
        Return the number of differing bits between start and goal,
        which is the popcount of start ^ goal.
        """
        diff = start ^ goal
        # Use Python 3.8+'s int.bit_count() if available
        if hasattr(diff, "bit_count"):
            return diff.bit_count()
        # Fallback: use Kernighan's algorithm to count set bits
        count = 0
        while diff:
            diff &= diff - 1
            count += 1
        return count
```
- Notes:
  - Approach: compute XOR of start and goal, then count set bits in the XOR (each set bit corresponds to one required flip).
  - Time complexity: O(b) where b is number of bits (<= 31 for given constraints) — effectively O(1).
  - Space complexity: O(1).
  - Implementation detail: code uses int.bit_count() when available for clarity and speed; falls back to Kernighan's loop otherwise.