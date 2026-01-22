# [Problem 2914: Minimum Number of Changes to Make Binary String Beautiful](https://leetcode.com/problems/minimum-number-of-changes-to-make-binary-string-beautiful/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The string is beautiful if it can be partitioned into even-length substrings each containing only 0s or only 1s. Even-length blocks of identical characters means each block length is a multiple of 2. That suggests blocks must align with pairs of indices (0,1), (2,3), ... because every block starts at index 0 and has even length, so every block boundary lies between an odd and the next even index. So it seems we can treat the string as n/2 independent pairs; each pair must be either "00" or "11" in any beautiful string. For a mismatched pair "01" or "10" we must flip at least one character in that pair. So minimal changes should be the number of pairs that are not already both equal. Initially I thought maybe we need some DP or to consider merging across pairs, but recognizing boundaries align with pairs simplifies it.

## Refining the problem, round 2 thoughts
Confirming the pair-alignment argument: the first block starts at index 0 and has even length, so it ends at an odd index; next block starts at an even index, and so on. Thus block boundaries always fall between indices 2k+1 and 2k+2, and blocks are integral numbers of these pairs. Therefore making the whole string beautiful reduces to ensuring every pair (2i,2i+1) has identical bits. Each pair's cost is independent: min flips to make it "00" (flip the ones) or "11" (flip the zeros) — which is 0 if both equal, otherwise 1. Edge cases: s length guaranteed even and >=2. So just count mismatched pairs. Time complexity O(n), space O(1).

## Attempted solution(s)
```python
class Solution:
    def minimumChanges(self, s: str) -> int:
        # Count pairs (2i, 2i+1) that are mismatched.
        n = len(s)
        changes = 0
        for i in range(0, n, 2):
            if s[i] != s[i+1]:
                changes += 1
        return changes
```
- Notes:
  - Approach: Treat the string as n/2 independent pairs of adjacent characters. Each pair must become "00" or "11". If a pair is already "00" or "11" cost is 0; if it's "01" or "10" cost is 1. Summing over all pairs gives the minimum changes.
  - Time complexity: O(n) where n = len(s).
  - Space complexity: O(1) additional space.