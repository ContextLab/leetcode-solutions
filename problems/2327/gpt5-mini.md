# [Problem 2327: Number of People Aware of a Secret](https://leetcode.com/problems/number-of-people-aware-of-a-secret/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share internal stream-of-consciousness. I can, however, give a concise high-level summary of the approach:
- Model how many people learn the secret on each day (dp[i]).
- For a given day i, those who can share are people who learned the secret earlier and are in their sharing window [learn_day + delay, learn_day + forget - 1].
- Use prefix sums to compute dp[i] quickly from previous dp values.

## Refining the problem, round 2 thoughts
- Let dp[i] be the number of people who learn the secret on day i. dp[1] = 1.
- For day i > 1, contributors are days j such that j + delay <= i <= j + forget - 1. This gives j in [i - forget + 1, i - delay].
- dp[i] = sum(dp[j]) over that j-range (if valid). Compute efficiently with prefix sums to avoid O(n^2).
- The final answer is the number of people who still remember the secret at the end of day n: sum(dp[j]) for j in [n - forget + 1, n].
- Time complexity: O(n). Space: O(n) (can be optimized to O(1) with a rolling window, but O(n) is straightforward and within constraints).

## Attempted solution(s)
```python
class Solution:
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        MOD = 10**9 + 7
        dp = [0] * (n + 1)  # dp[i] = people who learn on day i
        pref = [0] * (n + 1)  # prefix sums of dp: pref[i] = sum(dp[1..i])
        dp[1] = 1
        pref[1] = 1

        for i in range(2, n + 1):
            # j range: [i - forget + 1, i - delay]
            left = i - forget + 1
            if left < 1:
                left = 1
            right = i - delay
            if right >= left:
                dp[i] = (pref[right] - pref[left - 1]) % MOD
            else:
                dp[i] = 0
            pref[i] = (pref[i - 1] + dp[i]) % MOD

        # People who still remember at end of day n:
        # sum dp[j] for j in [n - forget + 1, n]
        start = n - forget + 1
        if start < 1:
            start = 1
        ans = (pref[n] - pref[start - 1]) % MOD
        return ans
```
- Notes:
  - dp[i] counts new learners on day i. People share starting at day learn_day + delay and stop sharing on day learn_day + forget - 1.
  - Using prefix sums pref allows computing each dp[i] in O(1), yielding overall O(n) time.
  - Space is O(n) for dp and pref; this can be reduced by maintaining a sliding window sum instead of keeping the whole prefix array.
  - Final result is sum of dp values for those who haven't forgotten by day n, computed via the prefix array.