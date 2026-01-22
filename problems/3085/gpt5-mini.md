# [Problem 3085: Minimum Deletions to Make String K-Special](https://leetcode.com/problems/minimum-deletions-to-make-string-k-special/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to make the string "k-special" so that for any two characters present in the final string, their frequencies differ by at most k. I can only delete characters. That suggests choosing a frequency interval [a, b] with b - a ≤ k such that every character I keep has final frequency within that interval. For a given interval, any character with original freq < a must be deleted entirely (can't increase), and any character with original freq > b can be reduced to b by deleting extra occurrences. Characters with freq in [a, b] can be kept as-is. So for each possible a (and b = a + k) I can compute how many characters remain, and deletions = total length - kept. Try all reasonable a to maximize kept (minimize deletions). There are at most 26 different letters so per a work is constant; a ranges up to max frequency (≤ n), so overall fine.

## Refining the problem, round 2 thoughts
- Only letters that remain (positive frequency) are considered in the k-special property, so deleting a letter entirely is allowed and useful.
- We only need to try integer lower bounds a from 1 to max_freq (no need for a = 0).
- For each a, b = a + k. For each letter with freq f:
  - if f < a: contribute 0 (delete all)
  - else contribute min(f, b) (keep up to b)
- Maximize total kept; answer = n - max_kept.
- Complexity: O(n + 26 * max_freq) ~ O(n) since max_freq ≤ n and 26 factor is constant. Space O(1) extra (26 counters).

## Attempted solution(s)
```python
from typing import List
import collections

class Solution:
    def minDeletions(self, word: str, k: int) -> int:
        # Count frequencies of each lowercase letter
        cnt = [0] * 26
        for ch in word:
            cnt[ord(ch) - ord('a')] += 1
        n = len(word)
        max_freq = max(cnt)  # 0 if empty, but word length >=1 by constraints
        
        max_kept = 0
        # Try all possible minimum frequencies a for kept letters (a >= 1)
        for a in range(1, max_freq + 1):
            b = a + k
            kept = 0
            for f in cnt:
                if f >= a:
                    kept += min(f, b)
            if kept > max_kept:
                max_kept = kept
        
        return n - max_kept
```
- Notes:
  - Approach: iterate possible lower bound a of frequency for kept letters, set upper bound b = a + k, compute how many characters can remain (letters with f < a are deleted, letters with f > b are reduced to b).
  - Time complexity: O(n + 26 * max_freq) → effectively O(n) since max_freq ≤ n and 26 is constant.
  - Space complexity: O(1) extra (array of size 26).