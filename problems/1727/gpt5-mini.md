# [Problem 1727: Largest Submatrix With Rearrangements](https://leetcode.com/problems/largest-submatrix-with-rearrangements/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share my internal stream-of-consciousness, but here's a concise summary of the immediate approach: compute for each column the number of consecutive 1s ending at each row (a heights array). For each row, those heights represent column heights if we consider submatrices that end at this row. Since we may reorder columns arbitrarily, sort the heights in descending order to place taller columns together; then for each possible width w (taking the first w sorted heights) the maximal height is the w-th value, so area = height * w. Track the maximum area across all rows.

## Refining the problem, round 2 thoughts
- We must update heights row-by-row: heights[j] increments when matrix[i][j] == 1, resets to 0 otherwise.
- Sorting the heights for every row simulates optimal column rearrangement for that row.
- Complexity: sorting each row leads to O(m * n log n) time (m rows, n columns). Given m * n <= 1e5 this is acceptable. An alternative is counting sort per row using the bounded height range [0..m] to achieve O(m*n) time.
- Edge cases: single row, single column, all zeros, all ones — handled naturally by the method.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        m, n = len(matrix), len(matrix[0])
        heights = [0] * n
        max_area = 0

        for i in range(m):
            # update heights for row i
            for j in range(n):
                if matrix[i][j] == 1:
                    heights[j] += 1
                else:
                    heights[j] = 0

            # sort heights descending to simulate optimal column rearrangement
            sorted_heights = sorted(heights, reverse=True)

            # compute best area using first k columns for k=1..n
            for k, h in enumerate(sorted_heights):
                area = h * (k + 1)
                if area > max_area:
                    max_area = area

        return max_area
```
- Notes:
  - Approach: For each row treat column values as heights of consecutive 1s ending at that row. Sorting heights descending models reordering columns. For each possible width w, area = w * (w-th largest height).
  - Time complexity: O(m * n log n) using Python's sort for each of m rows. With constraints m * n <= 1e5, this is acceptable. Using counting sort per row could reduce to O(m * n).
  - Space complexity: O(n) additional space for the heights and the sorted list.
  - Implementation details: We update heights in-place per row, then take a sorted copy (or new list) descending and iterate to compute areas. This avoids modifying the original matrix.