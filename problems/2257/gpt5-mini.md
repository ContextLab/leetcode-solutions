# [Problem 2257: Count Unguarded Cells in the Grid](https://leetcode.com/problems/count-unguarded-cells-in-the-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count cells that are empty and not seen by any guard along the four cardinal directions, with sight blocked by walls or other guards. The grid size m*n can be up to 1e5 cells (product), so building an explicit m x n grid is fine. A natural idea is to mark guards and walls on the grid, then simulate visibility by "sweeping" in each of the four directions (left->right, right->left for rows; top->bottom, bottom->top for columns). During a sweep we keep a flag that says whether we've seen a guard since the last wall/guard; if true we mark empty cells as guarded. This is a common approach for visibility on grids when obstructions are only in straight lines.

I should be careful not to mark occupied cells (guards/walls) as guarded, and ensure that encountering a guard resets/affects visibility correctly (a guard blocks sight beyond it and also provides sight starting from its own position). Doing sweeps in both directions ensures both sides' guard visibilities are captured.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Represent grid with integers: 0 = empty, 1 = guard, 2 = wall, 3 = guarded-empty.
- When sweeping:
  - On encountering a wall, visibility stops (reset seen flag).
  - On encountering a guard, do not mark it as guarded (it's occupied) but set seen = True so cells after it get marked (until next wall or guard).
  - When a cell is empty and seen is True, mark it guarded (set to 3).
- Sweep left->right and right->left for each row, and top->bottom and bottom->top for each column to capture all directions.
- After sweeps, count cells still 0 (empty and unguarded).
- Complexity: O(m*n) time, O(m*n) space (but m*n ≤ 1e5 so okay).
- Implementation details: use simple nested loops, ensure we only change empty cells to guarded, preserve guard/wall cells.

This approach is straightforward and efficient given constraints.

## Attempted solution(s)
```python
class Solution:
    def countUnguarded(self, m: int, n: int, guards: list[list[int]], walls: list[list[int]]) -> int:
        # 0 = empty, 1 = guard, 2 = wall, 3 = guarded empty
        grid = [[0] * n for _ in range(m)]
        
        for r, c in guards:
            grid[r][c] = 1
        for r, c in walls:
            grid[r][c] = 2
        
        # Sweep rows left -> right
        for r in range(m):
            seen = False
            for c in range(n):
                cell = grid[r][c]
                if cell == 2:  # wall
                    seen = False
                elif cell == 1:  # guard
                    seen = True
                elif seen and cell == 0:
                    grid[r][c] = 3
        
        # Sweep rows right -> left
        for r in range(m):
            seen = False
            for c in range(n - 1, -1, -1):
                cell = grid[r][c]
                if cell == 2:
                    seen = False
                elif cell == 1:
                    seen = True
                elif seen and cell == 0:
                    grid[r][c] = 3
        
        # Sweep columns top -> bottom
        for c in range(n):
            seen = False
            for r in range(m):
                cell = grid[r][c]
                if cell == 2:
                    seen = False
                elif cell == 1:
                    seen = True
                elif seen and cell == 0:
                    grid[r][c] = 3
        
        # Sweep columns bottom -> top
        for c in range(n):
            seen = False
            for r in range(m - 1, -1, -1):
                cell = grid[r][c]
                if cell == 2:
                    seen = False
                elif cell == 1:
                    seen = True
                elif seen and cell == 0:
                    grid[r][c] = 3
        
        # Count unguarded empty cells
        ans = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 0:
                    ans += 1
        return ans
```
- Notes:
  - Approach: mark guards/walls, then perform four directional sweeps to mark empty cells that are guarded.
  - Time complexity: O(m * n) — we visit each cell a constant number of times (4 sweeps + final count).
  - Space complexity: O(m * n) for the grid representation (feasible since m * n ≤ 1e5).
  - Implementation detail: always check grid cell value and only convert empty cells (0) to guarded (3); do not overwrite guard (1) or wall (2) cells.