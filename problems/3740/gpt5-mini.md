# [Problem 3740: Minimum Distance Between Three Equal Elements I](https://leetcode.com/problems/minimum-distance-between-three-equal-elements-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need triples of distinct indices i, j, k with the same value, and compute abs(i-j)+abs(j-k)+abs(k-i). For a fixed value, its occurrences have indices; the tuple distance only depends on those indices. If we sort three indices a <= b <= c, then the sum is (b-a) + (c-b) + (c-a) = 2*(c-a). So the distance depends only on the outer two indices (min and max) among the three. Therefore for a given value we want three occurrences whose outer indices are as close as possible. That suggests scanning each value's occurrence list and taking every window of size 3 and computing 2*(pos[i+2] - pos[i]). Collect minimum across all values. If no value appears at least 3 times, answer is -1.

## Refining the problem, round 2 thoughts
We should:
- Build a mapping from value -> list of indices (in increasing order by construction if we append while iterating).
- For each list with length >= 3, check consecutive triples (i, i+1, i+2) since these minimize c-a for any triple inside the list. No need to check non-consecutive triples.
- Keep global minimum, return -1 if unchanged.
Edge cases: arrays shorter than 3, values never repeated 3 times. Complexity: building index lists O(n), scanning windows O(n) total across all values. Space O(n) for storing indices.

## Attempted solution(s)
```python
from collections import defaultdict
from typing import List

class Solution:
    def minDistance(self, nums: List[int]) -> int:
        # Map each number to the list of its indices
        pos = defaultdict(list)
        for i, v in enumerate(nums):
            pos[v].append(i)
        
        ans = float('inf')
        # For each value with at least 3 occurrences, check consecutive triples
        for indices in pos.values():
            if len(indices) < 3:
                continue
            # Sliding window of size 3: distance = 2 * (indices[i+2] - indices[i])
            for i in range(len(indices) - 2):
                dist = 2 * (indices[i+2] - indices[i])
                if dist < ans:
                    ans = dist
        
        return -1 if ans == float('inf') else ans
```
- Approach: collect indices per value, for each value consider consecutive triples because distance reduces to 2*(max_index - min_index) and the smallest span for three occurrences is among consecutive occurrences.
- Time complexity: O(n) to build lists + O(n) to scan windows across all values => O(n) total (n = len(nums)).
- Space complexity: O(n) for storing indices in the dictionary.