# [Problem 840: Magic Squares In Grid](https://leetcode.com/problems/magic-squares-in-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- The simplest way I can think of to solve this would be to use a 2-D sliding window.  We can start at row 0, column 0, and loop (in a nested loop across rows down columns) through the matrix, counting up how many $3 \times 3$ "windows" are valid magic squares.
- Let's write out a few different functions to make this clean:
    - Given a start position (the row/column of the upper left of a $3 \times 3$ window, return the contents of the window
    - Given a $3 \times 3$ window, test whether it's a magic square:
        - Are the numbers 1 through 9 all included?
        - Do the rows all add up to 15? (Note: I don't *think* it's possible to make a magic square using some other sum-- but just in case, we could use the sum of the first row as the "target" for all other rows/columns, so that we're not hard coding it in.)
        - Do the columns all add up to 15?
        - Do both diagonals add up to 15?

## Refining the problem, round 2 thoughts
- The `getWindow(r, c)` function should look something like this:
```python
def getWindow(r, c):
    return [[grid[i][j] for j in range(c, c + 3)] for i in range(r, r + 3)]
```
- The `isMagicSquare(x)` function should look something like this:
```python
def isMagicSquare(x):
    # has the numbers 1 through 9?
    content = set()
    for i in range(len(x)):
        content.update(set(x[i]))

    if len(content) < 9:
        return False
    if not all([i in content for i in range(1, 10)]):
        return 0

    # all rows add up to the same number?
    target = sum(x[0])
    if any([sum(x[i]) != target for i in range(1, 3)]):
        return 0

    # all columns add up to the same number?
    if any([sum([x[i][j] for i in range(3)]) != target for j in range(3)]):
        return 0

    # diagonal 1 adds up to the same number?
    if sum([x[i][i] for i in range(3)]) != target:
        return 0

    # diagonal 2 adds up to the same number?
    if sum([x[i][2 - i] for i in range(3)]) != target:
        return 0
    
    return 1
```
- Let's put it all together...

## Attempted solution(s)
```python
class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        def getWindow(r, c):
            return [[grid[i][j] for j in range(c, c + 3)] for i in range(r, r + 3)]

        def isMagicSquare(x):
            # has the numbers 1 through 9?
            content = set()
            for i in range(len(x)):
                content.update(set(x[i]))
        
            if len(content) < 9:
                return False
            if not all([i in content for i in range(1, 10)]):
                return 0
        
            # all rows add up to the same number?
            target = sum(x[0])
            if any([sum(x[i]) != target for i in range(1, 3)]):
                return 0
        
            # all columns add up to the same number?
            if any([sum([x[i][j] for i in range(3)]) != target for j in range(3)]):
                return 0
        
            # diagonal 1 adds up to the same number?
            if sum([x[i][i] for i in range(3)]) != target:
                return 0
        
            # diagonal 2 adds up to the same number?
            if sum([x[i][2 - i] for i in range(3)]) != target:
                return 0
            
            return 1

        count = 0
        for i in range(len(grid) - 2):
            for j in range(len(grid[0]) - 2):
                count += isMagicSquare(getWindow(i, j))

        return count
```
- Given test cases pass
- Now let's make some random matrices:
    - `grid = [[9, 3, 14, 4, 4, 15, 7, 1, 1, 8], [1, 11, 6, 3, 7, 14, 7, 8, 11, 11], [1, 14, 5, 7, 7, 8, 14, 12, 10, 7], [3, 10, 4, 5, 12, 6, 13, 9, 9, 2], [15, 10, 11, 6, 15, 10, 13, 1, 1, 14], [11, 12, 8, 11, 12, 2, 3, 1, 1, 3], [3, 13, 5, 4, 6, 9, 9, 6, 2, 6], [13, 3, 3, 4, 13, 1, 13, 14, 9, 15], [14, 12, 9, 12, 9, 2, 3, 15, 15, 4], [13, 11, 6, 15, 5, 12, 11, 8, 5, 13]]`: pass
    - `grid = [[1, 8, 4, 1, 8, 14, 12, 6, 4, 4], [14, 8, 9, 2, 6, 9, 2, 12, 10, 6], [15, 10, 4, 6, 5, 6, 3, 10, 3, 13], [8, 3, 1, 15, 2, 9, 4, 14, 1, 15], [6, 2, 6, 9, 11, 2, 4, 7, 3, 6], [6, 1, 3, 6, 6, 8, 2, 8, 6, 4], [10, 13, 2, 7, 10, 5, 6, 8, 4, 6], [6, 3, 3, 3, 8, 3, 10, 11, 12, 4], [8, 15, 15, 15, 3, 11, 14, 13, 6, 5], [9, 9, 3, 11, 2, 7, 8, 13, 13, 9]]`: pass
- To "really" test this completely we should make some grids containing magic squares...but instead I'm just going to submit this, because I think the logic is sound overall.

![Screenshot 2024-08-08 at 11 31 40 PM](https://github.com/user-attachments/assets/062aac28-06ae-4393-bcde-fb714386f611)

Solved!
