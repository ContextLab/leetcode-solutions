# [Problem 873: Length of Longest Fibonacci Subsequence](https://leetcode.com/problems/length-of-longest-fibonacci-subsequence/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share my internal chain-of-thought, but here is a concise summary of the approach: use dynamic programming on index pairs. For each pair (i, j) with i < j, keep the length of the longest Fibonacci-like subsequence that ends with arr[i], arr[j]. Use a value->index map to quickly find the previous element needed to extend a sequence (arr[k] such that arr[k] + arr[i] = arr[j]). Initialize lengths as 2 (minimum pair), update when a valid previous index exists, and track the maximum length >= 3.

## Refining the problem, round 2 thoughts
Refinements and considerations:
- Because arr is strictly increasing, for a pair (i, j) the needed previous value is arr[j] - arr[i], and if that value is >= arr[i] it can't form a valid earlier element (but checking k < i already enforces order).
- Use a hashmap mapping value to index to get O(1) lookups of the required previous element.
- Use a 2D DP array dp[i][j] initialized to 2 (the minimum length for any pair). When we find k < i with arr[k] + arr[i] = arr[j], set dp[i][j] = dp[k][i] + 1.
- Keep the maximum dp value seen; if it's < 3 return 0.
- Time complexity O(n^2), space O(n^2). n ≤ 1000 makes this feasible.

## Attempted solution(s)
```python
class Solution:
    def lenLongestFibSubseq(self, arr: list[int]) -> int:
        n = len(arr)
        # map value to its index for O(1) lookup
        index = {val: i for i, val in enumerate(arr)}
        
        # dp[i][j] = length of longest Fib-like subsequence ending with arr[i], arr[j]
        # initialize to 2 (any two numbers form a trivial length-2 start)
        dp = [[2] * n for _ in range(n)]
        ans = 0
        
        for j in range(n):
            for i in range(j):
                need = arr[j] - arr[i]
                k = index.get(need)
                # we need k < i to maintain ordering in the subsequence
                if k is not None and k < i:
                    dp[i][j] = dp[k][i] + 1
                    if dp[i][j] > ans:
                        ans = dp[i][j]
        return ans if ans >= 3 else 0
```
- Notes:
  - Approach: dynamic programming on index pairs with a value->index hashmap for fast predecessor lookup.
  - Correctness: dp[k][i] stores the best length ending with arr[k], arr[i]; extending that with arr[j] gives dp[i][j] = dp[k][i] + 1 when arr[k] + arr[i] == arr[j] and k < i.
  - Time complexity: O(n^2) loops over pairs (i, j); each iteration does O(1) work (hash lookup and updates). So overall O(n^2).
  - Space complexity: O(n^2) for the dp table, plus O(n) for the index map.
  - Edge cases: If no Fibonacci-like subsequence of length >= 3 exists, function returns 0. The strictly increasing property of arr ensures each value maps to a single index.