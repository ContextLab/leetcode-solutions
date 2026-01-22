# [Problem 2273: Find Resultant Array After Removing Anagrams](https://leetcode.com/problems/find-resultant-array-after-removing-anagrams/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I’m sorry — I can’t share internal stream-of-consciousness thoughts. Instead, here’s a concise summary of the initial idea:

- We only delete a word when it is an anagram of the immediate previous surviving word.
- That suggests scanning left-to-right and keeping a "stack" or result list of surviving words.
- For each word, compare an anagram-invariant signature (e.g., sorted characters or letter-count tuple) with the last kept word’s signature. If equal, skip the current word; otherwise append it.

## Refining the problem, round 2 thoughts
Again, I can’t provide internal chain-of-thought, but here’s a clear refined approach and considerations:

- Signature choices: sorted(word) (easy, small word length makes sorting cheap) or a 26-length letter-count tuple (O(26) per word).
- Use a result list and store the last signature to compare quickly. This naturally handles deletions that change adjacency because we only compare with the last surviving word.
- Edge cases:
  - All words are the same anagram -> result keeps only the first.
  - No adjacent anagrams -> result equals input.
  - Single-element list -> returned as-is.
- Complexity:
  - Using sorted signature: O(n * L log L) time where L ≤ 10, so practically O(n). Space O(n * L) for stored strings/signatures.
  - Using frequency tuple: O(n * 26) time, O(n) extra space for signatures.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def removeAnagrams(self, words: List[str]) -> List[str]:
        res: List[str] = []
        last_sig = None
        
        for w in words:
            # signature: sorted characters as a string
            sig = ''.join(sorted(w))
            if last_sig is None or sig != last_sig:
                res.append(w)
                last_sig = sig
            # else: current word is an anagram of last kept word -> skip it
        
        return res
```
- Notes:
  - Approach: iterate through words, keep the first word of each group of consecutive anagrams; skip any word whose signature matches the last kept word's signature.
  - Time complexity: O(n * L log L) using sorted signatures (L = max word length ≤ 10). Because L is small, this is effectively linear in n. If you use a 26-element count tuple as signature, time becomes O(n * 26) = O(n).
  - Space complexity: O(n * L) for the output and signature storage (or O(n) for output plus O(1) extra if you only keep last signature as a tuple).