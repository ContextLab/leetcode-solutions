# [Problem 2381: Shifting Letters II](https://leetcode.com/problems/shifting-letters-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to apply many range shifts (forward or backward) to characters in s. Doing each shift by iterating from start to end would be O(m * k) in the worst case (m = number of shifts, k = average range length), which could be O(n * m) and too slow for 5e4. This is a classical use-case for a difference array (range-add via two point updates) so I can accumulate net shifts per index in O(m + n). Each shift contributes +1 (forward) or -1 (backward) to a contiguous range. If I maintain a diff array of length n+1, I can add at start and subtract at end+1, then prefix-sum to get total shifts for each position. Finally map each character by (char_index + net_shift) mod 26.

## Refining the problem, round 2 thoughts
- Use diff array length n+1 initialized to zeros.
- For each shifts[i] = [l, r, dir]:
  - delta = 1 if dir == 1 else -1
  - diff[l] += delta
  - diff[r+1] -= delta
- After processing all shifts, compute prefix sums for indices 0..n-1 to get net shift for each char.
- Apply net shift modulo 26 to each character. Use (ord(c) - ord('a') + net_shift) % 26 to handle negatives and wrap-around.
- Complexity: O(n + m) time and O(n) extra space.
- Edge cases: ensure r+1 update is safe by using diff of size n+1; negative net shifts must be handled via modulo.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def shiftingLetters(self, s: str, shifts: List[List[int]]) -> str:
        n = len(s)
        diff = [0] * (n + 1)
        
        # Apply range updates on diff array
        for l, r, direction in shifts:
            delta = 1 if direction == 1 else -1
            diff[l] += delta
            diff[r + 1] -= delta
        
        # Prefix sum to get net shifts for each position
        res_chars = []
        curr = 0
        for i, ch in enumerate(s):
            curr += diff[i]
            # reduce curr modulo 26 to avoid big numbers (handles negatives correctly)
            shift = curr % 26
            base = ord(ch) - ord('a')
            new_char = chr((base + shift) % 26 + ord('a'))
            res_chars.append(new_char)
        
        return ''.join(res_chars)
```
- Notes:
  - Approach: difference array for range updates and a single pass prefix-sum to compute net shift per index, then apply shifts to characters.
  - Time complexity: O(n + m), where n = len(s) and m = len(shifts).
  - Space complexity: O(n) extra for the diff array and output buffer.
  - Important details: using diff of size n+1 prevents index errors when doing r+1 updates. Taking curr % 26 before applying to characters prevents large intermediate values and properly handles negative totals.