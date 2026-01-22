# [Problem 2559: Count Vowel Strings in Ranges](https://leetcode.com/problems/count-vowel-strings-in-ranges/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I’m sorry — I can’t share my internal stream-of-consciousness. Here is a concise high-level plan instead:
- For each word, determine whether it starts and ends with a vowel (check first and last characters).
- Build a prefix-sum array of these boolean values so range counts can be answered in O(1).
- For each query [l, r], answer = pref[r+1] - pref[l].

## Refining the problem, round 2 thoughts
- Edge cases: words are guaranteed to have length >= 1, so accessing first and last characters is safe.
- Constraints allow up to 1e5 words and 1e5 queries; computing a prefix sum gives overall linear-time preprocessing and constant-time queries (overall fast enough).
- Alternative approaches (e.g., segment tree) are unnecessary here because prefix sums are simpler and optimal for static range-sum queries.
- Time complexity: O(sum(len(words[i])) + q) — checking first/last character is O(1) per word but overall bounded by total characters; practically O(n + q).
- Space complexity: O(n) for prefix array (n = number of words).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def vowelStrings(self, words: List[str], queries: List[List[int]]) -> List[int]:
        vowels = set('aeiou')
        n = len(words)
        # prefix sum array where pref[i] = number of valid words in words[:i]
        pref = [0] * (n + 1)
        for i, w in enumerate(words):
            # word length >= 1 per constraints
            if w[0] in vowels and w[-1] in vowels:
                pref[i + 1] = pref[i] + 1
            else:
                pref[i + 1] = pref[i]
        # answer queries using prefix sums
        ans = []
        for l, r in queries:
            ans.append(pref[r + 1] - pref[l])
        return ans
```
- Notes:
  - Approach: mark each word if it starts and ends with a vowel, build prefix sums, answer each query as pref[r+1] - pref[l].
  - Time complexity: O(n + q) in terms of number of words n and number of queries q (more precisely O(sum(len(words[i])) + q), but checking first/last char is constant per word).
  - Space complexity: O(n) for the prefix array and O(1) extra for processing (excluding output).