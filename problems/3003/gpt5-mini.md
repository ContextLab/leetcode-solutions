# [Problem 3003: Maximize the Number of Partitions After Operations](https://leetcode.com/problems/maximize-the-number-of-partitions-after-operations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We repeatedly remove the longest prefix containing at most k distinct characters. That greedy partitioning is deterministic for a fixed string. We are allowed to change at most one index (to any lowercase letter) before partitioning. How can one change affect the greedy cuts? Changing a character can either (a) allow a prefix to grow longer (if you change a new letter into an existing one), which reduces number of partitions (not helpful), or (b) introduce a new distinct letter earlier than it would naturally appear, causing the current prefix to stop earlier and thus potentially increasing the number of partitions. So we should consider, for each starting index i, where we can force a cut by using the single change, and otherwise where the greedy cut would occur without using the change.

This suggests dynamic programming from left-to-right, with a state for whether the change has been used. From position i:
- If the change is already used, we must take the greedy maximal prefix (with ≤k distinct) and continue.
- If the change is not yet used, we can either not use it (take the greedy maximal prefix) or use it to force an earlier cut at any position t where the distinct count in s[i:t-1] is exactly k (changing s[t-1] or s[t] appropriately to create a new distinct and end the prefix at t-1). So dp(i, used) = max(1 + dp(next_no_change, used), and, if not used, max over candidate t of 1 + dp(t, 1)).

We must efficiently know for each start i:
- the next index r where greedy cut occurs (first index that cannot be included because it would push distinct > k),
- all indices t (t > i) such that distinct(s[i:t-1]) == k (these are places we can force a cut using the single change).

k ≤ 26 bounds how many distinct increases can occur in any expansion from i, so the number of candidate cut positions per start is ≤ n but with at most 26 distinct events; overall precomputation per start is O(length of explored window). Precomputing these for all i gives an O(n^2) worst-case method which is acceptable for n ≤ 10^4 in practice with simple arrays and small constants.

## Refining the problem, round 2 thoughts
- If the whole string already has ≤ k distinct letters, answer is 1 immediately.
- We'll precompute for each start i:
  - next_no_change[i] := index r where greedy prefix ends (i.e., the next starting index after removing the maximal prefix beginning at i without using any change),
  - candidates[i] := list of indexes t (i < t ≤ n) such that distinct(s[i : t-1]) == k (so we can force a cut at t).
- Then use memoized DP dp(i, used) with 2*n states.
- Time complexity: precomputation of next/candidates takes O(n^2) worst-case (but each expansion only increases distinct ≤ 26 times), DP has O(n) states and O(#candidates per i) transitions; overall O(n^2) worst-case.
- Space: O(n + total candidates) ~ O(n^2) worst-case but practically far less (distinct bound helps).

Now implement the described approach with some micro-optimizations:
- Convert string to int array 0..25 to speed indexing.
- Precompute next_no_change and candidates for each i once.
- Memoize dp in a 2D list.

## Attempted solution(s)
```python
from typing import List
import sys
sys.setrecursionlimit(1000000)

class Solution:
    def maxNumOfSubstringsAfterOneChange(self, s: str, k: int) -> int:
        n = len(s)
        s_arr = [ord(c) - 97 for c in s]

        # If the whole string already fits in k distinct, answer is 1
        if len(set(s)) <= k:
            return 1

        # Precompute for each start i:
        # - next_no_change[i]: index r where greedy prefix starting at i ends (next start)
        # - candidates[i]: list of indices t (i < t <= n) with distinct(s[i:t-1]) == k
        next_no_change = [n] * (n + 1)
        candidates: List[List[int]] = [[] for _ in range(n + 1)]

        # For each i, expand forward until distinct > k and record candidate cut positions.
        for i in range(n):
            freq = [0] * 26
            distinct = 0
            r = i
            # Expand r until distinct > k
            while r < n:
                ch = s_arr[r]
                if freq[ch] == 0:
                    distinct += 1
                freq[ch] += 1
                if distinct > k:
                    # cannot include r, so next start is r
                    next_no_change[i] = r
                    break
                # If distinct == k, we can force a cut after r (i.e., next start t = r+1)
                if distinct == k:
                    candidates[i].append(r + 1)
                r += 1
            else:
                # reached end with distinct <= k
                next_no_change[i] = n

        # DP memoization: dp[i][used] = max partitions from i with used flag
        memo = [[-1] * 2 for _ in range(n + 1)]

        def dp(i: int, used: int) -> int:
            if i >= n:
                return 0
            if memo[i][used] != -1:
                return memo[i][used]

            # Option 1: don't use a change here (or we already used it)
            r = next_no_change[i]
            best = 1 + dp(r, used)

            # Option 2: if change not used yet, try forcing a cut at any candidate t
            if used == 0:
                # candidates[i] holds t values where distinct(s[i:t-1]) == k
                for t in candidates[i]:
                    # Force cut at t, and mark change used
                    # Note: t could be n which is fine (dp(n,1) == 0)
                    best = max(best, 1 + dp(t, 1))

            memo[i][used] = best
            return best

        return dp(0, 0)


# For LeetCode-style API, the method name would be maxNumOfSubstringsAfterOneChange as above.
# Provide a small wrapper matching expected single-function usage.
def maximizeTheNumberOfPartitionsAfterOperations(s: str, k: int) -> int:
    sol = Solution()
    return sol.maxNumOfSubstringsAfterOneChange(s, k)


# Example quick tests
if __name__ == "__main__":
    print(maximizeTheNumberOfPartitionsAfterOperations("accca", 2))  # expected 3
    print(maximizeTheNumberOfPartitionsAfterOperations("aabaab", 3)) # expected 1
    print(maximizeTheNumberOfPartitionsAfterOperations("xxyz", 1))   # expected 4
```

- Notes about approach:
  - We precompute for each starting index i where the greedy cut would happen next (next_no_change[i]) and all positions t where the distinct count in s[i:t-1] equals k (candidates[i]). Using a change at position t allows us to force a cut at t (prefix ends at t-1).
  - The DP dp(i, used) considers either taking the greedy maximal prefix (no change at this step) or — if the change hasn't been used — using the change to force an earlier cut at any valid candidate t. We add 1 for the partition we remove now and recurse.
  - Time complexity: worst-case O(n^2) due to the precomputation of prefix info for every start i (n ≤ 10^4 so acceptable). In practice the number of distinct changes across a run is ≤ 26, so the inner work per start is limited.
  - Space complexity: O(n + total candidates) which in worst-case behaves like O(n^2) but practically small because of the 26-letter bound; main DP memo is O(n).
  - This solution is careful to avoid repeatedly recomputing the same prefix information by precomputing and memoizing DP results.