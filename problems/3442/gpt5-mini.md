# [Problem 3442: Maximum Difference Between Even and Odd Frequency I](https://leetcode.com/problems/maximum-difference-between-even-and-odd-frequency-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the maximum difference freq(a1) - freq(a2) where a1 has odd frequency and a2 has even frequency. The simplest way is to count frequencies of each letter. Once I have frequencies, I can separate characters into those with odd counts and those with even counts. To maximize x - y, for a chosen odd count x I should pick the smallest even count y. So candidate answer is max(odd_counts) - min(even_counts). Need to be careful about whether characters with zero frequency count as even — the examples imply we must consider only characters that appear in the string (since otherwise choosing y=0 would always give larger answers). The constraints guarantee at least one odd and one even frequency character exist (presumably with positive counts), so we don't need special handling for a missing category.

## Refining the problem, round 2 thoughts
- Confirm: only consider characters with positive frequency. Characters not present (freq 0) should not be used for a2, because the sample would otherwise pick 0 and give larger answers.
- Implementation: use collections.Counter or a fixed-size array of length 26 to count letters.
- Extract odd_counts = [cnt for cnt in counts if cnt % 2 == 1] and even_counts = [cnt for cnt in counts if cnt % 2 == 0 and cnt > 0].
- Answer = max(odd_counts) - min(even_counts).
- Time complexity: O(n + 26) -> O(n). Space: O(1) extra (26-size arrays).
- Edge cases: string length small but constraint n >= 3; at least one odd and one even present by problem guarantee.

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def maxDiff(self, s: str) -> int:
        # Count frequencies of characters in s
        freq = Counter(s)
        
        # Collect positive even frequencies and odd frequencies
        odd_counts = []
        even_counts = []
        for cnt in freq.values():
            if cnt % 2 == 1:
                odd_counts.append(cnt)
            else:
                # cnt is even; only consider characters that appear (cnt > 0)
                even_counts.append(cnt)
        
        # Problem guarantees at least one odd and one even frequency character exists.
        # Compute maximum difference: choose largest odd and smallest even.
        return max(odd_counts) - min(even_counts)
```
- Notes:
  - Approach: count letters, separate odd and even positive frequencies, then compute max(odd) - min(even).
  - Time complexity: O(n) to count frequencies (n = len(s)), plus O(26) to scan counts => O(n).
  - Space complexity: O(1) extra (Counter holds up to 26 entries, lists of counts up to 26).
  - Important detail: do not include characters with zero frequency (not in Counter) — choosing zero would incorrectly inflate the result. The problem statement and examples imply only present characters should be considered, and constraints guarantee at least one odd and one even present.