# [Problem 959: Regions Cut By Slashes](https://leetcode.com/problems/regions-cut-by-slashes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- This is a tricky one!
- I have two ideas:
    - I could replace each symbol with a $3 \times 3$ "ASCII art" representation.  I.e.:
        - " " becomes
        ```
        000
        000
        000
        ```

        - "/" becomes

        ```
        00.*
        0*0
        *00
        ```

        - and "\\" becomes

        ```
        *00
        0*0
        00*
        ```
  
        - Then we can stitch together these building blocks to form the "image" of the full grid.  (An $n \times n$ grid's "image" will be $3n \times 3n$.)
        - Once we have that image, we can go through line by line (i.e., from left to right, across rows and down columns):
            - Initialize a counter to 1
            - Replace each "0" with the current value of the counter
            - If we encounter a "." or newline, increment the counter
        - Finally, we need to do a second pass through the full "image" to merge values that appear at neighboring (i.e., immediately above or below) cells.  I'll need to think through the implementation, but I think it'd be straightforward.
    - "My" second idea comes from [discussions](https://context-lab.slack.com/archives/C0753BB4MC5/p1723250580331859) in our slack channel (thanks @paxton!):
        - Initialize a counter to 0
        - Initailize the "position" to 0
        - Repeat until position (`i`) is less than $n^2$ (where $n$ is the length of one side of the grid):
            - Scan (across rows, down columns) through the grid, incrementing `i` as we go until we encounter a " ".  If so:
                - initalize a queue to include `i` and replace the " " at position `i` with an "x"
                - while the queue is not empty:
                    - pop the front of the queue (position `j`) and replace the " " at position `j` with an "x"
                    - enqueue any neighbors (above, below, left, or right) of position `j` that contain a " ".  The idea here is to find the next contiguous region of `" "`s.
        - Return the value of the counter
- The second idea seems more efficient, so I'm going to try that!

## Refining the problem, round 2 thoughts
- I'm seeing two pieces to this problem:
    - We need a way to convert from a "position" `i` to a specific row/column of the grid.  I think this is straightforward: the row is given by `i // n` and the column is given by `i % n`.
    - We need a way of finding the neighbors of position `i`:
        - It might help to have a function for going "back" from a row/column to a "position":
            - If the row is `r` and column is `c`, then the position is `rn + c`
        - Given the row `r` and column `c`, the neighbors are as follows:
            - The "above" neighbor is `(r - 1)n + c` if `r > 0`, or `None` otherwise
            - The "below" neighbor is `(r + 1)n + c` if `r < n - 1`, or `None` otherwise
            - The "right" neighbor is `rn + c + 1` if `c < n - 1`, or `None` otherwise
            - The "left" neighbor is `rn + c - 1` if `c > 0` or `None` otherwise
- So we can actually get rid of the "list of strings" representation entirely, and just replace the grid with a "listified" single string (`list("".join(grid))`).  Then we can go through the above without dealing with list indices.
- I think I'm ready to implement this...

## Attempted solution(s)
```python
class Solution:
    def regionsBySlashes(self, grid: List[str]) -> int:
        n = len(grid)
        grid = list("".join(grid))

        pos2rc = lambda i: [i // n, i % n]
        rc2pos = lambda r, c: r * n + c

        count = 0
        i = 0
        while i < n ** 2:
            if grid[i] == " ":
                count += 1
                grid[i] = "."
                queue = [i]
                while len(queue) > 0:
                    j = queue.pop(0)
                    grid[j] = "."
                    r, c = pos2rc(j)

                    # above
                    if r > 0:
                        if grid[(r - 1) * n + c] == " ":
                            queue.append((r - 1) * n + c)

                    # below
                    if r < n - 1:
                        if grid[(r + 1) * n + c] == " ":
                            queue.append((r + 1) * n + c)

                    # right
                    if c < n - 1:
                        if grid[r * n + c + 1] == " ":
                            queue.append(r * n + c + 1)

                    # left
                    if c > 0:
                        if grid[r * n + c - 1] == " ":
                            queue.append(r * n + c - 1)
            i += 1
        return count
```
- Ok...so after running this on the given test cases, I'm seeing that this isn't quite right: the test example `grid = ["/\\","\\/"]` is failing, because there are no spaces.  So my search for contiguous region needs some tweaking.  Maybe rather than starting a search when we find a blank space, we should (also? instead?) start a search when we encounter the *boundary* of a region...although then we need to know whether to search to the left/right.  Maybe we can just pick one direction arbitrarily (left?)?  And then at the very end (when we've gotten to the bottom right of the graph; `i == n ** 2`) we probably need to do an *additional* search (or...counter increment, since by the time we get there, there won't be any neighboring blanks) if that last block is a "/".
    - Actually, let's think this through:
        - If we encounter a "/" at the top left or bottom right, we need to increment the counter
        - If we encounter a "\\" at the top right or bottom left, we need to increment the counter
        - And then...how can we know whether a "shape" is enclosed? 🤔
        - I think this is actually not going to work.  To implement this solution properly, we would need to trace out the full extent of every region's boundary, until we have a self-intersection, or something like that.  I'm sure it's *possible* to do this, but I'm not immediately seeing a straightforward way.
        - So...I think I might want to just go back to the "ASCII art" idea.

## Refining the ASCII art idea
- Let's re-represent the grid as a $3n \times 3n$ matrix of characters:
    - " " represents an empty space
    - "*" represents a boundary
    - "x" represents somewhere we've visited (I think we can "borrow" the BFS idea to link together contiguous regions of empty space)
- First we can just initialize the grid to a bunch of `" "`s.  Then we can loop through (in a nested loop) each row/column, adding in boundaries when we encounter "/" or "\\" characters.
- This gives us our full "ASCII art" representation of the grid
- Once we have that, we can start counting regions.  I think we can actually just re-use the code above, with some tweaks:
    - Define a new "grid" using the ASCII art representation
    - Multiply `n` by 3 so that we're using the ASCII coordinates instead of the original coordinates
    - Then (I think!) we can re-use the code above
- I think we're good to implement this...
```python
class Solution:
    def regionsBySlashes(self, grid: List[str]) -> int:
        n = len(grid)

        # build an "ASCII art" version of the grid
        ascii_grid = [[" "] * (3 * n) for _ in range (3 * n)]
        for i in range(n):
            for j in range(n):
                if grid[i][j] == "/":
                    ascii_grid[3 * i][3 * j + 2] = "*"
                    ascii_grid[3 * i + 1][3 * j + 1] = "*"
                    ascii_grid[3 * i + 2][3 * j] = "*"
                elif grid[i][j] == "\\":
                    ascii_grid[3 * i][3 * j] = "*"
                    ascii_grid[3 * i + 1][3 * j + 1] = "*"
                    ascii_grid[3 * i + 2][3 * j + 2] = "*"

        # now re-use our solution above (but adjust ascii_grid and n to accomodate...)
        grid = list("".join(["".join([x for x in row]) for row in ascii_grid]))
        n *= 3

        pos2rc = lambda i: [i // n, i % n]
        rc2pos = lambda r, c: r * n + c

        count = 0
        i = 0
        while i < n ** 2:
            if grid[i] == " ":
                count += 1
                grid[i] = "."
                queue = [i]
                while len(queue) > 0:
                    j = queue.pop(0)
                    grid[j] = "."
                    r, c = pos2rc(j)

                    # above
                    if r > 0:
                        if grid[(r - 1) * n + c] == " ":
                            queue.append((r - 1) * n + c)

                    # below
                    if r < n - 1:
                        if grid[(r + 1) * n + c] == " ":
                            queue.append((r + 1) * n + c)

                    # right
                    if c < n - 1:
                        if grid[r * n + c + 1] == " ":
                            queue.append(r * n + c + 1)

                    # left
                    if c > 0:
                        if grid[r * n + c - 1] == " ":
                            queue.append(r * n + c - 1)
            i += 1
        return count
```
- Now all of the test cases pass!
- I'm just going to try submitting... 🤞

Oh, 💩...time limit exceeded:

![Screenshot 2024-08-10 at 12 06 40 AM](https://github.com/user-attachments/assets/9dd10319-fc3e-4c36-b576-1c86aaf8d429)

- There are some "quick" tweaks I can make:
  - Instead of paying the overhead of converting everything to/from the "position" to "row/column" coordinates, I could just work directly with the ascii_grid representation
  - If this isn't sufficient, I could explore whether depth-first search is somehow faster than breadth-first search, although I can't see how it would be (we still need to visit every region...but maybe the overhead from popping at the front instead of the back of a list is much higher?)

- Slightly tweaked version:
```python
class Solution:
    def regionsBySlashes(self, grid: List[str]) -> int:
        n = len(grid)

        # Build an "ASCII art" version of the grid
        ascii_grid = [[" "] * (3 * n) for _ in range(3 * n)]
        for i in range(n):
            for j in range(n):
                if grid[i][j] == "/":
                    ascii_grid[3 * i][3 * j + 2] = "*"
                    ascii_grid[3 * i + 1][3 * j + 1] = "*"
                    ascii_grid[3 * i + 2][3 * j] = "*"
                elif grid[i][j] == "\\":
                    ascii_grid[3 * i][3 * j] = "*"
                    ascii_grid[3 * i + 1][3 * j + 1] = "*"
                    ascii_grid[3 * i + 2][3 * j + 2] = "*"

        # Git countin' 🤠!
        count = 0
        for i in range(3 * n):
            for j in range(3 * n):
                if ascii_grid[i][j] == " ":
                    count += 1
                    queue = [(i, j)]
                    while len(queue) > 0:
                        x, y = queue.pop(0)
                        if 0 <= x < 3 * n and 0 <= y < 3 * n and ascii_grid[x][y] == " ":
                            ascii_grid[x][y] = "."  # Mark as visited
                            # Visit all 4 neighboring cells
                            queue.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

        return count
```
- Given test cases all (still) pass...and I don't think the logic has changed, so I'm going to just submit

![Screenshot 2024-08-10 at 12 17 22 AM](https://github.com/user-attachments/assets/bbacd813-67cf-4d11-9cbc-babf36064e78)

Phew 😅!
