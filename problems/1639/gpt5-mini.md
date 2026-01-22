# [Problem 1639: Number of Ways to Form a Target String Given a Dictionary](https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count ways to form target by selecting characters from columns of words such that chosen column indices strictly increase. All words have same length m, and there are n words. For each column k we can pick any word's character at that column; using that column consumes that column and all earlier columns for future picks (so picks must use strictly increasing columns). This suggests a DP across columns: at each column, we can either use it to match the next character in target (many choices depending on how many words have that character in this column) or skip it. The conventional trick is to precompute counts of each letter at every column and maintain dp[p] = number of ways to form first p characters of target using processed columns. When processing a new column, we update dp from right to left: dp[p] += dp[p-1] * count[column][target[p-1]].

## Refining the problem, round 2 thoughts
- Precompute counts per column: counts[k][ch].
- dp length is len(target)+1 with dp[0] = 1 (empty prefix).
- For column i, update dp[j] for j from min(i+1, tlen) down to 1 to avoid using updated values within same column.
- If target length > number of columns, answer is 0.
- Complexity: building counts is O(n * m). DP is O(m * tlen). Space: O(m*26 + tlen).
- Modulo 1e9+7.
- Edge cases: many zeros for counts; we can skip updates when count is zero (simple if-check).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numWays(self, words: List[str], target: str) -> int:
        MOD = 10**9 + 7
        n = len(words)
        m = len(words[0])
        tlen = len(target)
        if tlen > m:
            return 0

        # counts[i][c] = number of words with char c at column i
        counts = [[0] * 26 for _ in range(m)]
        for w in words:
            for i, ch in enumerate(w):
                counts[i][ord(ch) - 97] += 1

        dp = [0] * (tlen + 1)
        dp[0] = 1  # one way to form empty prefix

        for i in range(m):  # for each column
            cnts = counts[i]
            # we can form at most i+1 characters using first i+1 columns
            upper = min(tlen, i + 1)
            # update dp from right to left to avoid overwriting dp[j-1] used in same iteration
            for j in range(upper, 0, -1):
                cidx = ord(target[j-1]) - 97
                cnt = cnts[cidx]
                if cnt:
                    dp[j] = (dp[j] + dp[j-1] * cnt) % MOD

        return dp[tlen]
```
- Approach: Precompute letter counts per column, use 1D DP where dp[j] = ways to form first j characters of target using processed columns. For each column, we potentially extend dp[j-1] to dp[j] by choosing any word that has the required letter at this column.
- Time complexity: O(n * m + m * tlen). (n words of length m to build counts; for each of m columns we loop up to tlen positions).
- Space complexity: O(m * 26 + tlen) => O(m + tlen) effectively.
- Important detail: update dp in reverse (right-to-left) so each column's choices are applied only once per column and don't cascade within the same column. Returning dp[tlen] modulo 1e9+7.