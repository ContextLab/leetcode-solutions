# [Problem 2770: Maximum Number of Jumps to Reach the Last Index](https://leetcode.com/problems/maximum-number-of-jumps-to-reach-the-last-index/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the maximum number of jumps from index 0 to index n-1 where a jump i->j (j>i) is allowed if |nums[j]-nums[i]| <= target. This is a directed acyclic graph (edges only go forward), so longest-path in a DAG dynamic programming comes to mind. A naive DFS that explores all paths would work but could be exponential. Since edges only go from smaller index to larger index, processing indices in increasing order and computing the best (maximum) jumps to each index from 0 is natural.

We can set dp[i] = maximum jumps to reach i (or -inf/unset if unreachable). dp[0] = 0. For every i from 1..n-1, check all j < i: if dp[j] is reachable and |nums[i]-nums[j]| <= target then dp[i] = max(dp[i], dp[j]+1). Finally answer dp[n-1] or -1 if unreachable.

n <= 1000, so O(n^2) is fine (1e6 comparisons worst-case). There are potential alternatives using segment trees or coordinate compression for larger constraints, but not necessary here.

## Refining the problem, round 2 thoughts
Edge cases:
- target = 0, jump only when values equal.
- If no path exists, return -1.
- dp values represent count of jumps; dp[0]=0.
- Use a sentinel for unreachable (like -inf or None) to avoid mixing with valid counts.

Time complexity: O(n^2). Space: O(n).

Alternative: If n were large, could try to maintain structures of indices grouped by value ranges to speed up lookups, but not required.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumJumps(self, nums: List[int], target: int) -> int:
        n = len(nums)
        # dp[i] = maximum jumps to reach index i, -inf means unreachable
        NEG = -10**9
        dp = [NEG] * n
        dp[0] = 0
        
        for i in range(1, n):
            best = NEG
            ai = nums[i]
            for j in range(i):
                if dp[j] == NEG:
                    continue
                # check allowed jump
                if -target <= ai - nums[j] <= target:
                    # can jump from j to i
                    cand = dp[j] + 1
                    if cand > best:
                        best = cand
            dp[i] = best
        
        return dp[-1] if dp[-1] != NEG else -1
```
- Approach: Dynamic programming over indices in increasing order. For each target index i, examine all prior indices j to see if a jump is allowed; if so, update dp[i] = max(dp[i], dp[j]+1).
- Time complexity: O(n^2) where n = len(nums), because for each i we loop over j < i.
- Space complexity: O(n) for the dp array.
- Implementation details: Use a large negative sentinel (NEG) to indicate unreachable dp entries. Return -1 if the last index is unreachable.