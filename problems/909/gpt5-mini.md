# [Problem 909: Snakes and Ladders](https://leetcode.com/problems/snakes-and-ladders/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a shortest-path / minimum-moves problem on a board where each die roll moves you up to 6 squares, and some squares teleport you to another square (snakes or ladders). That suggests BFS over board squares (each square is a node, edges to next 1..6 squares, with teleport applied). The main non-trivial piece is mapping the 1..n^2 labels to (row, col) indices because of the boustrophedon labeling (rows alternate direction and numbering starts from the bottom-left). Also must be careful to only follow at most one teleport per die roll (i.e., if target has a board value != -1, move to that destination and stop). Mark visited when enqueuing to avoid revisiting nodes and infinite loops with snakes. BFS will give minimum dice rolls.

## Refining the problem, round 2 thoughts
- Need a robust mapping function label -> (r, c). For label s (1-based): quotient q = (s-1)//n determines which "horizontal band" (counting from bottom, q=0 is bottom row). Row r = n-1 - q. Column c = (s-1)%n if q is even (left-to-right), otherwise c = n-1 - ((s-1)%n) (right-to-left).
- BFS edge generation: from current square curr, try next in range(curr+1, min(curr+6, n^2)+1). For each next, map to (r,c); if board[r][c] != -1, set dest = board[r][c], else dest = next.
- Mark visited when pushing into queue (not when popping) to avoid duplicate pushes.
- If we reach n^2, return level (number of dice rolls).
- Complexity: O(n^2) nodes * up to 6 edges => O(n^2) time, O(n^2) space for visited and queue.
- Edge cases: unreachable end (due to cycles or blocked by snakes) -> return -1. n up to 20 so n^2 manageable.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        target = n * n

        def label_to_pos(s: int):
            # s is 1-based label
            q, r_mod = divmod(s - 1, n)
            row = n - 1 - q
            if q % 2 == 0:
                col = r_mod
            else:
                col = n - 1 - r_mod
            return row, col

        visited = set()
        q = deque()
        q.append((1, 0))  # (square label, moves)
        visited.add(1)

        while q:
            curr, moves = q.popleft()
            if curr == target:
                return moves
            for step in range(1, 7):
                nxt = curr + step
                if nxt > target:
                    break
                r, c = label_to_pos(nxt)
                if board[r][c] != -1:
                    dest = board[r][c]
                else:
                    dest = nxt
                if dest == target:
                    return moves + 1
                if dest not in visited:
                    visited.add(dest)
                    q.append((dest, moves + 1))
        return -1
```
- Notes:
  - Approach: standard BFS on integer-labeled squares with at most 6 outgoing edges per node and a mapping function to translate labels to board coordinates. Teleports (snakes/ladders) are applied immediately for the destination of a die roll, and chaining is not performed beyond one teleport per roll.
  - Time complexity: O(n^2) because we visit each square at most once and examine at most 6 neighbors per square.
  - Space complexity: O(n^2) for the visited set and queue in the worst case.
  - Implementation details: mark a square visited when enqueuing to prevent multiple enqueues for the same square; return early if we reach target while generating neighbors to avoid extra work.