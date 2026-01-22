# [Problem 3333: Find the Original Typed String II](https://leetcode.com/problems/find-the-original-typed-string-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We get the final typed word where long-presses can repeat characters. The final word can be split into runs of identical characters with lengths r1, r2, ..., rm. The intended original string must have the same sequence of run-characters, but each run in the original can have length xi where 1 <= xi <= ri (because long-press only increases a run, original run must be at least 1 and at most the final run length). We need to count how many choices of xi produce an original string of length at least k, modulo 1e9+7.

So it's a counting problem on bounded integer vectors: xi in [1, ri] and sum xi >= k. A standard transform is yi = xi - 1 so yi in [0, ri-1] and we need sum yi >= k - m. If k <= m then the minimum possible original length m already meets the requirement, so all possible assignments (product of ri choices) are valid. Otherwise we need to count assignments with sum yi >= S where S = k - m.

Count of assignments with sum >= S = total assignments - assignments with sum <= S-1. Total is product ri. Counting assignments with bounded sum up to T = S-1 can be done with DP on sums up to T. Note k <= 2000 so if m < k then m <= k-1 <= 1999, so the DP runs across at most ~2000 runs and sum dimension <=2000 — tractable. If m >= k we return total product immediately. This leads to an O(n) run detection + O(m * S) DP solution (and m * S <= k^2).

## Refining the problem, round 2 thoughts
- Build run lengths ri by scanning the word once.
- If m >= k: return product(ri) % MOD.
- Else S = k - m (>=1). Let bi = ri - 1 (upper bounds for yi).
- We want number of yi assignments with 0 <= yi <= bi and sum yi <= S-1. DP over prefix of runs and sum states 0..S-1:
  dp[s] = number of ways to get sum s after processing some runs.
  Transition for adding a run with bound b: dp_new[s] = sum_{t=0..min(b,s)} dp[s-t].
- Use prefix sums to compute that transition in O(S) per run: dp_new[s] = prefix[s] - prefix[s-b-1] (handle negative index).
- After processing all runs, bad = sum(dp[0..S-1]) is the number of assignments with sum <= S-1.
- Answer = (total - bad) % MOD.
- Complexity: scanning word O(n), DP O(m * S) with m < k and S <= k so O(k^2) worst-case (k <= 2000 => ~4e6 operations), memory O(S).

Edge cases:
- Word length up to 5e5, k up to 2000.
- Ensure modulo arithmetic correctness (make results >= 0).

## Attempted solution(s)
```python
class Solution:
    def countTexts(self, word: str, k: int) -> int:
        # not used; leetcode expects method name find... but will provide required method below
        pass

    def numberOfOriginals(self, word: str, k: int) -> int:
        MOD = 10**9 + 7

        # build run lengths
        n = len(word)
        runs = []
        i = 0
        while i < n:
            j = i + 1
            while j < n and word[j] == word[i]:
                j += 1
            runs.append(j - i)
            i = j

        m = len(runs)
        # total number of assignments (each run xi in [1, ri]) is product ri
        total = 1
        for r in runs:
            total = (total * r) % MOD

        # If minimal possible original length m >= k, all assignments valid
        if m >= k:
            return total

        # Need sum yi >= S where yi = xi - 1, 0 <= yi <= ri-1
        S = k - m  # target lower bound for sum yi
        T = S - 1  # we will count assignments with sum <= T (bad), then subtract from total

        # dp[s] = number of ways to get sum s (0 <= s <= T) after processing some runs
        dp = [0] * (T + 1)
        dp[0] = 1

        for r in runs:
            b = r - 1  # yi upper bound for this run
            # build prefix sums of dp for fast convolution
            prefix = [0] * (T + 1)
            prefix[0] = dp[0]
            for s in range(1, T + 1):
                prefix[s] = (prefix[s-1] + dp[s]) % MOD

            new_dp = [0] * (T + 1)
            # dp_new[s] = prefix[s] - prefix[s-b-1] if s-b-1 >= 0 else prefix[s]
            if b >= T:
                # b large enough to allow any t in [0..s], so dp_new[s] = prefix[s]
                for s in range(T + 1):
                    new_dp[s] = prefix[s]
            else:
                for s in range(T + 1):
                    left = prefix[s]
                    right = prefix[s - b - 1] if s - b - 1 >= 0 else 0
                    new_dp[s] = (left - right) % MOD

            dp = new_dp

        bad = sum(dp) % MOD
        ans = (total - bad) % MOD
        return ans

# Provide the LeetCode expected function name and signature:
class Solution:
    def findTheOriginalString(self, word: str, k: int) -> int:
        MOD = 10**9 + 7

        # build run lengths
        n = len(word)
        runs = []
        i = 0
        while i < n:
            j = i + 1
            while j < n and word[j] == word[i]:
                j += 1
            runs.append(j - i)
            i = j

        m = len(runs)
        # total number of assignments (xi in [1, ri]) is product ri
        total = 1
        for r in runs:
            total = (total * r) % MOD

        # If minimal possible original length m >= k, all assignments valid
        if m >= k:
            return total

        S = k - m  # we need sum yi >= S where yi = xi-1
        T = S - 1  # count assignments with sum <= T (bad)

        dp = [0] * (T + 1)
        dp[0] = 1

        for r in runs:
            b = r - 1
            prefix = [0] * (T + 1)
            prefix[0] = dp[0]
            for s in range(1, T + 1):
                prefix[s] = (prefix[s-1] + dp[s]) % MOD

            new_dp = [0] * (T + 1)
            if b >= T:
                for s in range(T + 1):
                    new_dp[s] = prefix[s]
            else:
                for s in range(T + 1):
                    left = prefix[s]
                    right = prefix[s - b - 1] if s - b - 1 >= 0 else 0
                    new_dp[s] = (left - right) % MOD
            dp = new_dp

        bad = sum(dp) % MOD
        return (total - bad) % MOD
```
- Approach notes:
  - Convert the problem into counting bounded integer vectors xi in [1, ri] with sum >= k.
  - Transform to yi = xi-1 to get 0 <= yi <= ri-1 and require sum yi >= S = k - m.
  - If m >= k, every assignment qualifies so answer is product of ri.
  - Otherwise count assignments with sum <= S-1 using DP with prefix sums (bounded knapsack / sliding window), subtract from total.
- Complexity:
  - Building runs: O(n).
  - DP: O(m * (k - m)) where m < k, worst-case O(k^2). Since k <= 2000, worst-case ~4e6 operations — feasible.
  - Space: O(k).
- Correctness:
  - The mapping xi in [1,ri] is exact because original must have at least one character per run and can't have more than the final run.
  - The DP counts all combinations that violate the length requirement; subtracting from total yields the number of valid originals.