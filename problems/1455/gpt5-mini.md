# [Problem 1455: Check If a Word Occurs As a Prefix of Any Word in a Sentence](https://leetcode.com/problems/check-if-a-word-occurs-as-a-prefix-of-any-word-in-a-sentence/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check whether searchWord is a prefix of any word in sentence and return the 1-based index of the first such word. The sentence words are separated by single spaces, so splitting the sentence into words is the simplest approach. For each word, check if it starts with searchWord (Python's str.startswith is convenient). Edge cases: searchWord longer than a word should not match; if multiple words match return the earliest (first) index; if none match return -1.

## Refining the problem, round 2 thoughts
Using sentence.split(" ") yields a list of words and then iterate with enumerate starting at 1 to get the 1-based index. Complexity is fine because sentence length ≤ 100, searchWord length ≤ 10. Alternatively, I could scan the sentence character-by-character to avoid extra list allocation, but that's unnecessary given constraints and split keeps the code simple and readable. Confirm behavior on trivial cases: single-word sentence, searchWord equal to the whole word, searchWord equals empty string (not allowed by constraints), and multiple occurrences (return first).

## Attempted solution(s)
```python
class Solution:
    def isPrefixOfWord(self, sentence: str, searchWord: str) -> int:
        # Split by single space as problem guarantees single-space separation
        words = sentence.split(" ")
        for idx, w in enumerate(words, start=1):
            if w.startswith(searchWord):
                return idx
        return -1
```
- Notes:
  - Approach: split the sentence into words and check each word with startswith; return the 1-based index of the first match.
  - Time complexity: O(n * m) in the worst case where n is number of words and m is length of searchWord; more precisely O(L) where L is length of sentence because each character is inspected at most a constant number of times.
  - Space complexity: O(n) for the list of words produced by split (in-place scanning alternative could reduce extra space to O(1), but split is acceptable given constraints).
  - This solution is straightforward, readable, and fits the problem constraints.