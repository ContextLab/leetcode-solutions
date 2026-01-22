# [Problem 2131: Longest Palindrome by Concatenating Two Letter Words](https://leetcode.com/problems/longest-palindrome-by-concatenating-two-letter-words/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have only two-letter words. To build a palindrome by concatenation of these words, any non-palindromic word (like "ab") must be paired with its reverse ("ba") so that one goes on the left and the other on the right. Each such pair contributes 4 characters (2 + 2). For words that are already palindromic (like "gg"), they can be placed symmetrically in pairs (two "gg" give 4 chars) and at most one single palindromic word can be placed in the middle to add 2 characters. So the plan: count frequencies, match non-palindromic words with their reverse greedily (use min count), handle palindromic words by using floor(count/2) pairs and possibly one leftover center if any palindromic count is odd.

## Refining the problem, round 2 thoughts
Need to avoid double-counting reverse pairs when iterating. Two simple ways: keep a visited set or only process a pair when word < reverse (lexicographic) to process each unordered pair once. Only palindromic words (both letters same) can serve as a center, so track if any palindromic word has an odd count. Complexity should be linear in number of words (effectively O(n)), but note there are at most 26*26 = 676 distinct two-letter words so overhead is small. Edge cases: no possible pairs -> return 0; multiple palindromic words with odd counts -> still only one can be center (add 2 once).

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def longestPalindrome(self, words: List[str]) -> int:
        cnt = Counter(words)
        result = 0
        center_available = False

        for w, c in cnt.items():
            rev = w[::-1]
            if w == rev:
                # use pairs of palindromic words
                pairs = c // 2
                result += pairs * 4
                if c % 2 == 1:
                    center_available = True
            else:
                # only process each non-palindromic unordered pair once
                if w < rev:
                    result += 4 * min(c, cnt.get(rev, 0))

        if center_available:
            result += 2

        return result
```
- Notes:
  - Approach: Count frequencies, pair each word with its reverse for non-palindromic words, pair palindromic words among themselves, and optionally place one leftover palindromic word in the center.
  - Time complexity: O(n) to build the counter + O(k) to iterate keys (k <= min(n, 676)), so overall O(n). Space complexity: O(k) for the counter (at most 676 distinct words).
  - Implementation detail: Using the lexicographic check (w < rev) avoids double-counting reverse pairs. Only palindromic words (like "aa") can be used as the single center element.