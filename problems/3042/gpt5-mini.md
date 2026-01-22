# [Problem 3042: Count Prefix and Suffix Pairs I](https://leetcode.com/problems/count-prefix-and-suffix-pairs-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks to count index pairs (i, j) with i < j where words[i] is both a prefix and a suffix of words[j]. My first, straightforward thought is to check every pair (i, j) with i < j and test whether words[j] startswith and endswith words[i]. Because words.length <= 50 and each word length <= 10, an O(n^2 * L) approach (where L is max word length) is perfectly fine.

I also note that if words[i] is longer than words[j], it can't be both prefix and suffix, so we can skip those pairs quickly. If words are equal (words[i] == words[j]) that should count as valid because a string is a prefix and suffix of itself, provided i < j.

I briefly considered more fancy data structures (tries, KMP borders, grouping by length), but given the small constraints they add unnecessary complexity.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Ensure we only consider i < j (order matters).
- Skip pairs where len(words[i]) > len(words[j]).
- Strings equal counts as valid (i < j).
- Built-in Python string methods startswith and endswith are appropriate and efficient for small L.
- Time complexity: O(n^2 * L) with n up to 50 and L up to 10 — trivial for limits.
- Space complexity: O(1) additional (besides input).

Alternative: group words by their content/length to avoid some checks, but not necessary here.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def prefixSuffix(self, words: List[str]) -> int:
        """
        Count pairs (i, j) with i < j such that words[i] is both a prefix and a suffix of words[j].
        """
        n = len(words)
        ans = 0
        for i in range(n):
            wi = words[i]
            li = len(wi)
            for j in range(i + 1, n):
                wj = words[j]
                if li <= len(wj) and wj.startswith(wi) and wj.endswith(wi):
                    ans += 1
        return ans

# Example usage:
# sol = Solution()
# print(sol.prefixSuffix(["a","aba","ababa","aa"]))  # -> 4
# print(sol.prefixSuffix(["pa","papa","ma","mama"]))  # -> 2
# print(sol.prefixSuffix(["abab","ab"]))  # -> 0
```
- Approach: Brute-force pair checking using Python's startswith and endswith, skipping pairs where word i is longer than word j.
- Time complexity: O(n^2 * L), where n = len(words) (<=50) and L = max word length (<=10).
- Space complexity: O(1) extra space (ignoring input storage).