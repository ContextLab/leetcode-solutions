# [Problem 3043: Find the Length of the Longest Common Prefix](https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the longest common prefix between any pair (x from arr1, y from arr2). Prefix here means the leftmost digits of the decimal representation. Immediately this suggests converting numbers to strings and comparing prefixes. A naive pairwise comparison of all numbers would be O(n1 * n2 * d) and could be large (n up to 5e4), but note each number has at most 9 digits (since ≤ 1e8), so each number contributes at most 9 prefixes. So it's feasible to gather all prefixes from arr1 and arr2 and check for intersections. Using sets of prefixes is straightforward: build set of all prefixes from arr1 and arr2, intersect them, and take the maximum length among common prefixes. This avoids expensive pairwise work and runs in linear time in number of inputs times digit-length.

## Refining the problem, round 2 thoughts
Edge cases: no common prefix → return 0. Single-digit numbers are fine. Duplicates don't matter since we use sets. Alternative approaches include constructing a trie for arr1 and then matching arr2 numbers down the trie, or checking prefix-sets by length descending to early stop — but building full prefix sets and intersecting is simple and efficient because digit length <= 9. Complexity: time O((n1 + n2) * D) with D ≤ 9 (so practically linear), space O((n1 + n2) * D) for the prefix sets.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        # Collect all prefixes (as strings) from arr1
        prefixes1 = set()
        for x in arr1:
            s = str(x)
            # add all non-empty left prefixes
            for i in range(1, len(s) + 1):
                prefixes1.add(s[:i])

        # Collect all prefixes from arr2
        prefixes2 = set()
        for y in arr2:
            s = str(y)
            for i in range(1, len(s) + 1):
                prefixes2.add(s[:i])

        # Intersection gives common prefixes; return the maximum length
        common = prefixes1 & prefixes2
        if not common:
            return 0
        return max(len(p) for p in common)
```
- Approach notes: Convert numbers to strings and generate all left prefixes for each number. Use sets to store prefixes for arr1 and arr2, then intersect and find the longest length among common prefixes.
- Time complexity: O((n1 + n2) * D) where D is the max number of digits (≤ 9). Practically linear in input size.
- Space complexity: O((n1 + n2) * D) for storing prefix strings (each number contributes up to D prefixes).