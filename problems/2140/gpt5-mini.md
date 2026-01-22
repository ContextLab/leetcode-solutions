# [Problem 2140: Solving Questions With Brainpower](https://leetcode.com/problems/solving-questions-with-brainpower/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We must process questions in order and decide to solve or skip each. If we solve question i we get points[i] but must skip the next brainpower[i] questions; if we skip, we move to i+1. This is a sequential decision process with overlapping subproblems — dynamic programming comes to mind. A recursion that at index i returns the maximum points from i to end: either take points[i] + best(i + brainpower[i] + 1) or skip and take best(i+1). Because decisions depend only on future indices, we can compute DP from the end backwards. Greedy doesn't work because a local larger points might block many future questions.

## Refining the problem, round 2 thoughts
- Use dp[i] = maximum points obtainable starting from question i. Answer is dp[0].
- Recurrence: dp[i] = max(points[i] + dp[i + brainpower[i] + 1], dp[i+1]). Handle indices beyond the array as 0.
- Compute dp bottom-up from i = n-1 down to 0. Use dp array of size n+1 with dp[n] = 0 for convenience so dp[next_index] is safe.
- Edge cases: n = 1, large brainpower values that jump past end, values large but Python int handles it.
- Time complexity: O(n) — each index processed once. Space complexity: O(n) for dp; can be considered optimal for this straightforward DP. (One can discuss other space trade-offs but dp array is simple and clear.)

## Attempted solution(s)
```python
class Solution:
    def mostPoints(self, questions: list[list[int]]) -> int:
        n = len(questions)
        # dp[i] = max points achievable starting from question i
        # use size n+1 so dp[n] = 0 (base case)
        dp = [0] * (n + 1)

        for i in range(n - 1, -1, -1):
            points, brainpower = questions[i]
            next_index = i + brainpower + 1
            take = points + (dp[next_index] if next_index <= n else 0)  # dp has length n+1, safe when next_index == n
            skip = dp[i + 1]
            dp[i] = max(take, skip)

        return dp[0]
```
- Approach: bottom-up DP iterating from the last question backward. At each index decide to take (earn points and jump past brainpower questions) or skip (move to next).
- Time complexity: O(n), where n = len(questions). Each question is processed once.
- Space complexity: O(n) for the dp array (size n+1).