# [Problem 3741: Minimum Distance Between Three Equal Elements II](https://leetcode.com/problems/minimum-distance-between-three-equal-elements-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I notice the distance for three indices i, j, k is abs(i-j)+abs(j-k)+abs(k-i). If I assume i <= j <= k, that becomes (j-i) + (k-j) + (k-i) = 2*(k-i). Interesting — the middle index j cancels out. So for any three equal elements the distance depends only on the outermost indices (first and third of the triple). That means to minimize distance for a particular value I should minimize the span between the 1st and 3rd occurrences. So scanning left-to-right and keeping track of recent occurrences for each value should work. I only need the index two steps back for each value (the earliest of the last three), not all occurrences.

## Refining the problem, round 2 thoughts
Thus for each value we can maintain the last two occurrence indices. When we see a new occurrence at index i and we already have at least two previous occurrences p0 (earlier) and p1 (more recent), the triple (p0, p1, i) has span i - p0 and distance 2*(i - p0). We then shift the stored last-two to (p1, i) and continue. This gives O(n) time and O(u) space where u is number of distinct values (<= n). Edge cases: values with fewer than 3 occurrences are ignored; if no value reaches 3 occurrences return -1. This is linear and memory efficient.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumDistance(self, nums: List[int]) -> int:
        last_two = {}  # val -> list of up to 2 most recent indices: [prev_prev, prev]
        ans = float('inf')
        for i, v in enumerate(nums):
            if v not in last_two:
                last_two[v] = [i]
            else:
                arr = last_two[v]
                if len(arr) == 1:
                    arr.append(i)
                else:
                    # arr[0] = prev_prev, arr[1] = prev
                    span = i - arr[0]
                    dist = 2 * span
                    if dist < ans:
                        ans = dist
                    # shift to keep the last two occurrences
                    arr[0], arr[1] = arr[1], i
        return -1 if ans == float('inf') else ans
```
- Notes:
  - Key observation: for indices a <= b <= c with same value, distance = 2*(c - a). So only the first and third occurrence matter for each triple.
  - We iterate once through nums, for each value track the last two indices; when a third (or further) occurrence appears compute distance using the index two steps back.
  - Time complexity: O(n), where n = len(nums).
  - Space complexity: O(u) for storing last two indices per distinct value (u <= n).