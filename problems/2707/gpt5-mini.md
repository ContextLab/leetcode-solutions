# [Problem 2707: Extra Characters in a String](https://leetcode.com/problems/extra-characters-in-a-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share my internal stream-of-consciousness. Instead, here is a concise summary of the approach: This is naturally solved with dynamic programming. Let dp[i] be the minimum number of extra characters in s[i:]. Base dp[n] = 0. For each position i, either treat s[i] as an extra character (1 + dp[i+1]) or, for any dictionary word that matches s starting at i, take dp[i + len(word)]. Take the minimum over these choices.

## Refining the problem, round 2 thoughts
Refinement/clarifications and edge cases (concise):
- s length is up to 50, dictionary sizes are small, so an O(n * total_dict_chars) DP is fine.
- Use bottom-up DP from right to left. Initialize dp with dp[n] = 0 and large values elsewhere.
- For each i, default to deleting the char (1 + dp[i+1]). For each word in dictionary, if s starts with word at i, consider dp[i + len(word)].
- Possible optimization: build a trie to avoid checking all words at each position (not necessary here given constraints).
- Time complexity: O(n * total_dict_chars) where total_dict_chars = sum(len(word) for word in dictionary). Space: O(n).

## Attempted solution(s)
```python
class Solution:
    def minExtraChar(self, s: str, dictionary: list[str]) -> int:
        n = len(s)
        dp = [0] * (n + 1)
        # dp[i] = min extra chars for s[i:]
        # base: dp[n] = 0 (already set)

        for i in range(n - 1, -1, -1):
            # default: treat s[i] as an extra character
            best = 1 + dp[i + 1]
            # try matching any dictionary word at position i
            for word in dictionary:
                L = len(word)
                if i + L <= n and s.startswith(word, i):
                    best = min(best, dp[i + L])
            dp[i] = best

        return dp[0]
```
- Notes on approach: This is a straightforward bottom-up DP. For each index, either skip the current character (counting it as extra) or match any dictionary word that begins at this index and add the cost from the next position after the matched word.
- Time complexity: O(n * total_dict_chars) where total_dict_chars = sum(len(w) for w in dictionary) (because s.startswith(word, i) checks up to len(word) characters). Given n <= 50 and dictionary sizes also small, this is efficient.
- Space complexity: O(n) for the dp array.