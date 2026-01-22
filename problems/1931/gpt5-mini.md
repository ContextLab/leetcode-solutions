# [Problem 1931: Painting a Grid With Three Different Colors](https://leetcode.com/problems/painting-a-grid-with-three-different-colors/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to paint an m x n grid with 3 colors so that no two adjacent cells (horizontally or vertically) share the same color. m is small (<= 5) while n can be up to 1000. That suggests treating one dimension (m) as the state dimension and iterating along the other (n) with dynamic programming.

The idea that comes to mind: consider each column as a state — a length-m vector of colors — but only keep columns that are internally valid (no same color in adjacent rows). Number of possible column states is at most 3^m (3^5 = 243), so manageable. Next, two adjacent columns must differ row-wise (no same color in the same row). That gives an adjacency relation between valid column states. Then we can do DP along columns: for each column index, count ways to end with each state based on previous column states that are compatible. n up to 1000 -> O(n * S^2) transitions is fine because S <= 243.

Edge quick-check: m = 1 is special but handled by the same scheme (3 initial states, each next column must be different from previous -> 3 * 2^(n-1)). No need for matrix exponentiation for n=1000; straightforward DP is fine.

## Refining the problem, round 2 thoughts
Refinements:
- Generate all base-3 numbers from 0 to 3^m - 1, convert to arrays of length m representing colors, and only keep those where adjacent entries differ.
- Precompute compatibility lists between valid states: a state s1 is compatible with s2 if for all row indices r, s1[r] != s2[r].
- Initialize dp for the first column as 1 for every valid state (any valid column can be the first). Then repeat n-1 times: new_dp[next_state] += dp[cur_state] for all compatible pairs (cur_state -> next_state).
- Use modulo 10^9+7.
- Complexity: Let S be number of valid columns (S <= 243). Preprocessing states and compatibility is O(3^m * m + S^2 * m) ~ negligible. DP is O(n * E) where E is number of compatible ordered pairs (worst-case S^2). For given constraints, this is fine.

Edge cases:
- m = 1 or n = 1 behave correctly with this approach.
- Keep careful about modulo and avoid unnecessary overhead in inner loops.

## Attempted solution(s)
```python
class Solution:
    def colorTheGrid(self, m: int, n: int) -> int:
        MOD = 10**9 + 7

        # Generate all possible columns (as base-3 numbers) and keep only those
        # that have no two equal adjacent colors vertically.
        max_states = 3 ** m
        valid = []
        colors = []  # list of lists: colors[idx][row] gives color 0..2

        for mask in range(max_states):
            col = []
            x = mask
            valid_flag = True
            prev = -1
            for _ in range(m):
                c = x % 3
                x //= 3
                if c == prev:
                    valid_flag = False
                    break
                col.append(c)
                prev = c
            if valid_flag:
                # col currently in order rows 0..m-1 (since we appended in the loop)
                # keep as list
                colors.append(col)
                valid.append(mask)

        k = len(colors)

        # Precompute compatibility: state i -> list of states j that are compatible
        # (i.e., no same color in any row).
        compat = [[] for _ in range(k)]
        for i in range(k):
            ci = colors[i]
            for j in range(k):
                cj = colors[j]
                ok = True
                # check row-wise
                for r in range(m):
                    if ci[r] == cj[r]:
                        ok = False
                        break
                if ok:
                    compat[i].append(j)

        # DP across columns: dp[i] = number of ways for current column to be state i
        dp = [1] * k  # first column can be any valid column
        for _ in range(n - 1):
            new_dp = [0] * k
            for i in range(k):
                ways = dp[i]
                if ways:
                    for j in compat[i]:
                        new_dp[j] = (new_dp[j] + ways) % MOD
            dp = new_dp

        return sum(dp) % MOD
```
- Notes on approach:
  - We enumerate all possible column patterns of length m (3^m possible), filter those with no equal adjacent colors vertically.
  - Build a compatibility graph where an ordered pair (i, j) is allowed when all rows differ between columns i and j.
  - Use DP along n columns; initial dp is 1 for every valid column pattern.
  - Time complexity: O(3^m * m + S^2 * m + n * S^2) in worst case where S is number of valid columns (S <= 3^m, with 3^5 = 243). Practically, preprocessing is small and the DP runs comfortably for n up to 1000. Space complexity: O(S^2) for compat lists plus O(S) for dp (worst-case memory ~ few tens of thousands entries).
  - This is a standard state-compression + transition DP that fits constraints well.