# [Problem 773: Sliding Puzzle](https://leetcode.com/problems/sliding-puzzle/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I’m sorry — I can’t share internal stream-of-consciousness. I can, however, provide a concise, high-level summary of the approach:

- Represent the 2x3 board as a flat string of length 6 (row-major), e.g. "123450".
- Use breadth-first search (BFS) from the initial configuration to the target "123450", generating neighbors by swapping the '0' with its valid adjacent positions.
- Keep a visited set to avoid revisiting states. BFS returns the minimum number of moves when the target is first reached.

## Refining the problem, round 2 thoughts
Summary of refinements, edge cases, and complexity considerations (concise):
- The board has at most 6! = 720 possible states, so BFS is efficient and safe.
- Precompute adjacency (valid swap indices) for each of the 6 positions on a 2x3 board to generate neighbors quickly.
- Edge case: if the start equals target, return 0 immediately.
- Time complexity: O(N) where N ≤ 720 (practically O(1) for this fixed-size puzzle); each state processes up to 4 neighbors and swapping is O(6) = O(1). Space complexity: O(N) for visited states and queue.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        # Flatten board to a string representation
        start = ''.join(str(num) for row in board for num in row)
        target = "123450"
        if start == target:
            return 0

        # Adjacency list for each index in the flattened 2x3 board
        neighbors = {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 5],
            3: [0, 4],
            4: [1, 3, 5],
            5: [2, 4],
        }

        def swap(s: str, i: int, j: int) -> str:
            lst = list(s)
            lst[i], lst[j] = lst[j], lst[i]
            return ''.join(lst)

        q = deque([(start, 0)])  # (state, moves)
        visited = {start}

        while q:
            state, moves = q.popleft()
            zero_idx = state.index('0')
            for nei in neighbors[zero_idx]:
                new_state = swap(state, zero_idx, nei)
                if new_state == target:
                    return moves + 1
                if new_state not in visited:
                    visited.add(new_state)
                    q.append((new_state, moves + 1))
        return -1
```
- Notes:
  - Approach: BFS on the state graph where nodes are board configurations and edges are valid swaps with the empty tile (0). BFS guarantees the minimum moves.
  - Time complexity: O(N) where N ≤ 720 (since there are 6! permutations), each step does O(1) work to generate neighbors and swap; practically constant time for this fixed puzzle size.
  - Space complexity: O(N) for the visited set and queue.