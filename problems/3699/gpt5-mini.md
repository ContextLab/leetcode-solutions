# [Problem 3699: Number of ZigZag Arrays I](https://leetcode.com/problems/number-of-zigzag-arrays-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count arrays length n, elements in [l, r], no equal adjacent, and no three consecutive elements strictly increasing or strictly decreasing. The "no three strictly monotone" condition implies that once you have two adjacent comparisons (between a1-a2 and a2-a3), they cannot be the same (cannot be both < or both >), so the comparisons between consecutive elements must alternate: up, down, up, down, ... or down, up, down, up, ... Adjacent elements must also be unequal, so comparisons are strict. Therefore the entire sequence is determined to follow one of two alternating-comparison patterns: start-up or start-down.

So count sequences for both patterns separately. For a fixed pattern, at step i the relation between a_{i-1} and a_i is known (either strict < or strict > depending on parity). We can do DP over position i and last value x: dp[i][x] = sum over allowed previous y of dp[i-1][y]. Each transition is a range sum over previous row (either y < x or y > x). Use prefix sums to compute those sums in O(1) per value. m = r-l+1 up to 2000, n up to 2000 => O(n*m) feasible.

## Refining the problem, round 2 thoughts
- Let m = r-l+1. Index values as 0..m-1 representing actual values.
- Base: dp[1][x] = 1 for all x (any single value).
- For positions i = 2..n, determine whether at this step we require previous < current or previous > current depending on whether we started with up or down and parity of i.
  - If pattern starts with up (a1<a2), then for even i we need prev < cur, for odd i>1 we need prev > cur.
  - For the other pattern reverse the parity.
- Use a rolling array: keep dp_prev (length m) and compute dp_cur using prefix sums of dp_prev.
- Sum results for both start patterns, mod 1e9+7.
- Time: O(n*m). Space: O(m).
- Edge cases: m>=2 since l<r per constraints, but code handles any m>=1 safely.

## Attempted solution(s)
```python
MOD = 10**9 + 7

class Solution:
    def countZigZagArrays(self, n: int, l: int, r: int) -> int:
        """
        Count number of length-n arrays with values in [l,r], no equal adjacent,
        and no three consecutive strictly increasing or decreasing.
        """
        m = r - l + 1
        # dp over values 0..m-1
        def count_for_start(start_up: bool) -> int:
            # dp_prev[x] = number of sequences of length i-1 ending with value x
            dp_prev = [1] * m  # i = 1
            # iterate i = 2..n
            for i in range(2, n + 1):
                # determine whether this step requires increasing (prev < cur)
                want_increasing = ((i % 2 == 0) == start_up)
                pref = [0] * m
                s = 0
                for idx in range(m):
                    s = (s + dp_prev[idx]) % MOD
                    pref[idx] = s
                dp_cur = [0] * m
                if want_increasing:
                    # dp_cur[x] = sum_{y < x} dp_prev[y] = pref[x-1]
                    for x in range(m):
                        if x == 0:
                            dp_cur[x] = 0
                        else:
                            dp_cur[x] = pref[x - 1]
                else:
                    # dp_cur[x] = sum_{y > x} dp_prev[y] = pref[m-1] - pref[x]
                    total = pref[m - 1]
                    for x in range(m):
                        dp_cur[x] = (total - pref[x]) % MOD
                dp_prev = dp_cur
            return sum(dp_prev) % MOD

        ans = (count_for_start(True) + count_for_start(False)) % MOD
        return ans

# Example usage:
# sol = Solution()
# print(sol.countZigZagArrays(3, 4, 5))  # -> 2
# print(sol.countZigZagArrays(3, 1, 3))  # -> 10
```

- Notes on approach:
  - We reduce the "no three monotone" condition to enforcing alternating comparisons after the first comparison.
  - DP dimension is n x m but we only keep previous row, so memory O(m).
  - Each DP row is computed using prefix sums to get the sum of a range in O(1) per value, so time O(n*m).
  - Complexity: Time O(n * (r-l+1)), Space O(r-l+1).
  - All arithmetic is modulo 10^9+7; subtraction is done modulo safely.