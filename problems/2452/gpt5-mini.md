# [Problem 2452: Words Within Two Edits of Dictionary](https://leetcode.com/problems/words-within-two-edits-of-dictionary/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given queries and dictionary strings all of the same length. An edit means changing any single letter to any other letter; we can perform up to two edits. That is exactly the Hamming distance between two equal-length strings: the number of positions where they differ. So for each query we need to check if there exists any dictionary word whose Hamming distance to the query is <= 2.

Brute force: for each query, compare to each dictionary word and count differing positions. If any comparison has <= 2 differences, include the query. Input sizes are small (<= 100 each, length <= 100), so O(Q * D * n) is fine. We can stop counting as soon as mismatches exceed 2 to save work.

Could also generate all variants of a query within two edits and check membership in dictionary set, or precompute patterns for dictionary, but that's unnecessary because brute force is simple, clear, and efficient given constraints.

## Refining the problem, round 2 thoughts
Edge cases:
- Exact matches (0 edits) should pass.
- Strings of length 1 or 2 — same logic applies.
- Make sure to break early when mismatch count exceeds 2 to avoid wasted work.
- Complexity: Q and D up to 100, n up to 100 => worst-case character comparisons ~1e6, trivial.

Alternative approaches:
- Precompute wildcards for dictionary words by masking up to two positions and store in a set, then check queries by generating the same masks. That reduces per-query checks but increases code complexity and memory. Not needed here.

I'll implement a helper that checks if two strings differ in at most two positions with early exit, then run nested loops and collect queries that match any dictionary word.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def twoEditWords(self, queries: List[str], dictionary: List[str]) -> List[str]:
        def differ_at_most_two(a: str, b: str) -> bool:
            # Count mismatches with early exit if > 2
            mismatches = 0
            for ca, cb in zip(a, b):
                if ca != cb:
                    mismatches += 1
                    if mismatches > 2:
                        return False
            return True

        res = []
        for q in queries:
            for d in dictionary:
                if differ_at_most_two(q, d):
                    res.append(q)
                    break
        return res
```
- Notes about the solution:
  - Approach: For each query, compare it to each dictionary word and count position-wise differences (Hamming distance). If any dictionary word has Hamming distance <= 2, the query is added to the result.
  - Time complexity: O(Q * D * n) where Q = len(queries), D = len(dictionary), n = length of words. Given constraints (<= 100 each), this is efficient.
  - Space complexity: O(1) extra space beyond the output list (ignoring input/output storage).