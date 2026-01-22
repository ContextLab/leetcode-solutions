# [Problem 1684: Count the Number of Consistent Strings](https://leetcode.com/problems/count-the-number-of-consistent-strings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count words whose characters all appear in the string allowed. The allowed string has distinct lowercase letters. The straightforward way is to make a set of allowed characters and for each word check every character membership; if any character is not in the allowed set the word is inconsistent. Since words are short (length <= 10) and words count <= 10^4, checking each character is cheap. Another approach is to convert each word to a set and check subset relationship (set(word) <= allowed_set) or use bitmasks for constant-space faster checks. But the simple set membership per character should be clean and fast enough.

## Refining the problem, round 2 thoughts
Edge cases:
- allowed contains all letters -> all words consistent.
- allowed contains a single letter -> only words composed of that letter count.
- words with repeated letters should still be fine as long as each unique char is allowed.

Complexity:
- Building allowed set: O(|allowed|) up to 26.
- For each word, checking characters: O(len(word)). Total O(sum of lengths of words) which is <= 10^4 * 10 = 10^5, very small.
Space:
- O(1) extra for allowed set (<=26). If using set(word) temporarily that's at most 26 but unnecessary.

Alternative:
- Use bitmask for allowed and word: faster bit operations but not necessary here.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        allowed_set = set(allowed)
        count = 0
        for w in words:
            # if all characters in w are in allowed_set, increment
            valid = True
            for ch in w:
                if ch not in allowed_set:
                    valid = False
                    break
            if valid:
                count += 1
        return count
```
- Notes:
  - Approach: build a set of allowed characters for O(1) membership checks, then iterate through each word and its characters to verify consistency.
  - Time complexity: O(A + S) where A = len(allowed) (<=26) and S = sum(len(word) for word in words). Given constraints S <= 10^5, this is efficient.
  - Space complexity: O(1) extra (allowed_set of up to 26 characters), not counting input.
  - Implementation detail: early break on first disallowed character to avoid unnecessary checks. An alternative succinct implementation is `if set(w) <= allowed_set: count += 1`, but that constructs a set for each word; the per-character check is slightly more direct and avoids extra set allocations.