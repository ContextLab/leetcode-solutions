# [Problem 3208: Alternating Groups II](https://leetcode.com/problems/alternating-groups-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count how many length-k contiguous groups on a circle are alternating. For a contiguous group of k tiles to be alternating, every adjacent pair inside that group must be of different colors. So for a group starting at i (0-based), we need colors[i] != colors[i+1], colors[i+1] != colors[i+2], ..., colors[i+k-2] != colors[i+k-1]. That's k-1 adjacent checks per start. Because the tiles are on a circle, indices wrap around.

This suggests precomputing, for every index j, whether the edge (j, j+1 mod n) is "good" (different colors). Then the problem reduces to counting how many starting indices i have the next k-1 edges all good. That's a sliding-window / prefix-sum on a circular boolean array of edges.

## Refining the problem, round 2 thoughts
Construct good[j] = 1 if colors[j] != colors[(j+1)%n], else 0. For start i we need sum(good[i..i+k-2]) == k-1. To handle wrap-around simply duplicate good (good + good) and use prefix sums or a sliding window over that duplicated array; only consider starts i in [0, n-1].

Edge cases: k >= 3 per constraints, so k-1 >= 2. If k == n it's still fine: we check n-1 internal adjacent edges (we don't require the adjacency that crosses the group boundary since the group boundary is between the last and first in the selected group). Time complexity should be O(n), space O(n) (or O(1) if sliding window without duplication). Both are acceptable for n up to 1e5.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def alternatingGroups(self, colors: List[int], k: int) -> int:
        n = len(colors)
        # good[j] = 1 if edge (j, j+1 mod n) is alternating
        good = [1 if colors[i] != colors[(i + 1) % n] else 0 for i in range(n)]
        # duplicate to handle circular windows
        good2 = good + good
        # prefix sums for good2
        prefix = [0] * (len(good2) + 1)
        for i, v in enumerate(good2):
            prefix[i + 1] = prefix[i] + v

        need = k - 1  # number of adjacent edges inside a group
        ans = 0
        # check every starting index in original circle
        for start in range(n):
            if prefix[start + need] - prefix[start] == need:
                ans += 1
        return ans
```
- Notes:
  - Approach: Build an array marking which adjacent pairs differ, duplicate it to handle circular windows, and use prefix sums to query sums over windows of length k-1 quickly.
  - Time complexity: O(n) to build arrays and check all n starts.
  - Space complexity: O(n) for the good array (and its duplicate/prefix). One can reduce extra space to O(1) by using a sliding window sum over the duplicated good stream instead of prefix sums.