# [Problem 3532: Path Existence Queries in a Graph I](https://leetcode.com/problems/path-existence-queries-in-a-graph-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The graph definition: an undirected edge exists between i and j iff |nums[i] - nums[j]| <= maxDiff. nums is sorted non-decreasing. That suggests we can leverage ordering.

First idea: build full graph by checking every pair would be O(n^2) — too slow for n up to 1e5. Because nums is sorted, for a particular index i, all indices j with nums[j] - nums[i] <= maxDiff form a contiguous block to the right (and similarly to the left). That suggests sliding-window or unioning ranges.

A simpler observation: if nums[i] and nums[j] (i<j) satisfy nums[j] - nums[i] <= maxDiff, then for every adjacent pair k,k+1 with i <= k < j, we must have nums[k+1] - nums[k] <= maxDiff as well — otherwise the sum of adjacent diffs would exceed maxDiff. Therefore having an edge between i and j implies every adjacent diff in [i, j-1] is <= maxDiff. Conversely, if all adjacent diffs in [i, j-1] are <= maxDiff, then i and j are connected via the chain of those adjacent edges. So we only need to union adjacent indices i and i+1 when nums[i+1] - nums[i] <= maxDiff. After that, connectivity queries reduce to checking same DSU component.

So Union-Find (DSU) on adjacent indices is efficient.

## Refining the problem, round 2 thoughts
Edge cases:
- Self queries (u == v) should be true — DSU find will handle that.
- Duplicates in nums are OK because difference zero <= maxDiff may connect many equal values.
- maxDiff = 0: only equal values connect; union adjacent when diff==0.

Complexity considerations:
- Building unions by scanning adjacent pairs is O(n) unions.
- Each query is a DSU find pair check, amortized near O(α(n)).
- Space: O(n) for DSU.

This is optimal and simple.

## Attempted solution(s)
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            # path compression (two-step)
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        return True


class Solution:
    def distanceLimitedPathsExist(self, n: int, nums: list[int], maxDiff: int, queries: list[list[int]]) -> list[bool]:
        dsu = DSU(n)
        # Union adjacent indices if their difference <= maxDiff
        for i in range(n - 1):
            if nums[i+1] - nums[i] <= maxDiff:
                dsu.union(i, i+1)

        ans = []
        for u, v in queries:
            ans.append(dsu.find(u) == dsu.find(v))
        return ans
```
- Approach: Use a Disjoint Set Union (union-find). Because nums is sorted, if nums[j] - nums[i] <= maxDiff then every adjacent difference between i and j is <= maxDiff, so unioning only adjacent indices with diff <= maxDiff yields correct connectivity for all pairs.
- Time complexity: O(n + q * α(n)) where n = len(nums), q = number of queries, α is inverse Ackermann (almost constant). Building unions scans n-1 adjacent differences; each query costs two find operations.
- Space complexity: O(n) for DSU arrays.