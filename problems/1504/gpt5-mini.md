# [Problem 1504: Count Submatrices With All Ones](https://leetcode.com/problems/count-submatrices-with-all-ones/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count all submatrices made of only 1s. Brute force would enumerate all possible top-left and bottom-right corners and check if all ones — that's O(m^2 * n^2) checks and too slow for 150x150 in the worst case. Another classic idea: for each row treat it like the base of a histogram where heights[j] is the number of consecutive ones up to this row in column j. Using these heights, count how many submatrices end at each cell in that row.

A straightforward method: for each row and for each column j, expand leftwards keeping track of the minimum height seen and add that minimum to the answer. That is O(n^2) per row -> O(m * n^2) overall, which is acceptable for 150*150*150 ~ 3.4M operations, but we can do better.

I recall a monotonic stack technique that processes each row in O(n) time by computing contributions of each column to submatrices ending at that column (similar to sum of subarray minimums logic). I'll use that to get O(m * n) time.

## Refining the problem, round 2 thoughts
Refine the histogram approach: compute heights[j] = number of consecutive 1s ending at current row at column j. For a fixed row, we want for each column j the number of all-1 submatrices that end at row (as bottom) and end at column j (as right). Using a monotonic increasing stack we can find the previous column with smaller height (prev_less). Then the number of new submatrices where right boundary is j can be expressed in terms of heights[j], the width (j - prev_less) and any counts already computed at prev_less. The recurrence is:

dp[j] = heights[j] * (j - prev_less) + (dp[prev_less] if prev_less != -1 else 0)

Summing dp[j] over j and then over rows gives the total. Handle zeros naturally (heights zero give dp zero). Complexity O(m * n) time, O(n) extra space. Edge cases: single row/column, all zeros.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numSubmat(self, mat: List[List[int]]) -> int:
        if not mat or not mat[0]:
            return 0
        m, n = len(mat), len(mat[0])
        heights = [0] * n
        total = 0

        for i in range(m):
            # update histogram heights for this row as bottom
            for j in range(n):
                if mat[i][j] == 1:
                    heights[j] += 1
                else:
                    heights[j] = 0

            # use monotonic increasing stack to compute dp[j]: number of submatrices
            # with bottom-right corner at (i, j)
            stack = []
            dp = [0] * n
            for j in range(n):
                # pop indices with heights >= current to find previous less
                while stack and heights[stack[-1]] >= heights[j]:
                    stack.pop()
                if not stack:
                    prev = -1
                    dp[j] = heights[j] * (j - prev)
                else:
                    prev = stack[-1]
                    dp[j] = dp[prev] + heights[j] * (j - prev)
                stack.append(j)
                total += dp[j]

        return total
```
- Notes:
  - Approach: For each row treat columns as a histogram of consecutive ones; use a monotonic increasing stack to compute, in O(n) per row, how many all-1 submatrices end at each column for that row. Sum over columns and rows.
  - Time complexity: O(m * n), where m is number of rows and n is number of columns.
  - Space complexity: O(n) additional space for heights, stack, and dp arrays.
  - Implementation details: heights[j] is reset to 0 when mat[i][j] == 0. Using >= when popping ensures we correctly group equal heights and avoid double counting. The dp recurrence aggregates the number of rectangles that can extend from previous smaller heights.