# [Problem 3121: Count the Number of Special Characters II](https://leetcode.com/problems/count-the-number-of-special-characters-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count letters that appear both lowercase and uppercase, and all lowercase occurrences must appear before the first uppercase occurrence. That suggests tracking positions of lower and upper occurrences per letter. One straightforward idea: for each letter a..z, record the last index of any lowercase occurrence and the first index of any uppercase occurrence. If both exist and last_lower < first_upper, that letter is "special". Another approach is a single left-to-right pass maintaining per-letter state (seen lowercase, seen uppercase, invalid if lowercase appears after uppercase). Both are O(n) and low-memory (26 letters). I'll go with the index-recording method because it's simple and easy to reason about.

## Refining the problem, round 2 thoughts
Edge cases: letters that appear only lowercase or only uppercase shouldn't be counted. If a letter's uppercase appears before any lowercase, it can't be special. If any lowercase appears after the first uppercase, it disqualifies the letter — using last lowercase index and first uppercase index covers that. Complexity should be O(n) time and O(1) (26) space. Implementation detail: initialize first_upper to a large sentinel (e.g., n+1) and last_lower to -1. After scanning, count letters satisfying the condition.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countSpecialCharacters(self, word: str) -> int:
        n = len(word)
        INF = n + 1
        # first_upper[i] = index of first uppercase for letter chr(i + ord('a')), or INF if none
        first_upper: List[int] = [INF] * 26
        # last_lower[i] = index of last lowercase for letter chr(i + ord('a')), or -1 if none
        last_lower: List[int] = [-1] * 26

        for i, ch in enumerate(word):
            if 'a' <= ch <= 'z':
                idx = ord(ch) - ord('a')
                last_lower[idx] = i
            else:
                idx = ord(ch.lower()) - ord('a')
                # record the first uppercase index (keep the minimum seen)
                if first_upper[idx] == INF:
                    first_upper[idx] = i

        ans = 0
        for i in range(26):
            if last_lower[i] != -1 and first_upper[i] != INF and last_lower[i] < first_upper[i]:
                ans += 1

        return ans
```
- Notes:
  - Approach: Single pass to record last lowercase index and first uppercase index for each of the 26 letters, then count letters satisfying last_lower < first_upper (and both present).
  - Time complexity: O(n) where n = len(word), since we scan the string once and then loop 26 letters.
  - Space complexity: O(1) (26-size arrays) in addition to input storage.
  - This handles edge cases: letters missing in either case are ignored; any lowercase after the first uppercase yields last_lower >= first_upper and thus disqualifies the letter.