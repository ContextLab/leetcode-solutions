# [Problem 2975: Maximum Square Area by Removing Fences From a Field](https://leetcode.com/problems/maximum-square-area-by-removing-fences-from-a-field/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the largest possible square side length achievable by removing some internal fences. Removing fences lets me merge adjacent strips, so any side length that equals the distance between some pair of horizontal fence lines (including the boundary fences at 1 and m) can be realized as a height; similarly any distance between some pair of vertical fence lines (including 1 and n) can be realized as a width. Therefore we need the largest value s such that s appears as a difference between two horizontal fence coordinates and also as a difference between two vertical fence coordinates. So compute all pairwise differences for horizontals and verticals (including boundaries), intersect them, and take the maximum. If none, return -1. Complexity: O(k^2) where k <= ~602 -> fine.

## Refining the problem, round 2 thoughts
- Include the boundary fences (1 and m for horizontals, 1 and n for verticals) because they cannot be removed.
- Differences should be positive (distinct fence positions).
- Arrays length <= 600 so computing all pairwise differences (approx 360k pairs) is fine.
- Alternative: compute all possible gap lengths by considering sorted lists and pairwise differences; could speed up by generating only differences from sorted arrays, but full nested loops are simple and acceptable.
- Edge cases: if intersection is empty -> return -1. If maximum side s is found, return s^2 % (1e9+7). Make sure to use integer modulo and handle large s (up to ~1e9) -> s^2 fits in Python int anyway but take modulo.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxSquare(self, m: int, n: int, hFences: List[int], vFences: List[int]) -> int:
        MOD = 10**9 + 7

        # include the boundary fences which cannot be removed
        hs = [1] + sorted(hFences) + [m]
        vs = [1] + sorted(vFences) + [n]

        # compute all positive differences for horizontals and verticals
        h_diffs = set()
        for i in range(len(hs)):
            for j in range(i+1, len(hs)):
                h_diffs.add(hs[j] - hs[i])

        v_diffs = set()
        for i in range(len(vs)):
            for j in range(i+1, len(vs)):
                v_diffs.add(vs[j] - vs[i])

        # intersection of possible side lengths
        common = h_diffs & v_diffs
        if not common:
            return -1

        s = max(common)
        return (s * s) % MOD
```
- Approach: Augment fence coordinate lists with the two immutable boundary fences, compute all pairwise distances (differences) within each augmented list, and find the maximum length present in both sets (horizontal and vertical). Square that length and take modulo 1e9+7.
- Time complexity: O(H^2 + V^2) where H = len(hFences)+2, V = len(vFences)+2. With H,V <= 602 this is ~O(3.6e5) operations per side, easily within limits.
- Space complexity: O(H^2 + V^2) in the worst-case for the sets of differences (practically much smaller).
- Important details: include boundaries 1 and m / 1 and n; ensure only positive differences considered by using j > i. If no common differences, return -1.