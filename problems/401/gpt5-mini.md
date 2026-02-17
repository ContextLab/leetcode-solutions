# [Problem 401: Binary Watch](https://leetcode.com/problems/binary-watch/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This problem describes a small search space: hours use 4 LEDs (0-11) and minutes use 6 LEDs (0-59). We are given the total number of LEDs that are on and asked to return all valid times with exactly that many bits set. My first thought is to brute-force all possible hour/minute pairs (12 * 60 = 720 possibilities) and check how many bits are set in the combined representation (or separately in hour and minute and sum). That's trivial and very fast given the tiny fixed search space.

Another idea is combinatorial: choose k bits among 10 positions and interpret which belong to hours vs minutes. That works but is more complex and unnecessary since brute force is constant-time for this input size.

Edge cases: turnedOn = 0 (should return "0:00"). turnedOn > 10 yields no solutions (but the brute-force will just return empty). Minutes must be zero-padded to two digits; hours must not have leading zero.

## Refining the problem, round 2 thoughts
Refinements:
- Validate hours < 12 and minutes < 60 while iterating.
- Use Python's int.bit_count() (or bin(x).count('1')) to get number of set bits efficiently.
- Complexity is constant (720 checks), so time/space are trivial. We should return times in any order.

Alternative:
- Use combination generation by splitting turnedOn into h_bits (0..min(4, turnedOn)) and m_bits = turnedOn - h_bits and generate hour values with h_bits ones and minute values with m_bits ones. That's slightly more structured but not necessary.

Complexity:
- Time: O(12 * 60) = O(1) practically, or O(720) operations.
- Space: O(number of valid times) in the output, at most 720 but practically far smaller.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def readBinaryWatch(self, turnedOn: int) -> List[str]:
        # If turnedOn is impossible (> 10), early return (optional)
        if turnedOn < 0 or turnedOn > 10:
            return []
        
        res = []
        for h in range(12):       # hours: 0..11
            for m in range(60):   # minutes: 0..59
                # Use int.bit_count() for efficient bit counting (Python 3.8+)
                if (h.bit_count() + m.bit_count()) == turnedOn:
                    res.append(f"{h}:{m:02d}")
        return res
```
- Notes:
  - Approach: brute-force iterate all 12 * 60 possible times and count the number of set bits in hour and minute; format minutes with two digits.
  - Complexity: Time O(720) = O(1) practically; Space O(R) where R is number of results returned.
  - Implementation detail: Using int.bit_count() is efficient; if unavailable, bin(x).count('1') can be used instead. The hour has no leading zero (string formatting of h as int achieves that), and minutes are zero-padded with :02d formatting.