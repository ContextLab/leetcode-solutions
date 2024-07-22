# [Problem 2392: Build a Matrix With Conditions](https://leetcode.com/problems/build-a-matrix-with-conditions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- this looks fun but also challenging to do efficiently.
- my first thought is that I could convert the conditions lists into some sort of graph where each unique value is a node and the "must be [left|right|above|below]" relationships are edges. Then I could traverse the edges to find the [left|right|top|bottom]-most values and place them in the first column/last column/top row/bottom row of the matrix.
- I think this would also give me a way to detect cases where "no answer exists" due to contradictory conditions. I could maintain a set of "visited" nodes, and if I ever encounter one I've already visited, then there's a cycle in the graph which means the conditions are contradictory and I can return an empty matrix.
- ~~the fact that I'm supposed to return an empty matrix if no answer exists makes me think I should be able to determine that before I start filling the matrix in, otherwise I'd have to "clear" or re-initialize the matrix in order to return it.~~ never mind, "empty matrix" means `[]`, not a `k` $\times$ `k` matrix of zeros.
- how could I set this up to actually be able to traverse the graph though? Should each node have an edge to all nodes I know from the conditions that it's above/left of? Or just the one it's directly above? How would I deal with a situation where I had something like `rowConditions = [[1, 3], [2, 4], [2, 3]]`? Valid top to bottom orders for that would be `1, 2, 3, 4` or `2, 1, 3, 4` or `1, 2, 4, 3`.
- I'm getting stuck so let's step back a bit. The matrix needs to be `k` $\times$ `k` and the values we need to add to it are all numbers from 1 to `k`. So if there are `k` rows & columns and `k` values to add, and the values have to be "**strictly**" above/below/left/right of each other, I think that means each row and column will contain exactly one value. And I think that in turn means that we can figure out the row and column orderings of the values independently of each other.
- so that makes this kinda like a sorting problem? Or rather, two sorting problems (one for rows and one for columns)?

---

- Thanks to Jeremy for the hint -- turns out this *does* in fact involve "sorting" a graph! So I wasn't totally off above...
- This is a bit of a cop-out, but in the interest of moving onto other things, it turns out there's a Python stdlib module called [`graphlib`](https://docs.python.org/3/library/graphlib.html) that has a `TopologicalSorter` class I can use for this. So I'll do that for now... but I should probably learn this algorithm at some point.
- One last thing potentially worth considering -- example 2 suggests there can be duplicates in either of the conditions lists. I wonder if it'd be worth removing those before constructing and sorting the graph? Easiest way would be to convert the conditions lists to sets, but since sets can only contain hashable objects, I'd have to convert the inner lists to tuples first. So it could end not being worth it in terms of runtime.
- Actually, I can do it while constructing the `dict`-format graph `TopologicalSorter` expects by having the values be sets instead of lists. It'll still add some overhead vs including the duplicates, but not as much as the idea above.

## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
from graphlib import TopologicalSorter, CycleError

class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        # wrote this with runtime/memory optimization in mind, but IRL would
        # structure this more cleanly & name things more readibly
        graph = {i: set() for i in range(1, k+1)}
        for i, j in rowConditions:
            graph[j].add(i)
        try:
            row_order = tuple(TopologicalSorter(graph).static_order())
        except CycleError:
            return []

        graph = {i: set() for i in range(1, k+1)}
        for i, j in colConditions:
            graph[j].add(i)
        try:
            col_order = tuple(TopologicalSorter(graph).static_order())
        except CycleError:
            return []

        matrix = [[0] * k for _ in range(k)]
        for i, j in enumerate(row_order):
            matrix[i][col_order.index(j)] = j
        return matrix
```

![](https://github.com/user-attachments/assets/9b41b7ab-7852-4759-87ef-a9fd725f4667)
