# [Problem 1871: Jump Game VII](https://leetcode.com/problems/jump-game-vii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to determine whether we can reach the last index from index 0 given jumps constrained by [minJump, maxJump] and only landing on '0' positions. Brute force DFS/BFS that tries all possible jumps from each reachable index would be too slow in worst case (O(n * maxJump)). Observing structure: whether index i is reachable depends only on whether there's at least one reachable index in a previous window [i-maxJump, i-minJump]. That suggests we can test reachability efficiently by maintaining either a running count (prefix-sum of reachable positions) or using BFS with a sliding window/pointer so we don't re-check indices multiple times. Both lead to O(n) time and O(n) space.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- s[0] is guaranteed '0'. If s[n-1] is '1', answer is false quickly.
- For each target index i, we only need to know if any position in a certain previous window is reachable; so use prefix sums of reachable or BFS + farthest processed pointer.
- Using BFS + a farthest pointer: when processing a reachable index idx, we attempt to enqueue indices in [idx+minJump, idx+maxJump] but only those not already considered; maintain 'farthest' as the smallest index not yet processed into the queue from previous windows. This ensures each index is considered at most once.
- Complexity: O(n) time (each index enqueued/checked once), O(n) space for visited queue/array.
- Alternatively, DP + prefix-sum: reachable[i] = (s[i]=='0') and (prefix[right+1] - prefix[left] > 0), also O(n).

I'll implement the BFS with a sliding window (farthest) since it's intuitive and concise.

## Attempted solution(s)
```python
from collections import deque

class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        if s[-1] == '1':  # quick fail if last position is blocked
            return False

        q = deque([0])
        visited = [False] * n
        visited[0] = True
        # 'farthest' is the smallest index that hasn't yet been considered/enqueued
        # from any previous reachable position's jump ranges.
        farthest = 1

        while q:
            idx = q.popleft()
            start = idx + minJump
            end = min(idx + maxJump, n - 1)
            # only iterate from max(start, farthest) to end to avoid repeated work
            j = max(start, farthest)
            while j <= end:
                if s[j] == '0' and not visited[j]:
                    visited[j] = True
                    if j == n - 1:
                        return True
                    q.append(j)
                j += 1
            # update farthest to one past end, because these indices have now been considered
            farthest = max(farthest, end + 1)

        return visited[n - 1]
```
- Notes about the solution:
  - Approach: BFS with a deque of reachable indices and a "farthest" pointer to ensure we only try each index once across all jump windows. For each popped index idx, we attempt to enqueue indices in [idx+minJump, min(idx+maxJump, n-1)] but start from farthest to avoid re-checking indices already handled by previous pops.
  - Time complexity: O(n). Each index is examined at most once in the inner loop (the farthest pointer ensures no repeated checks).
  - Space complexity: O(n) for visited and queue in the worst case.
  - Alternative: a DP + prefix-sum solution can compute reachability in O(n) as well: reachable[i] = (s[i]=='0') and (prefix[ right+1 ] - prefix[ left ] > 0) where left = max(0, i-maxJump) and right = i-minJump.