# [Problem 1408: String Matching in an Array](https://leetcode.com/problems/string-matching-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks to return words that are substrings of any other word in the array. My first thought is brute force: for each word, check every other word to see if it contains the current word using Python's substring check ("in"). Because words are unique and lengths are small (<= 30) and words.length <= 100, an O(n^2 * L) approach should be fine. I can also prune checks by only testing a word against longer words (a word cannot be a substring of a shorter word, and equal-length distinct words can't be substrings because they are unique).

## Refining the problem, round 2 thoughts
Refinements:
- Use nested loops but skip comparisons when candidate word length >= other word length (unless equal and identical, but uniqueness prevents identical equal-length matches).
- Break early for a word once we find one containing word to avoid unnecessary checks.
- Alternatively, one could concatenate all words with separators and search, or build a trie/ suffix structure, but that's overkill here given constraints.
- Complexity: O(n^2 * L) time in the worst case where L is max word length (substring check is O(L) typically). Space: O(n) for result (excluding input).

Edge cases:
- No substrings -> return empty list.
- Many substrings -> still fine.
- Return order may be any.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def stringMatching(self, words: List[str]) -> List[str]:
        n = len(words)
        res = []
        for i, w in enumerate(words):
            lw = len(w)
            found = False
            for j, t in enumerate(words):
                if i == j:
                    continue
                # Only check if t is longer than w (cannot be substring of shorter or equal unique string)
                if len(t) <= lw:
                    continue
                if w in t:
                    res.append(w)
                    found = True
                    break
            # optional: continue to next word if found (we already break)
        return res
```
- Notes:
  - Approach: Nested loops with pruning by length; for each word w, check if it appears in any strictly longer word t using Python's "in" substring test. Break as soon as a containing word is found.
  - Time complexity: O(n^2 * L) in the worst case, where n = len(words) and L is the maximum word length (because each substring check is O(L) and there are O(n^2) checks before pruning).
  - Space complexity: O(n) worst-case for the output (not counting input), plus O(1) auxiliary.
  - This is simple, clear, and efficient enough given constraints.