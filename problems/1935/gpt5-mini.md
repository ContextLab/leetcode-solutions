# [Problem 1935: Maximum Number of Words You Can Type](https://leetcode.com/problems/maximum-number-of-words-you-can-type/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a sentence (words separated by single spaces) and a set of distinct broken letters. We need to count how many words contain no broken letter. The straightforward approach: split the text into words and for each word check whether any character is in the broken set. Using a set for broken letters gives O(1) membership checks. Another idea is to check set intersection between the word's letters and the broken set — if intersection is empty, the word is typeable. This is an easy linear scan problem over the characters in text.

## Refining the problem, round 2 thoughts
Edge cases: brokenLetters may be empty (then all words are typeable). All words and letters are lowercase so no casing issues. Performance: building the broken set costs O(B) where B <= 26. Splitting the text takes O(T) where T is length of text; checking words by scanning characters or using set intersection still results in overall O(T) time because each character is looked at a constant number of times. Space: O(B) for the broken set plus negligible overhead for split words (which is proportional to number of words but within O(T)). There's no need for more complex data structures. Implementation choices: use set(brokenLetters) and then either all(c not in broken for c in word) or if not (set(word) & broken) — both are clear; the latter may build a set per word (costly if words are long), so scanning characters with early exit is slightly more optimal in practice.

## Attempted solution(s)
```python
class Solution:
    def canBeTypedWords(self, text: str, brokenLetters: str) -> int:
        broken = set(brokenLetters)
        count = 0
        for word in text.split():
            # check if any character in word is broken; early exit if so
            for ch in word:
                if ch in broken:
                    break
            else:
                # executed only if the inner loop did not break (no broken letter found)
                count += 1
        return count
```
- Notes:
  - Approach: split the input text into words, convert brokenLetters to a set for O(1) membership tests, and for each word check characters with early exit on first broken character. If none found, increment result.
  - Time complexity: O(T) where T = len(text). Each character in text is inspected at most once (plus overhead of splitting).
  - Space complexity: O(B) for the broken set, where B = len(brokenLetters) ≤ 26. Additional splitting uses space proportional to the number and length of words (which is bounded by T).