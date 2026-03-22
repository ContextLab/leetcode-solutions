# [Problem 1886: Determine Whether Matrix Can Be Obtained By Rotation](https://leetcode.com/problems/determine-whether-matrix-can-be-obtained-by-rotation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check whether rotating mat by 0, 90, 180, or 270 degrees (clockwise) can make it equal to target. Since n is at most 10, a brute-force approach that explicitly rotates and compares is fine. Rotating a matrix 90° clockwise can be done by mapping position (i, j) -> (j, n-1-i), or by transposing and then reversing each row. I'll just build a new rotated matrix each time and compare to target; if any match, return True. Watch for the case where mat is already equal to target (0 rotations). Complexity will be small (O(n^2) per rotation).

## Refining the problem, round 2 thoughts
Refinements / alternatives:
- We can rotate in-place (transpose + reverse rows) to avoid extra space, but building a new matrix is simpler and straightforward given the small constraints.
- Edge case: n = 1 -> just compare single elements.
- Stop early as soon as a rotation matches target.
- Time complexity: up to 4 * O(n^2) comparisons/constructs. Space complexity: O(n^2) extra for a single rotated matrix (or O(1) extra if done in-place).
- Use Python list equality for matrix comparison (works for nested lists).

## Attempted solution(s)
```python
class Solution:
    def findRotation(self, mat: list[list[int]], target: list[list[int]]) -> bool:
        n = len(mat)
        
        def rotate90(matrix):
            # Return new matrix rotated 90 degrees clockwise
            return [[matrix[n - 1 - j][i] for j in range(n)] for i in range(n)]
        
        current = mat
        for _ in range(4):
            if current == target:
                return True
            current = rotate90(current)
        return False
```
- Approach: try up to 4 rotations (including 0 rotations), building a new matrix for each 90° clockwise rotation using index mapping (i, j) <- (n-1-j, i). Compare with target using list equality; return True if any match.
- Time complexity: O(4 * n^2) = O(n^2) since constants drop. Each rotation and comparison is O(n^2).
- Space complexity: O(n^2) for the temporary rotated matrix each iteration (can be reduced to O(1) with in-place rotation).
- Implementation details: function is implemented as LeetCode expects within class Solution and uses Python list comprehensions for clarity.