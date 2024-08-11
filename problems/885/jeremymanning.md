# [Problem 885: Spiral Matrix III](https://leetcode.com/problems/spiral-matrix-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I'm seeing a few parts of this problem:
    - First, we need to have an outer while loop (until all cells are visited) where we cycle through right, down, left, and up moves
    - Moving right entails adding 1 to the column; down means adding 1 to the row; left means subtracting 1 from the column; up means subtracting 1 from the row
    - We need to keep track of the max/min rows and columns we've visited.  As we're moving in some direction, we want to keep moving until we hit either:
        - One more than the current max (or min) visited (in which case we should now updated the max/min values as needed) OR
        - The outer bounds of the matrix
    - In some cases (e.g., if some arm of the spiral occurs outside of the bounds of the matrix) we might not add *any* new cells to the path in a given direction.  In that case we just skip to the endpoint and take one step along the next direction in the spiral.
- To keep track of visited locations we can use a list of coordinates, `path`.  This is what we'll return at the end.
- To keep track of the outer bounds, we can use four variables-- `min_row`, `max_row`, `min_col`, and `max_col`.  Initially we can set these to the corresponding values in `rStart` and `cStart`.

## Refining the problem, round 2 thoughts
- The one tricky piece is what happens when we're outside of the bounds of the matrix.
- The "efficient" solution would be to skip ahead to the end of that leg of the path.
    - If we're moving *right* (but above the top or below the bottom of the matrix), then the next coordinate will be `[max_row, max_col]` (and so on for the other directions)
    - But actually, this potentially leads to another tricky scenario: what if the *next* move (e.g., *down* after we've finished moving right) is *also* outside of the bounds of the matrix?
- So instead, I think we should do something easier:
    - If we're ever making a move that's outside of the matrix, we'll follow the same logic in making right/down/left/up moves as always (though not updating the outer bounds if we're already outside of the matrix's limits)-- but we should only append a given "location" to `path` if it falls within the bounds of the matrix-- i.e., for location `[x, y]` we should only append it to `path` if `(0 <= x < rows) and (0 <= y < cols)`.
    - This will be a little less efficient (we might need to temporarily store in memory a set of up to 102 locations, e.g., if we're dealing with a matrix of size 100 along some dimension and we're outside of the bounds at both ends along that dimension) but it's not too bad given the matrix sizes we're dealing with, and it'll make the code much simpler.
- I think I should also write functions `moveRight(x, y)`, `moveLeft(x, y)`, `moveUp(x, y)`, and `moveDown(x, y)` to return a list of moves along the given direction, given the starting location `[x, y]`.  (These will each need to reference the "bounds" variables.)
- Then once we get each move, we can just extend path as follows: `path.extend([[x, y] for x, y in moves if (0 <= x < rows) and (0 <= y < cols)])`.  And if the last position (`moves[-1]`) is within the bounds of the matrix along the relevant direction, we'll need to update the relevant bound accordingly.
- There are a few pieces to this one, but I think it's straightforward.  I'll move on to implementing this now.
- Note: actually, rather than `x` and `y`, let's use `r` (for row) and `c` (for column)...otherwise I think the right/left/up/down functions' notations will get confusing to read.  But functionally they'll be the same as above.

## Attempted solution(s)
```python
class Solution:
    def spiralMatrixIII(self, rows: int, cols: int, rStart: int, cStart: int) -> List[List[int]]:
        min_row, max_row = rStart, rStart
        min_col, max_col = cStart, cStart
        
        def moveRight(pos):
            r, c = pos
            return [[r, x] for x in range(c + 1, max_col + 2)]

        def moveLeft(pos):
            r, c = pos
            return [[r, x] for x in range(c - 1, min_col - 2, -1)]

        def moveUp(pos):
            r, c = pos
            return [[y, c] for y in range(r - 1, min_row - 2, -1)]

        def moveDown(pos):
            r, c = pos
            return [[y, c] for y in range(r + 1, max_row + 2)]

        def inBounds(pos):
            r, c = pos
            return (0 <= r < rows) and (0 <= c < cols)

        path = [[rStart, cStart]]
        pos = [rStart, cStart]
        while len(path) < rows * cols:
            # move right
            moves = moveRight(pos)
            path.extend([m for m in moves if inBounds(m)])
            pos = moves[-1]
            max_col = max(min(cols + 1, pos[1]), max_col)

            # move down
            moves = moveDown(pos)
            path.extend([m for m in moves if inBounds(m)])
            pos = moves[-1]
            max_row = max(min(rows + 1, pos[0]), max_row)

            # move left
            moves = moveLeft(pos)
            path.extend([m for m in moves if inBounds(m)])
            pos = moves[-1]
            min_col = min(max(0, pos[1]), min_col)

            # move up
            moves = moveUp(pos)
            path.extend([m for m in moves if inBounds(m)])
            pos = moves[-1]
            min_row = min(max(0, pos[0]), min_row)

        return path
```
- Given test cases pass
- Let's try some more:
    - `rows = 100, cols = 100, rStart = 50, cStart = 50`: pass
    - `rows = 100, cols = 100, rStart = 99, cStart = 50`: pass
    - `rows = 100, cols = 100, rStart = 99, cStart = 0`: pass
    - `rows = 1, cols = 100, rStart = 0, cStart = 99`: pass
- Ok...let's submit...

![Screenshot 2024-08-07 at 11 55 04 PM](https://github.com/user-attachments/assets/fb2ad127-a514-4737-ae78-b7392b4a8250)

Solved!

