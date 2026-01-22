# [Problem 874: Walking Robot Simulation](https://leetcode.com/problems/walking-robot-simulation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to simulate the robot on an infinite grid. Commands are either turns (-2 left, -1 right) or small forward moves (1..9). There are obstacles that block movement if the robot would step onto them; then it stays in the previous cell and continues with the next command. The goal is to return the maximum squared Euclidean distance from origin encountered.

A straightforward simulation seems fine: keep the robot's position and direction, process each command. For movement commands, move one step at a time checking for obstacles. Obstacle lookups should be O(1), so store obstacles in a hash set (tuples). Directions can be represented by an array of dx/dy and a direction index. Constraints (commands length up to 1e4, each move up to 9 steps) make per-step simulation acceptable.

Edge-case: obstacle at (0,0) — important: robot starts at (0,0) and should ignore an obstacle at origin until it leaves; but our simulation only checks obstacles when stepping into a cell, so starting on (0,0) is fine and later attempts to re-enter (0,0) will be blocked normally.

## Refining the problem, round 2 thoughts
- Represent directions in order [north, east, south, west] with dx,dy arrays and update the direction index on turns:
  - -2 (left): dir = (dir + 3) % 4
  - -1 (right): dir = (dir + 1) % 4
- Convert obstacles to a set of tuples for O(1) containment checks.
- For each forward command k, do k single-step moves; if the cell ahead is an obstacle, stop processing this movement command and proceed to the next command.
- Keep track of max(x*x + y*y) after each successful step.
- Complexity: commands length up to 1e4 and each command moves at most 9 steps -> at most ~9e4 steps; obstacles up to 1e4. Using a set for obstacles yields efficient membership checks.
- Alternative approaches (e.g., precomputing nearest obstacle in each direction) are unnecessary here because forward steps are small; the simple simulation is clear and efficient for constraints.
- Make sure to handle negative coordinates correctly when storing obstacles (use tuple of ints).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        # Convert obstacles to a set of tuples for O(1) lookup
        obs = set(map(tuple, obstacles))
        
        # Directions: north, east, south, west
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        d = 0  # start facing north
        x = y = 0
        max_dist_sq = 0
        
        for cmd in commands:
            if cmd == -2:  # turn left 90 degrees
                d = (d + 3) % 4
            elif cmd == -1:  # turn right 90 degrees
                d = (d + 1) % 4
            else:
                dx, dy = dirs[d]
                for _ in range(cmd):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in obs:
                        # obstacle blocks further movement for this command
                        break
                    x, y = nx, ny
                    dist_sq = x * x + y * y
                    if dist_sq > max_dist_sq:
                        max_dist_sq = dist_sq
        
        return max_dist_sq
```
- Notes:
  - Approach: Straightforward simulation. Use a set of obstacle coordinates for constant-time checks, maintain direction index and position, and step one unit at a time for move commands.
  - Time complexity: O(C + S) where C is number of commands and S is total unit steps executed. Given each command moves at most 9 steps, S <= 9 * C, so effectively O(C + |obstacles|) for preprocessing the obstacle set. With constraints this is efficient.
  - Space complexity: O(|obstacles|) for the obstacle set.
  - Implementation detail: Using tuple coordinates (x,y) in a Python set handles negative coordinates and large ranges correctly. The special-case note about an obstacle at (0,0) is naturally handled because we only check obstacles when stepping into cells, not for the starting cell.