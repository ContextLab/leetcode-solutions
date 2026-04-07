# [Problem 2069: Walking Robot Simulation II](https://leetcode.com/problems/walking-robot-simulation-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The robot moves along the boundary of a width x height grid. Every time it would step out of bounds it turns 90° counterclockwise and keeps trying until it completes that step. Observing the motion, the robot always stays on the perimeter (border) cells and traverses them in a fixed cyclical order: along the bottom edge from left to right, then up the right edge, then along the top edge right-to-left, then down the left edge, and repeat.

So we can precompute the list of perimeter coordinates in that traversal order and treat the robot as moving along indices of that list. A step(num) is simply advancing the current index by num (mod perimeter length). For getDir(), direction depends on which segment of the perimeter the current index lies on; there's a special-case: when the robot is at the starting position (index 0) and it has completed at least one step in the past (i.e., total steps taken > 0), it should be facing "South" (this matches the turn pattern after a full loop).

This yields O(width+height) setup and O(1) per operation.

## Refining the problem, round 2 thoughts
Edge cases:
- width, height >= 2 so perimeter length is at least 4.
- step(num) can be large, so use modulo arithmetic to update index.
- Need to know whether the robot has ever moved a positive number of steps to decide the special direction at index 0. Keep a total_steps counter (unbounded integer in Python is fine).
- Compute the boundary list carefully to avoid duplicating corner cells.

Time complexity:
- Initialization: O(width + height)
- step / getPos / getDir: O(1)

Space complexity:
- O(perimeter) = O(width + height)

## Attempted solution(s)
```python
class Robot:
    def __init__(self, width: int, height: int):
        # Build the perimeter path in the order the robot will traverse:
        # bottom row left->right, right column bottom->top,
        # top row right->left, left column top->bottom (excluding corners duplicates)
        self.w = width
        self.h = height
        path = []
        # bottom edge (y = 0), x = 0..w-1
        for x in range(0, width):
            path.append((x, 0))
        # right edge (x = w-1), y = 1..h-1
        for y in range(1, height):
            path.append((width - 1, y))
        # top edge (y = h-1), x = w-2..0
        for x in range(width - 2, -1, -1):
            path.append((x, height - 1))
        # left edge (x = 0), y = h-2..1
        for y in range(height - 2, 0, -1):
            path.append((0, y))

        self.path = path
        self.L = len(path)  # perimeter length, equals 2*(w + h) - 4
        self.idx = 0        # current index in path
        self.total_steps = 0  # total steps ever taken (to detect full-loop special case)

    def step(self, num: int) -> None:
        if self.L == 0:
            return
        self.total_steps += num
        self.idx = (self.idx + num) % self.L

    def getPos(self) -> [int, int]:
        x, y = self.path[self.idx]
        return [x, y]

    def getDir(self) -> str:
        # Special case: if at starting cell after having moved >0 steps, robot faces South
        if self.idx == 0 and self.total_steps > 0:
            return "South"

        # Determine which edge segment the current index is on
        # indices:
        # 0 .. (w-1) - 1        -> bottom edge -> East
        # (w-1) .. (w-1 + h-1) - 1 -> right edge -> North
        # ... next (w-1) -> top edge -> West
        # remaining -> left edge -> South
        seg1 = self.w - 1
        seg2 = seg1 + (self.h - 1)
        seg3 = seg2 + (self.w - 1)
        # seg4 is implicit remainder

        if self.idx < seg1:
            return "East"
        elif self.idx < seg2:
            return "North"
        elif self.idx < seg3:
            return "West"
        else:
            return "South"
```
- Notes:
  - We precompute the perimeter path in traversal order; moving is an index shift modulo path length.
  - We maintain total_steps to distinguish the initial facing ("East" at start index 0) from the facing after a full loop (index 0 but should be "South").
  - Time: O(width + height) init, O(1) per method call.
  - Space: O(width + height) for the path list.