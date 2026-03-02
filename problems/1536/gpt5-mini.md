# [Problem 1536: Minimum Swaps to Arrange a Binary Grid](https://leetcode.com/problems/minimum-swaps-to-arrange-a-binary-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the grid such that all cells above the main diagonal are zeros. For row i (0-based), columns 0..i-1 can be anything, but positions i+1..n-1 (i.e., to the right of the diagonal) must be zeros. That means row i must have at least (n-1-i) trailing zeros (zeros at the right end). So for each row we can compute how many trailing zeros it has (or equivalently the index of the rightmost 1). Then we need to place, at row i, any row whose trailingZeros >= (n-1-i).

Swapping is allowed only between adjacent rows, but adjacent swaps allow us to bubble any lower row up at cost equal to how many positions it moves. A greedy strategy suggests: for each target position i from 0..n-1, find the first row at or below i that satisfies the trailing-zero requirement, bubble it up by adjacent swaps, and add the number of swaps. If none found, return -1.

This fits well because choosing the earliest acceptable row minimizes swaps used for that position and doesn't harm future placements (a standard greedy/swap-bubble argument).

## Refining the problem, round 2 thoughts
- Compute an array tz where tz[k] is trailing zeros in row k (or compute lastOneIndex and derive tz). For row i, required = n-1-i.
- Search j from i..n-1 for the first tz[j] >= required. If not found, impossible -> -1.
- Bubble tz[j] left to position i by swapping with its predecessor repeatedly; each adjacent swap increments answer by 1.
- Complexity: computing tz is O(n^2) in worst case (each row has n elements), and the greedy bubbling is O(n^2) in worst case, so overall O(n^2) time which is fine for n <= 200. Space O(n).

Edge cases:
- All rows identical and cannot satisfy some position -> return -1.
- Already valid grid -> zero swaps.
- n=1 trivial -> zero swaps.

Alternative: maintain list of last one positions and work with them. Or use deque; but simple list and swaps suffice.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minSwaps(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # Compute trailing zeros for each row.
        tz = [0] * n
        for i in range(n):
            # count zeros from right until first 1 or beginning
            count = 0
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 0:
                    count += 1
                else:
                    break
            tz[i] = count

        swaps = 0
        # For each position i, we need a row with tz >= n-1-i
        for i in range(n):
            required = n - 1 - i
            j = i
            # find a row at or below i that satisfies requirement
            while j < n and tz[j] < required:
                j += 1
            if j == n:
                return -1  # impossible
            # bubble row j up to position i using adjacent swaps
            while j > i:
                tz[j], tz[j - 1] = tz[j - 1], tz[j]
                swaps += 1
                j -= 1

        return swaps
```
- Notes:
  - The solution computes trailing zeros per row, then greedily places suitable rows into each target position by bubbling them up. This greedy is optimal because using the earliest acceptable row minimizes swaps for that position and doesn't prevent future placements.
  - Time complexity: O(n^2) — computing trailing zeros costs O(n^2) in the worst case and the bubbling/searching is O(n^2) in total.
  - Space complexity: O(n) for the tz array (ignoring input).