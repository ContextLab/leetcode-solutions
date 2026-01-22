# [Problem 3541: Find Most Frequent Vowel and Consonant](https://leetcode.com/problems/find-most-frequent-vowel-and-consonant/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count frequencies of letters in the string, then pick the most frequent vowel and the most frequent consonant and sum their frequencies. The string length is small (<= 100), so any straightforward counting is fine. Use a set for vowels to separate them quickly. collections.Counter is convenient, or a fixed-size array of 26 ints. If a category (vowel or consonant) doesn't appear, its contribution is 0.

## Refining the problem, round 2 thoughts
- Edge cases: string all vowels (consonant max = 0) or all consonants (vowel max = 0). Single letter strings are fine.
- Ties: problem allows choosing any when multiple letters tie for max; we only need the count, not which letter.
- Complexity: one pass to count letters (O(n)), then scanning counts (O(26)=O(1)). Space O(1) aside from input (26 counters).
- Implementation: I'll use collections.Counter for readability. Use a vowel set {'a','e','i','o','u'} and compute vowel_max as max(count[c] for c in vowel_set) but need to ensure letters not present default to 0; with Counter missing keys return 0. For consonants, iterate all lowercase letters excluding vowels.

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def maxFreq(self, s: str) -> int:
        """
        Return sum of the highest-frequency vowel and highest-frequency consonant in s.
        If no vowels or no consonants exist, treat their max frequency as 0.
        """
        vowels = set('aeiou')
        cnt = Counter(s)
        
        # Max frequency among vowels
        vowel_max = 0
        for v in vowels:
            vowel_max = max(vowel_max, cnt[v])
        
        # Max frequency among consonants
        consonant_max = 0
        # iterate all lowercase letters and skip vowels
        for i in range(26):
            ch = chr(ord('a') + i)
            if ch in vowels:
                continue
            consonant_max = max(consonant_max, cnt[ch])
        
        return vowel_max + consonant_max
```
- Notes:
  - Approach: Count frequencies with Counter in one pass. Then find the maximum count among vowels and among consonants separately.
  - Time complexity: O(n) to build the counter plus O(1) (26 iterations) to compute maxima, so overall O(n).
  - Space complexity: O(1) extra (Counter stores up to 26 keys; ignoring input storage), so O(1) auxiliary.
  - Implementation detail: Counter returns 0 for missing keys, so it's safe to query letters that don't appear.