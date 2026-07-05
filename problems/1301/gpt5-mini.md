# [Problem 1301: Number of Paths with Max Score](https://leetcode.com/problems/number-of-paths-with-max-score/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to move from 'S' (bottom-right) to 'E' (top-left) with allowed moves up, left, and up-left, collecting digits along the way and avoiding 'X' cells. We want the maximum sum of digits collected and the number of distinct paths that achieve that maximum (mod 1e9+7). This is a dynamic programming problem on a grid where each cell's best result depends on reachable neighbors in one direction.

Because the allowed moves from S to E are up/left/upleft, it's convenient to reverse the viewpoint: consider starting from S and propagating values to cells above/left (or equivalently start at E and use transitions down/right/down-right). Either view works. We need to keep, for every cell, the maximum sum achievable from that cell to S and how many ways achieve that maximum. Use two DP arrays: dp_sum and dp_cnt. For unreachable cells dp_cnt = 0. Base case: dp at S is (0,1). Then, for each cell (not an obstacle), consider its three "children" that lie towards S (down, right, down-right if iterating from top-left to bottom-right, or similarly if iterating backwards). Choose children that produce the maximal dp_sum and sum their dp_cnt for dp_cnt at the current cell. Add the current cell's digit (if any) to that maximal child sum. At the end, read dp at E. If dp_cnt[E] == 0, return [0,0]. Otherwise return [dp_sum[E], dp_cnt[E] % MOD].

## Refining the problem, round 2 thoughts
- We must be careful to treat 'E' and 'S' as having value 0 (they do not contribute digits).
- Use a sentinel for unreachable dp_sum (e.g., a large negative value) and dp_cnt = 0 for unreachable.
- Ensure iteration order ensures children have been computed before the parent: iterate from bottom-right up to top-left when using children (i+1, j), (i, j+1), (i+1, j+1).
- Time complexity should be O(n^2) since each cell examines at most three neighbors. Space O(n^2) for dp arrays.
- Handle modulo only for counts; sums are small (<= 9 * n * n) so no overflow issues in Python.
- Edge case: no path exists => return [0,0].

## Attempted solution(s)
```python
class Solution:
    def pathsWithMaxScore(self, board: list[str]) -> list[int]:
        MOD = 10**9 + 7
        n = len(board)
        # locate S and E
        si = sj = ei = ej = -1
        for i in range(n):
            for j in range(n):
                if board[i][j] == 'S':
                    si, sj = i, j
                elif board[i][j] == 'E':
                    ei, ej = i, j

        # dp_sum: maximum sum from cell to S (or very negative if unreachable)
        # dp_cnt: number of ways to achieve that maximum (mod MOD)
        NEG = -10**9
        dp_sum = [[NEG] * n for _ in range(n)]
        dp_cnt = [[0] * n for _ in range(n)]

        # base: at S we have sum 0 and 1 way (standing still)
        dp_sum[si][sj] = 0
        dp_cnt[si][sj] = 1

        # iterate from bottom-right to top-left so children (i+1, j), (i, j+1), (i+1, j+1) are already computed
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if board[i][j] == 'X':
                    continue
                # skip S itself (already initialized). But it's safe to allow recomputation; we keep skip to be explicit:
                if i == si and j == sj:
                    continue

                best = NEG
                ways = 0
                for di, dj in ((1, 0), (0, 1), (1, 1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n and dp_cnt[ni][nj] > 0:
                        child_sum = dp_sum[ni][nj]
                        if child_sum > best:
                            best = child_sum
                            ways = dp_cnt[ni][nj]
                        elif child_sum == best:
                            ways = (ways + dp_cnt[ni][nj]) % MOD

                if ways > 0:
                    add = 0
                    # digits add to sum, 'E' and 'S' contribute 0
                    if board[i][j].isdigit():
                        add = int(board[i][j])
                    dp_sum[i][j] = best + add
                    dp_cnt[i][j] = ways

        # If E is unreachable, return [0,0]
        if dp_cnt[ei][ej] == 0:
            return [0, 0]
        return [dp_sum[ei][ej], dp_cnt[ei][ej] % MOD]
```
- Approach notes:
  - We initialize dp at S and propagate values toward top-left by considering children at (i+1, j), (i, j+1), (i+1, j+1).
  - For each cell we choose the maximum child sum and aggregate counts of children that achieve that max.
  - 'E' and 'S' have numeric value 0; numeric cells add their digit to the chosen maximum child sum.
  - Obstacle cells are skipped.
- Complexity:
  - Time: O(n^2) — each of the n^2 cells checks up to 3 neighbors.
  - Space: O(n^2) for dp_sum and dp_cnt arrays.
- Important details:
  - Counts are taken modulo 1e9+7 when aggregated.
  - Use a sufficiently small sentinel (NEG) to represent unreachable sums.