# [Problem 884: Uncommon Words from Two Sentences](https://leetcode.com/problems/uncommon-words-from-two-sentences/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find words that appear exactly once in one sentence and do not appear in the other. First idea: split each sentence into words and count occurrences. If a word appears exactly once in s1 and zero times in s2, it's uncommon; likewise for s2. Another quick observation: if you combine both sentences and count all words, then any word that appears exactly once overall must appear exactly once in one sentence and zero times in the other (because if it appeared in both, total would be >=2). So a single combined Counter and selecting items with count == 1 should work. Alternative would be to build two Counters and test counts separately, but combined counting is simpler.

## Refining the problem, round 2 thoughts
Edge cases: repeated words in a single sentence (e.g., "apple apple") should not be considered uncommon. Words that appear once in each sentence should be excluded. Constraints guarantee lowercase letters and single-space separation, so simple split() works. Complexity: splitting and counting is linear in total number of characters/words; space is linear as well to hold counts. Using a single Counter over the concatenation of both word lists is concise and efficient.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def uncommonFromSentences(self, s1: str, s2: str) -> List[str]:
        # Split both sentences into words
        words = s1.split() + s2.split()
        # Count occurrences across both sentences
        cnt = Counter(words)
        # Uncommon words are those that appear exactly once overall
        return [w for w, c in cnt.items() if c == 1]
```
- Notes:
  - Approach: split both sentences into lists of words, combine them, count occurrences with Counter, and return words whose total count is exactly 1.
  - Time complexity: O(n) where n is the total number of words across both sentences (splitting and counting).
  - Space complexity: O(m) for the Counter and resulting list, where m is the number of distinct words.