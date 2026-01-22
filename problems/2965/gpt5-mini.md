# [Problem 2965: Find Missing and Repeated Values](https://leetcode.com/problems/find-missing-and-repeated-values/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given an n x n grid containing numbers from 1..n^2 with exactly one value repeated twice and exactly one value missing. That sounds like the standard "find duplicate and missing" problem but on a flattened grid. The simplest idea is to count occurrences of each number (frequency array or dictionary) while scanning the grid once. Then find which number has frequency 2 (the repeated one) and which has frequency 0 (the missing one).

Other approaches: use arithmetic (expected sum and expected sum of squares) or XOR-based tricks to get O(1) extra space — possible here, but counting is straightforward and safe given n^2 ≤ 2500.

## Refining the problem, round 2 thoughts
- Use a frequency array of size n*n + 1 (index 1..n^2) and scan every element in the grid once.
- After building counts, iterate from 1 to n^2 to find the value with count 2 (a) and count 0 (b).
- Edge cases: none special because constraints guarantee exactly one missing and exactly one repeated value.
- Time complexity: O(n^2). Space complexity: O(n^2) for the counts array (which is fine for n ≤ 50).
- Alternative with constant extra space: use sum and sum of squares or XOR technique, but counting is simpler and clearer.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findMissingAndRepeatedValues(self, grid: List[List[int]]) -> List[int]:
        n = len(grid)
        total = n * n
        counts = [0] * (total + 1)  # index 0 unused; use 1..total

        for row in grid:
            for val in row:
                counts[val] += 1

        repeated = -1
        missing = -1
        for x in range(1, total + 1):
            if counts[x] == 2:
                repeated = x
            elif counts[x] == 0:
                missing = x
            # early exit if both found
            if repeated != -1 and missing != -1:
                break

        return [repeated, missing]
```
- Approach: Build a frequency array for values 1..n^2 by scanning the grid once. Then scan the frequency array to identify the value appearing twice (repeated) and the value appearing zero times (missing).
- Time complexity: O(n^2) to scan the n x n grid and O(n^2) to scan the counts (overall O(n^2)).
- Space complexity: O(n^2) for the counts array (size n^2 + 1). Given n ≤ 50, this is small and practical.
- Implementation detail: Use index range 1..n^2 for clarity; index 0 is unused. The constraints guarantee exactly one repeated and one missing, so the final result always exists.