# [Problem 3043: Find the Length of the Longest Common Prefix](https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the longest common prefix (by digits) between any x in arr1 and any y in arr2. A prefix of an integer is simply its leftmost k digits. So if I convert numbers to strings, a prefix is s[:k]. The maximum number of digits for inputs up to 1e8 is small (<= 9), so it's feasible to check every possible prefix length k (1..max_digits) and see if any prefix appears in both arrays. I should handle the fact that a number shorter than k can't contribute a k-length prefix. A straightforward way: convert all numbers to strings, iterate k descending from max_len to 1 and check intersection of prefix sets for arr1 and arr2 — return first k with non-empty intersection. If none, return 0.

## Refining the problem, round 2 thoughts
- Converting each number to string once and reusing avoids repeated conversions.
- Because max digits <= 9, complexity is linear in array sizes times a small constant (max digits).
- Iterate k from the largest possible downwards so we can return immediately on the first match (gives the maximum k).
- Edge cases: numbers shorter than k must be skipped for that k. If either array has no numbers long enough for k, skip quickly.
- Alternative: build all prefixes for one array and check against the other; or do binary search for k, but unnecessary because max digits small.
- Memory: storing string forms and temporary prefix sets is fine for n up to 5e4.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        # Convert numbers to strings once
        s1 = [str(x) for x in arr1]
        s2 = [str(x) for x in arr2]
        # Determine maximum possible prefix length
        max_len = 0
        if s1:
            max_len = max(max_len, max(len(x) for x in s1))
        if s2:
            max_len = max(max_len, max(len(x) for x in s2))
        # Check from longest possible prefix down to 1
        for k in range(max_len, 0, -1):
            prefs1 = {x[:k] for x in s1 if len(x) >= k}
            if not prefs1:
                continue
            # Build prefixes for s2 and check intersection on the fly for early exit
            for x in s2:
                if len(x) >= k and x[:k] in prefs1:
                    return k
        return 0
```
- Approach: convert arrays to string lists, iterate k from max possible digits down to 1, build prefix set for arr1 for length k, then check if any arr2 element has that prefix. Return the first (largest) k found.
- Time complexity: O((n1 + n2) * D) where n1 = len(arr1), n2 = len(arr2), D = max digits (<= 9). Converting to strings is O(n * D) as well.
- Space complexity: O(n1 + n2) for storing string forms, plus O(n1) temporary for prefix sets in worst case.