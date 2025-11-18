# [Problem 717: 1-bit and 2-bit Characters](https://leetcode.com/problems/1-bit-and-2-bit-characters/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have two character encodings: 0 is a single-bit character, 10 and 11 are two-bit characters. The array always ends with 0. We need to determine whether that final 0 is decoded as a single-bit character or whether it is consumed as the second bit of a preceding two-bit character.

First idea: simulate parsing the bits from left to right greedily. When we see a 0, it must be a one-bit character, so move one step. When we see a 1, it must start a two-bit character (10 or 11), so skip two steps. If we parse until we reach the last position, then the last bit is a one-bit character; otherwise it's part of a two-bit character. This gives an O(n) time, O(1) space solution.

I also recall a neat trick: count how many consecutive 1s appear immediately before the final 0. If that count is odd, the final 0 is part of a two-bit character (because the last two-bit started at that odd 1), so return false; if even, return true.

Edge-case thoughts: array length might be 1 (bits = [0]) -> true. The array always ends with 0 by problem statement.

## Refining the problem, round 2 thoughts
- The greedy parse is straightforward and easy to implement. Stop parsing when i reaches n-1 (the last index) or goes beyond it. If i == n-1 at the end, last is one-bit; else not.
- The counting-ones trick is slightly more clever and also O(n) but requires scanning backwards from the second-last element counting consecutive ones until hitting a 0 or start. If count is even -> true, odd -> false.
- Both are O(n) time and O(1) extra space. The greedy parse is easy to reason about and less error-prone.
- Confirm constraints: n up to 1000 so any linear solution is fine.
- Implementation detail: use while loop carefully to avoid index errors; for greedy approach loop while i < n-1 so we don't accidentally skip checking the last required comparison.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def isOneBitCharacter(self, bits: List[int]) -> bool:
        """
        Greedy parse: iterate from the start, when seeing 1 skip two bits, when seeing 0 skip one bit.
        Stop when we reach or pass the last index. If we exactly land on the last index, it's a one-bit char.
        """
        n = len(bits)
        i = 0
        # parse until the penultimate index; the last bit is guaranteed 0 by problem statement
        while i < n - 1:
            if bits[i] == 1:
                i += 2
            else:
                i += 1
        return i == n - 1
```
- Notes:
  - Approach: Greedy left-to-right parsing. When encountering 1 we know it's the start of a two-bit character so skip the next bit; when encountering 0 it's a one-bit character so move one step.
  - Correctness: Since encoding is unambiguous and greedy picking of smallest valid character at each step matches valid decoding, the final position indicates whether the last bit stands alone.
  - Time complexity: O(n), where n = len(bits), because each iteration advances i by at least 1.
  - Space complexity: O(1) extra space.