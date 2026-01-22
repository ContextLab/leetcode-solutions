# [Problem 1400: Construct K Palindrome Strings](https://leetcode.com/problems/construct-k-palindrome-strings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to split all characters of s into exactly k non-empty palindrome strings. For a palindrome string, characters mostly come in pairs; at most one character in each palindrome can have an odd count (the center). So the number of palindromes we can form is at least the number of characters with odd counts (each odd must be placed as a center somewhere). Also every palindrome must be non-empty, so k cannot exceed len(s). That suggests the two necessary conditions: k <= len(s) and number_of_odd_counts <= k. I should check if those are sufficient as well — intuitively they are because pairs can be redistributed to fill up remaining palindromes without breaking palindromicity.

## Refining the problem, round 2 thoughts
- Compute frequency counts of letters; count how many characters have odd frequency (odd_count).
- If odd_count > k: impossible because each palindrome can only absorb one odd center.
- If k > len(s): impossible because each palindrome must be non-empty.
- If odd_count <= k <= len(s): we can always construct k palindromes. Reason: use each odd-count character as center for odd_count palindromes; for remaining k - odd_count palindromes, we can split pairs from the pooled even counts (or break a pair into two singles? actually we can distribute pairs to create additional palindromes of odd length by giving them a single center drawn from splitting pairs) — known constructive argument on this problem. Complexity: counting is O(n), space O(1) (26 letters) or O(26) ~ O(1).

Edge cases: s length 1, k = 1; k equal to n; all characters same; k = 0 not allowed by constraints (k >= 1).

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def canConstruct(self, s: str, k: int) -> bool:
        n = len(s)
        if k > n:
            return False
        freq = Counter(s)
        odd_count = sum(1 for v in freq.values() if v % 2 == 1)
        return odd_count <= k
```
- Notes:
  - Approach: Count character frequencies, compute number of odd frequencies. Return True iff odd_count <= k <= len(s).
  - Time complexity: O(n), where n = len(s), to build the counter and compute odd counts.
  - Space complexity: O(1) extra (counts for at most 26 lowercase letters, or O(26) which is constant).