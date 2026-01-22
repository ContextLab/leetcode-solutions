# [Problem 37: Sudoku Solver](https://leetcode.com/problems/sudoku-solver/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a classic backtracking problem: fill each '.' with digits '1'..'9' while respecting row/column/3x3-box constraints. A naive backtracking that tries digits 1..9 for each empty cell will work but can be slow for harder puzzles. To speed up, maintain which digits are already used in each row/column/box so candidate checks are O(1). Additionally, use heuristics like choosing the empty cell with the fewest candidates (minimum remaining values, MRV) to prune the search faster. Bitmasks are a compact, fast way to represent used digits for rows/cols/boxes and to compute available candidates quickly.

## Refining the problem, round 2 thoughts
Refine to an implementation that:
- Precomputes used digits for each row, column, and box as 9-bit masks (bits 0..8 map to digits 1..9).
- Builds a list of empty cell coordinates.
- Uses recursive DFS with MRV: at each step, scan the empties to pick the cell with the smallest number of candidate digits; if some cell has 0 candidates, backtrack immediately.
- For candidate iteration, extract low bit repeatedly (mask & -mask) to iterate candidates efficiently.
- Modify the input board in place (LeetCode requirement) and stop once a solution is found.

Complexity: worst-case exponential in number of empties (m), roughly O(9^m), but MRV + constraint propagation prunes heavily. Space complexity: O(m) for recursion and empties list plus O(1) for bitmasks.

## Attempted solution(s)
```python
class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        """
        Modify board in-place to fill the Sudoku solution.
        """
        # Helper: get box index
        def box_index(r: int, c: int) -> int:
            return (r // 3) * 3 + (c // 3)

        # Bit representation: bit 0 -> digit '1', bit 1 -> '2', ..., bit 8 -> '9'
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9
        empties = []

        # Initialize masks and empties list
        for r in range(9):
            for c in range(9):
                ch = board[r][c]
                if ch == '.':
                    empties.append((r, c))
                else:
                    d = int(ch) - 1
                    bit = 1 << d
                    rows[r] |= bit
                    cols[c] |= bit
                    boxes[box_index(r, c)] |= bit

        FULL_MASK = (1 << 9) - 1  # 0x1FF, bits for digits 1..9

        # DFS with MRV (choose empty cell with minimal candidates)
        def dfs() -> bool:
            # If no empties left, solved
            if not empties:
                return True

            # Find the empty cell with the fewest candidates
            best_i = -1
            best_count = 10
            best_mask = 0
            for i, (r, c) in enumerate(empties):
                if board[r][c] != '.':
                    continue  # already filled by earlier step
                mask = ~(rows[r] | cols[c] | boxes[box_index(r, c)]) & FULL_MASK
                cnt = mask.bit_count()
                if cnt == 0:
                    return False  # dead end
                if cnt < best_count:
                    best_count = cnt
                    best_i = i
                    best_mask = mask
                    if cnt == 1:
                        break  # can't get better than 1

            # best_i should be valid
            r, c = empties[best_i]
            bidx = box_index(r, c)

            # Try each candidate digit (iterate bits)
            mask = best_mask
            while mask:
                bit = mask & -mask  # lowest set bit
                d = (bit.bit_length() - 1)  # 0-based digit index
                # place digit
                board[r][c] = str(d + 1)
                rows[r] |= bit
                cols[c] |= bit
                boxes[bidx] |= bit

                # recurse
                if dfs():
                    return True

                # backtrack
                board[r][c] = '.'
                rows[r] &= ~bit
                cols[c] &= ~bit
                boxes[bidx] &= ~bit

                mask &= mask - 1  # clear lowest set bit

            return False

        # Kick off DFS
        dfs()
```
- Notes:
  - Approach: Depth-first search (backtracking) with bitmasking for quick validity checks and MRV (choose the empty with fewest candidates) for pruning.
  - Time complexity: worst-case exponential, O(9^m) where m is the number of empty cells. Practical performance is far better due to constraint propagation and MRV.
  - Space complexity: O(m) for the recursion stack and empties list, plus O(1) for the 27 masks (rows/cols/boxes).
  - Implementation details:
    - Use integer bitmasks for rows/cols/boxes to make candidate computations and updates O(1).
    - Use mask & -mask and bit_length() to iterate over possible digits quickly.
    - Modify the input board in-place as required. The dfs stops when a valid filling is found.