# [Problem 3160: Find the Number of Distinct Colors Among the Balls](https://leetcode.com/problems/find-the-number-of-distinct-colors-among-the-balls/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have limit+1 balls labelled 0..limit, but limit can be up to 1e9 so we cannot allocate an array of that size. However, number of queries n ≤ 1e5, so we only ever touch at most n distinct balls (those that appear in queries). Each query sets ball x to color y (overwriting any previous color). After each operation we need the number of distinct colors among all colored balls (uncolored is not a color). This suggests maintaining the current color of each referenced ball and tracking counts of each color. On an update, decrease the count of the previous color (if any) and increase the count of the new color; if a color's count goes to zero it no longer counts as distinct.

A trivial detail: if a query sets the ball to the same color it already has, nothing changes. Use hash maps (dicts) keyed by label->color and color->count. This yields O(1) amortized per query.

## Refining the problem, round 2 thoughts
- Data structures: label_to_color: dict[int,int], color_count: dict[int,int], and an integer distinct_count to avoid repeatedly computing len(color_count).
- Edge cases: a ball being colored for first time (no previous), re-coloring to same color (skip), re-coloring from one color to another (decrement old, increment new), colors that reach zero count should be removed/ignored.
- Complexity: each query does O(1) dictionary operations amortized; overall O(n) time. Space O(k) where k is number of distinct balls referenced and distinct colors used, both ≤ n.
- The large limit is irrelevant except to note we must not use arrays of size limit.

## Attempted solution(s)
```python
from typing import List
from collections import defaultdict

class Solution:
    def distinctColors(self, limit: int, queries: List[List[int]]) -> List[int]:
        # label -> current color (only for labels that have been colored)
        label_to_color = {}
        # color -> number of balls currently with this color
        color_count = defaultdict(int)
        distinct = 0
        res = []
        
        for x, y in queries:
            prev = label_to_color.get(x)
            # if same color as before, no change
            if prev == y:
                res.append(distinct)
                continue
            
            # remove previous color count if there was one
            if prev is not None:
                color_count[prev] -= 1
                if color_count[prev] == 0:
                    # color disappears
                    del color_count[prev]
                    distinct -= 1
            
            # add/increment new color
            if color_count.get(y, 0) == 0:
                distinct += 1
            color_count[y] += 1
            
            # set the ball's color
            label_to_color[x] = y
            res.append(distinct)
        
        return res
```
- Approach: Maintain two hash maps: label_to_color and color_count. For each query, if the ball's previous color exists and differs from the new color, decrement previous color count and remove it if it reaches zero; then increment the new color's count (and increase distinct count if it was 0). If assigning same color again, skip changes. Append the current distinct count after each query.
- Time complexity: O(n) amortized for n queries.
- Space complexity: O(m) where m ≤ n is number of distinct labels/colors we have seen.