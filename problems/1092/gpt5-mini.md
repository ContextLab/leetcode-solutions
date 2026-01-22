# [Problem 1092: Shortest Common Supersequence ](https://leetcode.com/problems/shortest-common-supersequence/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I know the shortest common supersequence (SCS) problem is closely related to the longest common subsequence (LCS). If we find the LCS of str1 and str2, we can "merge" the two strings around the LCS characters to form an SCS. The SCS length equals len(str1) + len(str2) - len(LCS). So computing the LCS (classic DP) seems like the first step. After obtaining the LCS string, I can walk both inputs and interleave the non-LCS characters and the LCS characters to produce a valid shortest supersequence. Edge cases: when the LCS is empty (then SCS is simply concatenation), or when strings are identical (SCS is either string). Time complexity will be dominated by the LCS DP O(m*n) for lengths up to 1000, which is acceptable.

## Refining the problem, round 2 thoughts
Refinement: implement a DP table dp[i][j] = length of LCS of str1[:i] and str2[:j]. After filling dp, backtrack to build the actual LCS string (reversing as needed). Then produce the SCS by iterating through the LCS and appending characters from str1 and str2 up to each LCS character, then appending that LCS character, continuing until both strings are exhausted. This produces a shortest supersequence. Complexity: O(m*n) time and O(m*n) space for the DP table. Memory could be reduced if only LCS length were needed, but to reconstruct the LCS we either need the full table or a more complex approach; full table is simpler and fine for constraints.

Edge cases to watch:
- Ties in backtracking for LCS: choosing either direction yields a valid LCS (maybe different), any is fine.
- When one string is completely consumed while merging with LCS, append the remainder of the other string.

## Attempted solution(s)
```python
class Solution:
    def shortestCommonSupersequence(self, str1: str, str2: str) -> str:
        m, n = len(str1), len(str2)
        # dp[i][j] = length of LCS of str1[:i] and str2[:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            a = str1[i - 1]
            row = dp[i]
            prev_row = dp[i - 1]
            for j in range(1, n + 1):
                if a == str2[j - 1]:
                    row[j] = prev_row[j - 1] + 1
                else:
                    # take the max of skipping one char from either string
                    if prev_row[j] >= row[j - 1]:
                        row[j] = prev_row[j]
                    else:
                        row[j] = row[j - 1]

        # Backtrack to build the LCS string
        i, j = m, n
        lcs_chars = []
        while i > 0 and j > 0:
            if str1[i - 1] == str2[j - 1]:
                lcs_chars.append(str1[i - 1])
                i -= 1
                j -= 1
            else:
                if dp[i - 1][j] >= dp[i][j - 1]:
                    i -= 1
                else:
                    j -= 1
        lcs_chars.reverse()
        lcs = "".join(lcs_chars)

        # Merge str1 and str2 around the LCS to build the SCS
        res = []
        i = j = 0
        for c in lcs:
            # append non-LCS characters from str1 up to c
            while i < m and str1[i] != c:
                res.append(str1[i])
                i += 1
            # append non-LCS characters from str2 up to c
            while j < n and str2[j] != c:
                res.append(str2[j])
                j += 1
            # append the common LCS character and advance both pointers
            res.append(c)
            i += 1
            j += 1

        # append remaining tails
        if i < m:
            res.append(str1[i:])
        if j < n:
            res.append(str2[j:])

        return "".join(res)
```
- Notes:
  - Approach: compute LCS via dynamic programming, backtrack to form the LCS string, then merge str1 and str2 using the LCS as a guide to produce a shortest common supersequence.
  - Time complexity: O(m * n) where m = len(str1), n = len(str2) due to the DP fill and the backtracking/merge steps which are O(m + n).
  - Space complexity: O(m * n) for the DP table. Additional space for the resulting string and LCS is O(m + n).