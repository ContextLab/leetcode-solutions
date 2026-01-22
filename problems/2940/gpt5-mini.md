# [Problem 2940: Find Building Where Alice and Bob Can Meet](https://leetcode.com/problems/find-building-where-alice-and-bob-can-meet/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can only move to the right (i < j) and only to strictly taller buildings (heights[i] < heights[j]). For two people at a and b, any meeting building k must satisfy k >= max(a, b) (they can't move left), and for k > a we need heights[k] > heights[a], for k > b we need heights[k] > heights[b]. If a == b they can already meet at a. Otherwise k > a and k > b so both conditions reduce to heights[k] > max(heights[a], heights[b]). So the problem reduces to: for each query (a, b), let L = max(a, b) and H = max(heights[a], heights[b]) (and if a==b return a). Find the smallest index k >= L with heights[k] > H. Return -1 if none.

So we need a data structure that can, given a starting index L and threshold H, find the leftmost index >= L whose value > H. A segment tree storing maximums (and doing a left-first search) is a natural fit — we can skip whole segments whose maximum <= H.

## Refining the problem, round 2 thoughts
- Edge cases: a == b (answer is a). If L is at or beyond n-1, ensure bounds handled. heights values are positive so sentinel values outside n can be safely 0.
- Alternative structures: binary indexed tree won't help because we need first index with value > H; we need range maximum and leftmost index search => segment tree or sparse table with binary searching segments. Also could compress values + Fenwick for next greater by value, but segment tree is simplest and O(log n) per query.
- Complexity target: build tree O(n), each query O(log n) time in worst case. With n,q up to 5e4 this is fine.
- Implementation detail: build a segment tree on next power-of-two size to simplify recursion and bounds.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findBuildingWhereAliceAndBobCanMeet(self, heights: List[int], queries: List[List[int]]) -> List[int]:
        n = len(heights)
        # Build segment tree for range maximums (complete binary tree of size = next power of two)
        size = 1
        while size < n:
            size <<= 1
        # tree indices: 1..(2*size-1)
        tree = [0] * (2 * size)
        for i in range(n):
            tree[size + i] = heights[i]
        for i in range(size - 1, 0, -1):
            tree[i] = max(tree[2 * i], tree[2 * i + 1])

        # recursive helper: find leftmost index >= pos with value > H
        def find_first_greater(idx: int, l: int, r: int, pos: int, H: int) -> int:
            # If segment entirely before pos, or max <= H, no candidate
            if r < pos or tree[idx] <= H:
                return -1
            if l == r:
                # l is within [0, size-1], ensure it's a real index
                return l if l < n else -1
            mid = (l + r) // 2
            # try left child first to get leftmost
            left = find_first_greater(idx * 2, l, mid, pos, H)
            if left != -1:
                return left
            return find_first_greater(idx * 2 + 1, mid + 1, r, pos, H)

        ans = []
        for a, b in queries:
            if a == b:
                ans.append(a)
                continue
            L = max(a, b)
            H = max(heights[a], heights[b])
            idx = find_first_greater(1, 0, size - 1, L, H)
            ans.append(idx if idx != -1 and idx < n else -1)
        return ans
```
- Notes on the approach:
  - We reduced each query to a range-first-greater-than-threshold query: find the smallest index k >= L with heights[k] > H (L = max(a,b), H = max(height[a], height[b])). If a == b we return a immediately.
  - Segment tree stores maximum for each node; when querying, if a node's max <= H or the node range is completely left of pos, we skip it. Otherwise we recurse left-first to obtain the leftmost valid index.
- Complexity:
  - Building the segment tree: O(n).
  - Each query: O(log n) in the average/worst-case recursion depth (each level we descend at most to two children but we short-circuit segments whose max <= H), so overall O(q log n).
  - Space: O(size) = O(n) for the segment tree.