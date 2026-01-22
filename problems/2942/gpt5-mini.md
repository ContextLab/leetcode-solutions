# [Problem 2942: Find Words Containing Character](https://leetcode.com/problems/find-words-containing-character/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need indices of words that contain a given character x. The simplest approach that comes to mind is to iterate through the list of words with their indices and check membership using Python's "in" operator (e.g., if x in word). That will short-circuit as soon as a match is found in each word. The returned order can be any, so returning indices in increasing order (natural enumerate order) is fine.

## Refining the problem, round 2 thoughts
- Edge cases: no words contain x -> return empty list; words length and list length are small (<=50), so performance is trivial.
- Alternatives: convert each word to a set for O(1) membership checks per word, but converting to a set costs O(m) anyway, and we only need to check each word once, so "x in word" (which is O(m) worst-case) is simpler and efficient enough.
- Complexity: for n words with average length m, time is O(n * m). Space is O(k) for the output where k is number of matching words (plus negligible overhead).
- Implementation detail: use enumerate to collect indices easily.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findWords(self, words: List[str], x: str) -> List[int]:
        result: List[int] = []
        for i, w in enumerate(words):
            if x in w:
                result.append(i)
        return result
```
- Approach: iterate with enumerate and use Python's substring membership operator to test presence of x in each word; append index when true.
- Time complexity: O(n * m), where n = len(words) and m = average length of words[i].
- Space complexity: O(k) for the output list (k = number of words containing x).
- Notes: The solution returns indices in increasing order but any order is allowed per the problem statement. The approach is simple and sufficient given the input size constraints.