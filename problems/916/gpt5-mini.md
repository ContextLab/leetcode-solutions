# [Problem 916: Word Subsets](https://leetcode.com/problems/word-subsets/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to find which words in words1 are "universal" with respect to all words in words2. The subset definition includes multiplicity, so if words2 contains "abb" then a candidate word in words1 must have at least two 'b's and one 'a'. For multiple strings in words2, the requirement for each letter is the maximum multiplicity required by any single string in words2. So compute a required frequency vector (26 letters) which is the elementwise maximum of frequency vectors of words2. Then for each word in words1, compute its frequency vector and check if it meets or exceeds the required vector for all letters. Using fixed-size arrays of length 26 (instead of Counters) is fast and simple.

## Refining the problem, round 2 thoughts
- Compute max-required counts from words2 only once: required[c] = max over b in words2 of count_b[c].
- For each word a in words1, compute counts and check required <= counts.
- Edge cases: if words2 is empty (constraints say >=1 so not needed but code handles it), every word in words1 is universal. All strings are lowercase and length <= 10, so counting is cheap.
- Complexity: Let n1 = len(words1), n2 = len(words2), L1 avg length of words1 strings, L2 avg length of words2 strings. Time O(n2*L2 + n1*L1 + 26*(n1+n2)) which is essentially linear in total input size. Space O(26) extra besides output.
- Alternative: use collections.Counter and take max via elementwise max, but list-of-26 is faster and simpler.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
        # Helper to count letters into a length-26 list
        def count_letters(word: str) -> List[int]:
            cnt = [0] * 26
            for ch in word:
                cnt[ord(ch) - 97] += 1
            return cnt

        # Build required max frequency from words2
        required = [0] * 26
        for b in words2:
            cb = count_letters(b)
            for i in range(26):
                if cb[i] > required[i]:
                    required[i] = cb[i]

        # For each word in words1, check if it satisfies required counts
        result = []
        for a in words1:
            ca = count_letters(a)
            ok = True
            for i in range(26):
                if ca[i] < required[i]:
                    ok = False
                    break
            if ok:
                result.append(a)
        return result
```
- Notes:
  - Approach: compute maximum required frequency per character from words2, then filter words1 by checking if each word's character counts meet those maxima.
  - Time complexity: O(sum(len(b) for b in words2) + sum(len(a) for a in words1) + 26*(len(words1)+len(words2))) which simplifies to O(total number of characters) and is effectively linear.
  - Space complexity: O(1) extra (26-length arrays) plus output list.