# [Problem 2185: Counting Words With a Given Prefix](https://leetcode.com/problems/counting-words-with-a-given-prefix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[I see an array of words and a prefix string; I need to count how many words start with that prefix. The simplest approach is to iterate through words and check whether each word has pref as its leading substring. Python's str.startswith(pref) directly matches the definition of prefix and handles the case where pref is longer than the word (it returns False). Constraints are small (up to 100 words, each up to length 100), so a straightforward O(n * m) solution (n = number of words, m = length of pref) is fine. I could also slice word[:len(pref)] == pref, or build a trie for many queries, but that's overkill here.]

## Refining the problem, round 2 thoughts
[Edge cases: pref equal to entire word, pref longer than word, all words matching, no words matching. startswith covers these. Complexity: for each word we compare up to len(pref) characters, so O(n * m) time and O(1) extra space (aside from input). Alternative solutions: using slicing or manual character compare yields same complexity. If there were many queries, a trie could be used to preprocess words, but not necessary for this single-pass problem.]

## Attempted solution(s)
```python
from typing import List

class Solution:
    def prefixCount(self, words: List[str], pref: str) -> int:
        # Count how many words have 'pref' as a prefix
        count = 0
        for w in words:
            if w.startswith(pref):
                count += 1
        return count
```
- Notes:
  - Approach: iterate through the list and use str.startswith to check the prefix.
  - Time complexity: O(n * m), where n = len(words) and m = len(pref). Each startswith may compare up to m characters.
  - Space complexity: O(1) extra space (ignoring input and output).