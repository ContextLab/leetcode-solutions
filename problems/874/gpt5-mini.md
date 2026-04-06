# [Problem 874: Walking Robot Simulation](https://leetcode.com/problems/walking-robot-simulation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to simulate a robot moving on an infinite grid following commands: turn left, turn right, or move forward k steps (k between 1 and 9). Some grid points are obstacles; if the robot would step onto an obstacle, that single step is blocked and the robot stops processing further steps of that command (but continues with next command). We must return the maximum squared Euclidean distance from origin reached at any time.

First thought: this is a straight simulation. Keep track of (x, y) and a facing direction. For each forward command, move one step at a time and check if the next cell is an obstacle. Use a set for obstacles (O(1) membership). Directions can be represented by a list of (dx, dy) vectors in a fixed order (e.g. north, east, south, west), and turning changes the index.

Edge details: obstacles can include (0,0) — that's fine since we don't check the starting cell for blocking; only stepping into a cell is blocked. Complexity will be dominated by the total number of single-step moves (sum of all movement commands), which is bounded by 9 * commands.length in worst case (<= 9e4 here), so simulation is efficient.

## Refining the problem, round 2 thoughts
- Representation: obstacles as a set of tuples (x,y) is simple and fast.
- Direction handling: let dirs = [(0,1),(1,0),(0,-1),(-1,0)] with index 0 = north. For -2 (turn left) we do dir = (dir + 3) % 4; for -1 (turn right) dir = (dir + 1) % 4. That mapping is concise and correct.
- Movement: for a forward k, loop i in range(k) and attempt to step to (x+dx, y+dy); if that coordinate is in obstacles, break; else update position and update max distance squared.
- Edge cases: obstacles empty; obstacle at origin handled naturally since we never check starting position; coordinates can be negative, storing tuples handles that fine.
- Complexity: time O(C + S) where C = len(commands) and S = total single-step moves (S <= 9 * C). Space O(M) for obstacles set where M = len(obstacles).

This approach is straightforward and optimal for given constraints.

## Attempted solution(s)
```python
from typing import List, Set, Tuple

class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        # Directions: north, east, south, west
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        d = 0  # start facing north (index 0)
        x = y = 0
        max_dist_sq = 0

        # Convert obstacle list to a set of tuples for O(1) lookup
        obs_set: Set[Tuple[int, int]] = {(ox, oy) for ox, oy in obstacles}

        for cmd in commands:
            if cmd == -2:  # turn left 90 degrees
                d = (d + 3) % 4
            elif cmd == -1:  # turn right 90 degrees
                d = (d + 1) % 4
            else:
                dx, dy = dirs[d]
                # move step by step
                for _ in range(cmd):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in obs_set:
                        # blocked by obstacle, stop this command
                        break
                    x, y = nx, ny
                    dist_sq = x*x + y*y
                    if dist_sq > max_dist_sq:
                        max_dist_sq = dist_sq

        return max_dist_sq
```
- Notes on the solution:
  - Approach: simulate the robot step-by-step, using a set for obstacles to check each candidate cell in O(1).
  - Correctness: handles turning and single-step movement, and respects obstacle blocking semantics (stops only the current command's movement when an obstacle is encountered).
  - Time complexity: O(C + S) where C = len(commands) and S = sum of forward steps (S <= 9 * C). Given constraints this is efficient.
  - Space complexity: O(M) to store obstacles (M = len(obstacles)).