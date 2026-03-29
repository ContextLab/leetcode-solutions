# [Problem 2839: Check if Strings Can be Made Equal With Operations I](https://leetcode.com/problems/check-if-strings-can-be-made-equal-with-operations-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The allowed operation is to choose indices i and j with j - i = 2 and swap characters. For a length-4 string the only swaps possible are 0<->2 and 1<->3. That means characters at even indices (0 and 2) can be permuted among themselves, and characters at odd indices (1 and 3) can be permuted among themselves. So to transform s1 into s2, the multiset of characters in s1 at even positions must match the multiset of characters in s2 at even positions, and likewise for odd positions. Duplicates matter, so we should compare multisets (or sorted lists / counters) rather than sets.

## Refining the problem, round 2 thoughts
Because each parity group has exactly two positions, comparing the sorted two-character lists for even and odd indices is simple and sufficient. Edge cases: repeated characters are handled by comparing counts (sorting does that implicitly). Time and space are constant because strings are fixed length 4; in general the approach is O(n) for length-n strings partitioned by parity. Implementation can be concise: compare sorted([s1[0], s1[2]]) == sorted([s2[0], s2[2]]) and same for odd indices.

## Attempted solution(s)
```python
class Solution:
    def checkStrings(self, s1: str, s2: str) -> bool:
        # Compare multiset of characters at even positions (0,2)
        if sorted([s1[0], s1[2]]) != sorted([s2[0], s2[2]]):
            return False
        # Compare multiset of characters at odd positions (1,3)
        if sorted([s1[1], s1[3]]) != sorted([s2[1], s2[3]]):
            return False
        return True
```
- Notes:
  - Approach: Characters at even indices can only move among even indices, and likewise for odd indices. Thus compare multisets (sorted lists) of even-position characters and odd-position characters between s1 and s2.
  - Time complexity: O(1) for the given fixed length 4 (or O(n) for general length n if extended), because we perform a constant amount of work; sorting tiny lists of size 2 is constant.
  - Space complexity: O(1) extra space (a few temporary lists of constant size).