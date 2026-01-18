# [Problem 1895: Largest Magic Square](https://leetcode.com/problems/largest-magic-square/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find the largest k x k sub-square where all row sums, column sums and both diagonals sums are equal. Brute force would be: for each possible top-left and each possible k, compute all those sums and compare. But computing sums naively inside loops will be expensive. Prefix sums can make checking any row or column sum O(1). Diagonal sums can also be precomputed with diagonal prefix arrays (one for main diagonal, one for anti-diagonal). Since grid sizes are at most 50x50, an approach that tries k from largest to smallest and checks all positions with O(k) work per check is feasible.

Key idea:
- Precompute row prefix sums and column prefix sums to get any row/column segment sum in O(1).
- Precompute diagonal prefix sums for main and anti-diagonals for O(1) diagonal sum retrieval.
- Try k from min(m, n) down to 1; for each top-left (r, c) of k x k, compute target (first row sum) and verify all k row sums, all k column sums, and both diagonals equal to target.

If any k works, return it (we try descending so first success is maximal).

## Refining the problem, round 2 thoughts
Edge cases:
- 1x1 squares are always magic -> algorithm must return at least 1.
- Large element values (up to 1e6) but Python ints handle large sums.
- Make sure diagonal prefix arrays are computed correctly; anti-diagonal prefix is slightly trickier but standard construction works.

Complexity:
- Let m, n be grid dimensions and s = min(m, n).
- For each k we check (m-k+1)*(n-k+1) positions; each check tests k rows and k columns (O(k) checks) plus two diagonal checks O(1). So overall worst-case time complexity roughly O(m * n * s^2) (for constraints up to 50 this is fine).
- Space: O(m*n) for prefix arrays.

Now the implementation.

## Attempted solution(s)
```python
class Solution:
    def largestMagicSquare(self, grid):
        m = len(grid)
        n = len(grid[0])
        # rowPrefix[i][j] = sum of grid[i][0..j-1] (length n+1)
        rowPrefix = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                rowPrefix[i][j + 1] = rowPrefix[i][j] + grid[i][j]

        # colPrefix[i][j] = sum of grid[0..i-1][j] (length m+1)
        colPrefix = [[0] * n for _ in range(m + 1)]
        for j in range(n):
            for i in range(m):
                colPrefix[i + 1][j] = colPrefix[i][j] + grid[i][j]

        # diag1[i+1][j+1] = sum of main-diagonal elements along top-left direction
        # diag1[r+k][c+k] - diag1[r][c] gives sum of main diagonal starting at (r,c) length k
        diag1 = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                diag1[i + 1][j + 1] = diag1[i][j] + grid[i][j]

        # diag2[i+1][j] = diag2[i][j+1] + grid[i][j]
        # then diag2[r+k][c] - diag2[r][c+k] gives anti-diagonal sum from (r, c+k-1) down-left length k
        diag2 = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            # iterate j from right to left so diag2[i][j+1] is available
            for j in range(n - 1, -1, -1):
                diag2[i + 1][j] = diag2[i][j + 1] + grid[i][j]

        max_k = min(m, n)
        # try sizes from largest to smallest
        for k in range(max_k, 0, -1):
            # for each possible top-left (r,c)
            for r in range(0, m - k + 1):
                for c in range(0, n - k + 1):
                    # target is the sum of the first row in the square
                    target = rowPrefix[r][c + k] - rowPrefix[r][c]

                    ok = True
                    # check rows
                    for t in range(k):
                        row_sum = rowPrefix[r + t][c + k] - rowPrefix[r + t][c]
                        if row_sum != target:
                            ok = False
                            break
                    if not ok:
                        continue

                    # check columns
                    for t in range(k):
                        col_sum = colPrefix[r + k][c + t] - colPrefix[r][c + t]
                        if col_sum != target:
                            ok = False
                            break
                    if not ok:
                        continue

                    # check main diagonal
                    main_diag = diag1[r + k][c + k] - diag1[r][c]
                    if main_diag != target:
                        continue

                    # check anti-diagonal (top-right to bottom-left)
                    anti_diag = diag2[r + k][c] - diag2[r][c + k]
                    if anti_diag != target:
                        continue

                    # all checks passed
                    return k

        return 1
```
- Approach notes:
  - Precomputed rowPrefix, colPrefix, diag1 (main diagonal) and diag2 (anti-diagonal) allow O(1) retrieval of any row segment, column segment, and diagonal of a square.
  - We iterate k from largest to smallest so first valid square found is maximal; we can return immediately.
  - Complexity: time roughly O(m * n * min(m, n)^2) in the worst case (m, n <= 50 so it's acceptable). Space O(m * n) for prefix arrays.

