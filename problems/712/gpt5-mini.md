# [Problem 712: Minimum ASCII Delete Sum for Two Strings](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This looks like a variant of the Longest Common Subsequence (LCS) problem, but instead of maximizing length we care about ASCII-weighted characters. One way: for any common subsequence, keeping it means deleting all other characters from both strings; the cost is the sum of ASCII values of deleted chars. If I know the ASCII-sum of the largest-weight common subsequence, then the minimal delete cost = total ASCII sum of both strings minus twice that common subsequence sum. So I can reframe as: find the maximum ASCII sum of a common subsequence (a weighted LCS). That suggests a dynamic programming solution similar to LCS, with dp[i][j] representing the maximum ASCII-sum common subsequence using s1[:i] and s2[:j].

A direct alternative is to compute dp representing minimal delete cost for prefixes, but computing max-weight common subsequence and subtracting is cleaner and symmetric.

## Refining the problem, round 2 thoughts
- Use DP with complexity O(m * n) where m = len(s1), n = len(s2). This fits constraints up to 1000 (1e6 operations).
- Memory can be optimized to O(n) using a rolling row because dp[i][j] only depends on dp[i-1][j-1], dp[i-1][j], and dp[i][j-1].
- Edge cases: one string empty -> delete all chars of the other string (sum ASCII of that string). The DP handles this naturally.
- Implementation detail: maintain dp as 1D array of length (n+1). For each i, iterate j from 1..n, keep prev to represent dp[j-1] from previous row.
- Complexity: Time O(mn), Space O(n).

## Attempted solution(s)
```python
class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        m, n = len(s1), len(s2)
        # dp[j] will hold the maximum ASCII-sum of common subsequence
        # for s1[:i] (current row) and s2[:j]. We'll reuse dp for each i.
        dp = [0] * (n + 1)

        for i in range(1, m + 1):
            prev = 0  # this will represent dp[j-1] from the previous row
            si = s1[i - 1]
            si_val = ord(si)
            for j in range(1, n + 1):
                temp = dp[j]  # store dp[j] from previous row before overwriting
                if si == s2[j - 1]:
                    dp[j] = prev + si_val
                else:
                    # max of skipping a char from s1 (dp[j] previous row)
                    # or skipping a char from s2 (dp[j-1] current row)
                    dp[j] = max(dp[j], dp[j - 1])
                prev = temp

        max_common_ascii = dp[n]
        total_ascii = sum(ord(c) for c in s1) + sum(ord(c) for c in s2)
        return total_ascii - 2 * max_common_ascii
```
- Notes:
  - Approach: compute maximum ASCII-sum of a common subsequence using DP (weighted LCS). The minimal deletion cost equals total ASCII sum of both strings minus twice that maximum common-sum.
  - Time complexity: O(m * n), where m = len(s1), n = len(s2).
  - Space complexity: O(n) using a single-row rolling DP array.
  - The implementation uses a classic 1D LCS roll with a `prev` variable to access dp[j-1] from the previous row. This is efficient and straightforward.