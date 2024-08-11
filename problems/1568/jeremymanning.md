# [Problem 1568: Minimum Number of Days to Disconnect Island](https://leetcode.com/problems/minimum-number-of-days-to-disconnect-island/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- The wording of this problem is confusing-- what does "maximal 4-directionally (horizontal or vertical) connected group of 1's" mean?  From the examples, it looks like 1's that are in adjacent blocks (horizontally _or_ vertically) are considered to be connected.
- But I guess (from Example 2) a single 1 in isolation is *also* considered to be connected, even though it has no neighbors?
- Another strange aspect of the problem is the "exactly one island" part of the "connected" definition.  E.g., in Example 1 both of the remaining 1's are "fully connected islands" (each comprising just a single block), but they don't "count" because there are *two* islands rather than 1.
- So it seems like we might need to make some sort of graph representation, where each cell containing a 1 has an edge to other horizontal or vertical neighbors that also contain 1's.
    - To isolate *all* islands, we could continually do the following, until there are no cells with any connections:
        - Sort cells by number of connections (in descending order of numbers of connections)
        - Convert the most-connected cell and remove it from all other connection lists
    - But we don't need to go quite that far-- maybe all we need is *either* 0 connections for all 1's *or* at least 2 cells with 0 connections...or more broadly, at least 2 isolated groups that aren't connected to each *other*.
        - How can we detect when groups are isolated?  Ignoring efficiency issues, we could initialize a list of groups to `[]` and then go through each cell (containing a 1) in order:
            - Identify which group(s) contain *any* locations connected to the current cell (including the cell itself)
                - If there are multiple groups, merge those groups and add the current cell along with its connections
                - If there is only 1 group, just add the current cell along with its connections (actually...maybe this is the same case as the multiple group case-- we'll just have a list containing one "matching" group)
                - If there are 0 groups that contain any locations connected to the current cell (including the cell itself), start a new group
            - If, after going through all of the groups, there is just a single group of connected cells, then we're not done.  If there are 0 groups, or if there are multiple distinct groups, then we can stop.
- I think this solution would _work_, but I'm not sure it's practical because it seems very inefficient:
    - We need nested loops to go through all of the 1's.  There could potentially be $O(mn)$ of these, so the inner loop is run $O((mn)^2)$ times.
    - The "detecting isolated sets" algorithm above *also* needs to run any time we convert a cell.  That would seem to require (at least) an additional $O(mn)$ steps...assuming constant lookup time to see if there's any overlap between two sets of numbers.  (But this could take *linear* time-- $O(mn)$, in which case it's even _worse_ than what I'm assuming.)  So the full algorithm would be require something like $O((mn)^3)$, or possibly even $O((mn)^4)$ time.  The max grid size is $30 \times 30$, so we're looking at somewhere in the range of billions to hundreds of billions of steps.  I think we need a better approach.
- Let's consider different possibilities:
    - If there are *no* cells with 1's, return 0 (there are 0 islands)
    - If there is exactly *1* cell with a 1, return 1-- we just need to convert it to a 0
    - If there are several cells with 1's:
        - If the islands are *not* connected, then we can return 0 immediately
        - If those cells _are_ connected, then...what can we do?
            - We can make a single edit if the least-connected 1 has only a single neighbor and there is at least 1 other 1 cell remaining after we remove the neighbor.  In other words, if we have something like this:
            ```
            00100
            00100
            01110
            00000
            ```
            Then the top 1 could be isolated by removing the second-to top 1:
            ```
            00100
            00000
            01110
            00000
            ```
            And now we have 2 islands.
            - But if the least-connected 1 has *two* neighbors, then we'll need to remove 2 cells (we can just return 2).  I.e., suppose we have a scenario similar to Example 1:
            ```
            0110
            0110
            0000
            ```
            All of the 1's are equally connected (each has 2 neighbors), so we can pick any of them to isolate.  No matter which one we pick, this will require 2 converstions.  And this is true of *any* layout (where the least-connected 1 has two neighbors).  Even if we have some larger grid, like this:
            ```
            11110000
            11110000
            11110000
            11110000
            00000000
            ```
            Then the "corners" of the island will still have only two neighbors (even though the middle cells have 4).  So we can isolate them in 2 conversions.
            - And just to check another case, what if we have something like this:
            ```
            11000
            01000
            11000
            11000
            00000
            ```
            Then that 1 in the upper left could be cut off to break the original island apart.
- Ok...so I think the answer is always going to be either 0, 1, or 2:
    - If there are no 1s, or if the initial state is disconnected, return 0
    - If the least-connected 1 has 1 connection *and* removing that connection still leaves behind at least 1 more cell with a 1 in it, return 1
    - Otherwise, return 2
- So the main trick is going to be figuring out if there are 2 or more islands.  I think we can solve this similar to yesterday's problem:
    - Initialize a matrix, `visited` to all `False`s (should be the same size as `grid`)
    - Start with any cell containing a 1 (just pick the first one) and enqueue it.
    - While the queue isn't empty:
        - Pop the first cell in the queue and mark it as visited
        - Enqueue all of its neighbors that are 1's
    - Now loop through the full `grid`: if there are any cells that are 1's in `grid` but that are *not* visited, then we know there are at least 2 disconnected islands.
- The second trick is figuring out when we're in the "least-connected 1 has just 1 connection" scenario.  We could do something like:
    - Loop through the `grid` (row: `i`; column: `j`)
    - If `grid[i][j] == 1` then add `[i, j]` to a hash table (as a key)-- e.g. `graph[(i, j)] = []`
        - Also find any immediately adjacent neighbors of `grid[i][j]` and list them in `graph[(i, j)]`
    - Now loop through all of the keys of `graph`:
        - For any that have just a single connection `(x, y)`:
            - Loop through all of the other keys of `graph` (besides `(i, j)` and `(x, y)`).  If there is at least one of these, return 1.  Otherwise return 2.

## Refining the problem, round 2 thoughts
- For convenience, let's write a function to grab the neighbors of location `(i, j)` that are also 1's:
```python
def neighbors(i, j):
    x = []
    if i > 0 and grid[i - 1][j] == 1:
        x.append((i - 1, j))

    if i < len(grid) - 1 and grid[i + 1][j] == 1:
        x.append((i + 1, j))

    if j > 0 and grid[i][j - 1] == 1:
        x.append((i, j - 1))

    if j < len(grid[0]) - 1 and grid[i][j + 1] == 1:
        x.append((i, j + 1))
    return x
```
- Let's first write out the `one_island(grid)` function to determine if the grid is disconnected:
```python
def one_island(grid):
    queue = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                queue.append((i, j))
                break
        if len(queue) > 0:
            break

    if len(queue) != 1:  #There are no 1s in the grid
        return False

    # otherwise we need to do a breadth-first search (DFS would also work)
    visited = [[False for _ in grid[0]] for _ in grid]
    while len(queue) > 0:
        i, j = queue.pop(0)
        visited[i][j] = True

        # enqueue neighbors, if any
        for x, y in neighbors(i, j):
            if not visited[x][y]:
                queue.append((x, y))        

    # now see if there are any unvisited 1s left
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1 and not visited[i][j]:
                return False
    return True
```
- Next let's detect the "least-connected 1 has just 1 connection, and there's stuff left after removing it" scenario:
```
def isolatable_1(grid):
    graph = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                graph[(i, j)] = neighbors(i, j)

    sorted_graph = list(sorted(list(graph.items()), key=lambda x: len(x[1])))
    for n in sorted_graph:
        if len(n[1]) == 1:            
            i, j = n[0]
            x, y = n[1][0]

            # see if there are any other 1s besides i, j and x, y
            for m in sorted_graph:
                if m[0] not in [(i, j), (x, y)]:
                    return True
    return False
```
- Now we can put the full thing together...        

## Attempted solution(s)
```python
class Solution:
    def minDays(self, grid: List[List[int]]) -> int:
        def neighbors(i, j):
            x = []
            if i > 0 and grid[i - 1][j] == 1:
                x.append((i - 1, j))
        
            if i < len(grid) - 1 and grid[i + 1][j] == 1:
                x.append((i + 1, j))
        
            if j > 0 and grid[i][j - 1] == 1:
                x.append((i, j - 1))
        
            if j < len(grid[0]) - 1 and grid[i][j + 1] == 1:
                x.append((i, j + 1))
            return x
    
        def one_island(grid):
            queue = []
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1:
                        queue.append((i, j))
                        break
                if len(queue) > 0:
                    break
        
            if len(queue) != 1:  #There are no 1s in the grid
                return False
        
            # otherwise we need to do a breadth-first search (DFS would also work)
            visited = [[False for _ in grid[0]] for _ in grid]
            while len(queue) > 0:
                i, j = queue.pop(0)
                visited[i][j] = True
        
                # enqueue neighbors, if any
                for x, y in neighbors(i, j):
                    if not visited[x][y]:
                        queue.append((x, y))        
        
            # now see if there are any unvisited 1s left
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1 and not visited[i][j]:
                        return False
            return True
    
        def isolatable_1(grid):
            graph = {}
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1:
                        graph[(i, j)] = neighbors(i, j)
        
            sorted_graph = list(sorted(list(graph.items()), key=lambda x: len(x[1])))
            for n in sorted_graph:
                if len(n[1]) == 1:            
                    i, j = n[0]
                    x, y = n[1][0]
        
                    # see if there are any other 1s besides i, j and x, y
                    for m in sorted_graph:
                        if m[0] not in [(i, j), (x, y)]:
                            return True
            return False
    
        if not one_island(grid):
            return 0
        elif isolatable_1(grid):
            return 1
        else:
            return 2
```
- Ok...the given test cases pass
- Another test case: `grid = [[0,1,1,0],[0,1,1,0],[0,1,0,0],[0,1,1,0]]`: pass
- Let's submit...

![Screenshot 2024-08-10 at 11 56 08 PM](https://github.com/user-attachments/assets/7fc910de-93c6-46c0-8572-28b6f0581834)

Ok, well...bummer.

I'm guessing the issue is with my `isolatable_1` function-- that one is the most "hacky."  A more "robust" solution would be:
  - Fill in the graph like I did before (although...we don't really need to sort the graph anymore)
  - For each cell with 1 neighbor, see if changing the neighbor to 0 now "fixes" the 1 island scenario.  If `not one_island(updated_grid)`, we can return `True`
  - If none of the removals "work" then return `False`:
```python
def isolatable_1(grid):
    graph = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                graph[(i, j)] = neighbors(i, j)
    
    for cell, connections in graph.items():
        if len(connections) == 1:
            x, y = connections[0]

            grid[x][y] = 0
            if not one_island(grid):
                grid[x][y] = 1  # restore that location (before returning)
                return True
            grid[x][y] = 1      # restore that location!
    return False
```

So let's put the full (updated) thing together:
```python
class Solution:
    def minDays(self, grid: List[List[int]]) -> int:
        def neighbors(i, j):
            x = []
            if i > 0 and grid[i - 1][j] == 1:
                x.append((i - 1, j))
        
            if i < len(grid) - 1 and grid[i + 1][j] == 1:
                x.append((i + 1, j))
        
            if j > 0 and grid[i][j - 1] == 1:
                x.append((i, j - 1))
        
            if j < len(grid[0]) - 1 and grid[i][j + 1] == 1:
                x.append((i, j + 1))
            return x
    
        def one_island(grid):
            queue = []
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1:
                        queue.append((i, j))
                        break
                if len(queue) > 0:
                    break
        
            if len(queue) != 1:  #There are no 1s in the grid
                return False
        
            # otherwise we need to do a breadth-first search (DFS would also work)
            visited = [[False for _ in grid[0]] for _ in grid]
            while len(queue) > 0:
                i, j = queue.pop(0)
                visited[i][j] = True
        
                # enqueue neighbors, if any
                for x, y in neighbors(i, j):
                    if not visited[x][y]:
                        queue.append((x, y))        
        
            # now see if there are any unvisited 1s left
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1 and not visited[i][j]:
                        return False
            return True
    
        def isolatable_1(grid):
            graph = {}
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1:
                        graph[(i, j)] = neighbors(i, j)
            
            for cell, connections in graph.items():
                if len(connections) == 1:
                    x, y = connections[0]
                    
                    grid[x][y] = 0
                    if not one_island(grid):
                        grid[x][y] = 1  # restore that location (before returning)
                        return True
                    grid[x][y] = 1      # restore that location!
            return False
    
        if not one_island(grid):
            return 0
        elif isolatable_1(grid):
            return 1
        else:
            return 2
```
- Hmm...that test case still fails.  Let's actually dig into it then (but for the record, I am doing this begrudgingly!):
- `grid = [[1,1,0,1,1],[1,1,1,1,1],[1,1,0,1,1],[1,1,0,1,1]]`
- And we can draw this out:
```
11011
11111
11011
11011
```
- Ah.  Ok, so this is a case I didn't account for.  That "middle of the H" 1 cell has *2* neighbors, but removing it would isolate the islands on the sides.  Hrmph.
- And actually, it's even more dire than I though, because we could have a scenario like this:
```
11011
11111
11011
11111
11011
11111
11011
```
- Where we now need to remove *3* 1s in order to split those islands...
- ...Or...actually, maybe not.  Because we could just isolate one of the 1s in a corner, like this:
```
10011
01111
11011
11111
11011
11111
11011
```
and still "fix" this in 2 steps.
- So it seems like there's an additional case to account for: does converting *any* single 1 result in an acceptable solution?  If so, return 1.  Otherwise we'll need to return 2.
- We can implement this by tweaking the `isolatable_1` function (let's just search over all 1s, instead of first doing the graph thing).  We can call the new function `single_fix`:
```python
class Solution:
    def minDays(self, grid: List[List[int]]) -> int:
        def neighbors(i, j):
            x = []
            if i > 0 and grid[i - 1][j] == 1:
                x.append((i - 1, j))
        
            if i < len(grid) - 1 and grid[i + 1][j] == 1:
                x.append((i + 1, j))
        
            if j > 0 and grid[i][j - 1] == 1:
                x.append((i, j - 1))
        
            if j < len(grid[0]) - 1 and grid[i][j + 1] == 1:
                x.append((i, j + 1))
            return x
    
        def one_island(grid):
            queue = []
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1:
                        queue.append((i, j))
                        break
                if len(queue) > 0:
                    break
        
            if len(queue) != 1:  #There are no 1s in the grid
                return False
        
            # otherwise we need to do a breadth-first search (DFS would also work)
            visited = [[False for _ in grid[0]] for _ in grid]
            while len(queue) > 0:
                i, j = queue.pop(0)
                visited[i][j] = True
        
                # enqueue neighbors, if any
                for x, y in neighbors(i, j):
                    if not visited[x][y]:
                        queue.append((x, y))        
        
            # now see if there are any unvisited 1s left
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1 and not visited[i][j]:
                        return False
            return True
    
        def single_fix(grid):
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 1:
                        # try removing this cell
                        grid[i][j] = 0
                        if not one_island(grid):
                            grid[i][j] = 1
                            return True
                        grid[i][j] = 1
            return False
    
        if not one_island(grid):
            return 0
        elif single_fix(grid):
            return 1
        else:
            return 2
```
- Ok...*now* all of the test cases (including the one that failed before) work.  I'll try submitting again...

![Screenshot 2024-08-11 at 12 20 06 AM](https://github.com/user-attachments/assets/cd8bca38-7554-41c9-93fa-f2aff800acdf)

- Ugh...time limit exceeded when `grid = [[1,1,1,1,1,1,1,1,1,1,1,0,1],[1,1,1,1,1,1,1,1,1,0,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1,1,1],[0,1,1,0,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,0],[1,0,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,0,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,0,1,1,1],[0,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1,1,1]]`
- And even *testing* that one example doesn't work (runs out of time in the manual testing system too)
- I'm going to come back to this tomorrow...


