# [Problem 48: Rotate Image](https://leetcode.com/problems/rotate-image/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to rotate an n x n matrix by 90 degrees clockwise in-place. First thought: one simple way is to create a new matrix and fill rotated positions, but that's not allowed (must be in-place). I recall common in-place approaches: (1) transpose the matrix and then reverse each row, or (2) perform layer-by-layer four-way swaps (move four elements at a time around the cycle). Both are O(n^2) time and use O(1) extra space. Transpose + reverse is concise and easy to implement correctly. For n=1 nothing changes. Need to be careful with indices during transpose (only swap for j > i).

## Refining the problem, round 2 thoughts
Refine to choose transpose + row-reverse approach because it's clear and minimal code, less error-prone than manual four-way swaps. Edge cases: n=1 or matrix with negative numbers — no special handling required. Complexity: we will touch each element a constant number of times, so O(n^2) time. Extra space: only O(1) extra (a few temporaries for swaps). Confirm correctness: transposing converts rows to columns; reversing each row then maps the transposed matrix to the clockwise-rotated matrix. Alternative is the layer-by-layer cycle swap which also achieves O(n^2) time and O(1) space; either is acceptable.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        # Step 1: transpose (swap matrix[i][j] with matrix[j][i] for j > i)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # Step 2: reverse each row
        for i in range(n):
            matrix[i].reverse()
```

- Notes about the solution approach, complexity, and implementation details:
  - Approach: Transpose the matrix in-place (swap symmetric elements across the main diagonal), then reverse each row. This sequence results in a 90-degree clockwise rotation.
  - Time complexity: O(n^2) — transposing touches about n(n-1)/2 elements and reversing touches n^2 elements overall, still O(n^2).
  - Space complexity: O(1) extra space — swaps are done in-place using temporary storage in Python tuple assignment; no additional matrix is allocated.
  - Correctness: For every element originally at (i, j), after transpose it goes to (j, i); reversing rows moves (j, i) to (j, n-1-i), which is the correct final position for a clockwise rotation.
  - Implementation detail: Using matrix[i].reverse() is efficient and clear; if desired, one could also swap elements pairwise while reversing to be explicit.