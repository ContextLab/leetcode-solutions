# [Problem 1340: Jump Game V](https://leetcode.com/problems/jump-game-v/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the maximum number of indices I can visit starting from any index, where from index i I can jump left or right up to distance d, but only to strictly smaller values and only as long as no intervening element is >= arr[i]. This sounds like we can view each index as a node and allowed jumps as directed edges from higher to lower values until a blocking element appears. The natural approach is dynamic programming: dp[i] = maximum number of indices reachable starting from i (including i). For each i, explore left and right up to distance d and stop when we hit arr[j] >= arr[i]. This exploration has overlapping subproblems so memoization (DFS + cache) should work. Complexity likely O(n * d) since for each i we scan up to d positions in each direction.

I also recall an alternate approach with monotonic stack to build a DAG and then compute longest path, but the DFS+memo is simpler and fine for n <= 1000.

## Refining the problem, round 2 thoughts
Refinements and important details:
- When scanning in a direction, as soon as arr[j] >= arr[i], further positions in that direction are inaccessible from i (we must break).
- Equal heights block jumps too (arr[j] >= arr[i] blocks).
- dp[i] base is 1 (you can always visit i itself).
- Use recursion + memo or iterative DP over indices sorted by value (another valid approach). Recursion with caching is straightforward.
- Edge cases: all equal values -> every dp[i] = 1. Strictly decreasing array with d = 1 -> can traverse all indices.
- Time complexity: each index scans at most d entries in each direction, so O(n*d). Space: O(n) for memo and recursion stack.
- Use sys.setrecursionlimit to be safe.

## Attempted solution(s)
```python
from functools import lru_cache
import sys

class Solution:
    def maxJumps(self, arr, d):
        sys.setrecursionlimit(10000)
        n = len(arr)
        
        @lru_cache(None)
        def dfs(i):
            best = 1  # at least visit i itself
            # explore left
            for step in range(1, d+1):
                j = i - step
                if j < 0:
                    break
                if arr[j] >= arr[i]:
                    break
                best = max(best, 1 + dfs(j))
            # explore right
            for step in range(1, d+1):
                j = i + step
                if j >= n:
                    break
                if arr[j] >= arr[i]:
                    break
                best = max(best, 1 + dfs(j))
            return best
        
        return max(dfs(i) for i in range(n))
```
- Notes about the solution:
  - Approach: DFS with memoization. For each index i, attempt jumps left and right up to distance d, stopping when encountering a blocking element arr[j] >= arr[i]. dp(i) = 1 + max(dp(j)) over reachable j, or 1 if none.
  - Time complexity: O(n * d) in worst case — for each of the n indices we may scan up to d positions in both directions.
  - Space complexity: O(n) for memoization and recursion stack (stack depth up to n in worst case).
  - Important implementation detail: breaking when arr[j] >= arr[i] is crucial — equal values block further jumps and prevent continuing scanning past that index.