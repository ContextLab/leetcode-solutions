# [Problem 1514: Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- First we need a way to represent the graph more conveniently.  I'm thinking we should have a hash table whose keys are nodes and whose values are lists of connected nodes + probabilities.  E.g., for the first given example, `graph[0] = [(2, 0.2), (1, 0.5)]`, etc.  We can build up this hash table with a single pass through the edge list + success probability list:
```python
graph = {}
for edge, prob in zip(edges, succProb):
    if edge[0] in graph:
        graph[edge[0]].append((edge[1], prob))
    else:
        graph[edge[0]] = [(edge[1], prob)]

    if edge[1] in graph:
        graph[edge[1]].append((edge[0], prob))
    else:
        graph[edge[1]] = [(edge[0], prob)]
```
- Now I think we can build up paths using BFS or DFS starting from `start_node`:
    - If we hit a loop, stop and delete that path from the queue/stack
    - If we reach `end_node`:
        - Go back and compute the probability of this path
        - If it's higher than the probability of the current best path (initialized to `0`), replace the best probability
        - Then delete the path from the queue/stack
- Potential pitfalls:
    - We might run out of memory if we build up the paths one node at a time.
    - Ideally we could instead just build up something like probability of the path so far + last node reached.  But then I'm not sure we'll be able to detect loops...
    - The probabilities could get very small, leading to rounding errors.  We could instead track *log* probabilities (summing as we go) and then exponentiate at the end.
- Instead of BFS/DFS, maybe we want to use a heap to keep the paths sorted by max probability.

## Refining the problem, round 2 thoughts
We could use the built-in `heapq` to do this (according to the documentation `heapq` is a max heap, but we can just multiply the probabilities by -1 so that the most probable paths appear at the "top" of the heap):
    - First push the start of the path (`(-1.0, start_node)`) onto the heap
    - Keep track of `n` probabilities (of reaching each node).  Initialize to 0.0, except the start node (initialize to 1.0).
    - While the heap is not empty:
        - Pop the most probable path `(prob, last_node)`
        - If we're at the end node, return `prob`
        - Otherwise:
            - For each neighbor `x` of `last_node` (connected with probability `new_prob`):
                - Probability of path ending at `x` is `-prob * new_prob`
                - If `-prob * new_prob` is greater than `probabilities[x]`:
                    - Update `probabilities[x]` -- this ensures we only push more probable paths than we've already found onto the heap.  This also avoids loops, since visiting an already-visited node will necessarily result in a lower probability path to that node.
                    - Push `(prob * new_prob, x)` on the heap
    - If the heap empties before we found the end, just return 0.0.

## Attempted solution(s)
```python
import heapq

class Solution:
    def maxProbability(self, n, edges, succProb, start, end):
        # build the graph
        graph = {}
        for x in range(n):
            graph[x] = []
        for edge, prob in zip(edges, succProb):
            graph[edge[0]].append((edge[1], prob))
            graph[edge[1]].append((edge[0], prob))
            
        # max heap
        heap = [(-1.0, start)]
        probabilities = [0.0] * n
        probabilities[start] = 1.0

        while heap:
            p, node = heapq.heappop(heap)
            if node == end:
                return -p

            for x, xp in graph[node]:
                new_prob = p * xp   # remember: this is negative
                if -new_prob > probabilities[x]:
                    probabilities[x] = -new_prob
                    heapq.heappush(heap, (new_prob, x))

        # end not found :(
        return 0.0
```
- Given test cases pass
- Another example:
```python
n = 7
edges = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6]]
succProb = [0.01, 0.01, 0.01, 0.01, 0.01, 0.1]
start_node = 0
end_node = 6
```
- passes!
- Ok, submitting!

![Screenshot 2024-08-27 at 12 07 09 AM](https://github.com/user-attachments/assets/3d64e697-53a5-4cbf-a3b4-d397ea27a0f5)

Solved!

