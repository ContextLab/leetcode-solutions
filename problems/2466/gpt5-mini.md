# [Problem 2466: Count Ways To Build Good Strings](https://leetcode.com/problems/count-ways-to-build-good-strings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This looks like a counting / dynamic programming problem. We build strings by repeatedly appending a block of zeros of fixed length "zero" or a block of ones of fixed length "one". The number of distinct strings of a given total length L equals the number of sequences of these block-append operations that sum to L (order matters). So it's essentially counting the number of ways to reach lengths between low and high using steps of sizes zero and one — a classic DP/counting paths problem. A bottom-up dp where dp[i] = number of ways to build length i seems natural.

## Refining the problem, round 2 thoughts
- dp[0] = 1 (empty start). For each length i from 1..high, dp[i] = (dp[i-zero] if i >= zero) + (dp[i-one] if i >= one).
- We only need dp up to high, then sum dp[i] for i in [low..high] modulo 1e9+7.
- Time complexity O(high), space O(high). Since high <= 1e5, this is fine.
- Edge cases: zero == one is fine (we'll add the same previous dp twice but with different indices; if indices equal we won't double-count because they refer to different step sizes only when sizes equal they'd be same index but that just corresponds to two different choices? Actually if zero == one then both choices append blocks of different characters but same length — they still produce distinct strings because characters differ, and our recurrence adding both contributions is correct).
- Could optimize space to O(max(zero, one)) by keeping sliding window, but not necessary here.

## Attempted solution(s)
```python
class Solution:
    def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:
        MOD = 10**9 + 7
        dp = [0] * (high + 1)
        dp[0] = 1

        for length in range(1, high + 1):
            ways = 0
            if length >= zero:
                ways += dp[length - zero]
            if length >= one:
                ways += dp[length - one]
            dp[length] = ways % MOD

        result = sum(dp[low:high + 1]) % MOD
        return result
```
- Notes:
  - Approach: bottom-up dynamic programming where dp[i] = number of ways to build a string of length i by appending zero-length or one-length blocks.
  - Time complexity: O(high) — we compute dp for every length up to high.
  - Space complexity: O(high) for the dp array. This can be reduced to O(max(zero, one)) with a rolling buffer if needed.
  - We take all counts modulo 10^9 + 7 as required.