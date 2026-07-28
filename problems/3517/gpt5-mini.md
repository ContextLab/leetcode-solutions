# [Problem 3517: Smallest Palindromic Rearrangement I](https://leetcode.com/problems/smallest-palindromic-rearrangement-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a string s that is already a palindrome. We may rearrange characters to produce another palindrome and must return the lexicographically smallest possible palindrome permutation.

Because the result must be a palindrome, character counts are constrained: every character count must be even except possibly one character (when |s| is odd). So think in terms of building the first half of the palindrome and mirroring it. The lexicographic order compares from the start, so to minimize the whole palindrome we should place the smallest possible characters as early as allowed. That suggests forming the first half by taking half of each character's count and placing those characters in ascending (a→z) order. If there is a middle character (odd count), it must appear in the center.

So approach: count characters, compute half_count for each letter = count // 2, form first_half by appending letters in ascending order according to half_count, find the odd-count letter if any for middle, then return first_half + mid + reverse(first_half).

## Refining the problem, round 2 thoughts
Edge cases:
- Length 1: trivial, returns s.
- All characters same: works.
- Even length with no odd counts: mid is empty.
- The input is guaranteed palindromic, so there will be at most one odd count; no need to validate feasibility.

Complexity: counting characters is O(n). Building result also O(n). Space is O(26) for counts plus O(n) for result.

Alternate solutions: you could greedily choose characters for the first half character-by-character (same effect), but constructing half by sorting counts is simpler and optimal.

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        # Count frequencies
        cnt = Counter(s)
        # Build first half by taking half of each count in ascending letter order
        first_half_parts = []
        mid = ''
        for c in map(chr, range(ord('a'), ord('z') + 1)):
            if cnt[c] % 2 == 1:
                mid = c  # at most one odd is guaranteed
            half = cnt[c] // 2
            if half:
                first_half_parts.append(c * half)
        first_half = ''.join(first_half_parts)
        return first_half + mid + first_half[::-1]
```
- Notes:
  - The algorithm counts characters (O(n)), computes how many of each go into the first half (half of each frequency), and places them in ascending order to ensure the lexicographically smallest prefix.
  - The middle character (if any) is the one with odd count; since s is guaranteed palindromic, there is at most one such character.
  - Time complexity: O(n) where n = len(s). Space complexity: O(n) for the output (plus O(1) extra for counters of fixed alphabet size).