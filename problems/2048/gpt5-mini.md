# [Problem 2048: Next Greater Numerically Balanced Number](https://leetcode.com/problems/next-greater-numerically-balanced-number/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the smallest number strictly greater than n such that for every digit d that appears in the number, it appears exactly d times. Digits '0' can't appear because if 0 appears it would require 0 occurrences — contradictory. A straightforward check for a given integer x is to count digit frequencies and verify for every present digit d that freq == d.

Two obvious approaches come to mind:
- Brute force: start from n+1 and test each integer until we find a numerically balanced number. The check is cheap (count digits), so if the next balanced number isn't too far, this will be simple and fast.
- Generate all numerically balanced numbers up to some practical length (by selecting digits 1..9 and repeating each digit d exactly d times, then permuting) and then pick the smallest > n. Generation avoids scanning many numbers but requires handling permutations/deduplication; however, because digit-sums must be small when n ≤ 10^6, generation is feasible.

Given constraints (n ≤ 10^6) and that digit-check is O(number of digits) per candidate, brute force is simplest and reliable here.

## Refining the problem, round 2 thoughts
Edge cases:
- Numbers containing '0' are invalid (immediately reject).
- Single-digit numbers: only 1 is valid (1 occurs once). 2 is not valid because 2 occurs once but requires 2 occurrences.
- We must be careful about worst-case performance if the next balanced number is far away. But in practice and given constraints, the gap is small and brute-force is acceptable.
Alternative (generation) would be deterministic and avoid scanning, but is a bit more code and permutations for larger lengths can get heavy. I'll implement the simple brute-force with an efficient digit-count check.

Complexity:
- Let g be the gap between n and the next balanced number. Each candidate we check by converting to string and counting digits => O(log x) per check. So time is O(g * log X). For this problem size, g is small in practice, so this is fine. Space is O(1) extra aside from counters.

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def nextBeautifulNumber(self, n: int) -> int:
        def is_balanced(x: int) -> bool:
            s = str(x)
            cnt = Counter(s)
            # if '0' appears it's invalid because 0 would need 0 occurrences
            if '0' in cnt:
                return False
            # for each digit that appears, its count must equal the digit value
            for ch, c in cnt.items():
                if c != int(ch):
                    return False
            return True

        x = n + 1
        # loop until we find a numerically balanced number
        while True:
            if is_balanced(x):
                return x
            x += 1
```
- Notes:
  - Approach: brute-force incrementing from n+1 and checking the numerically-balanced property by counting digit frequencies.
  - Correctness: The check ensures no '0' digit appears and that every present digit d appears exactly d times.
  - Time complexity: O(g * D) where g is the gap to the next valid number and D is number of digits of current candidate (O(log x)). For given constraints (n ≤ 10^6) this is efficient in practice.
  - Space complexity: O(1) extra (counter size bounded by at most 10).