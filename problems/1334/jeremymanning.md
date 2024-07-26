# [Problem 1334: Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- There's probably a very efficient way to do this, but what comes to mind initially is that we should just start by building the graph.  I'll need to think of an appropriate representation for storing the nodes/edges.
- Then I think we could have a hash table (keys: nodes; values: list of other nodes reachable in less than or equal to `distanceThreshold` steps).  How can we build this?
- Then we can loop through the nodes and return the one with the minimum number of neighbors (and the greatest ID number if there are multiple cities with that same minimum number of neighbors)

## Refining the problem, round 2 thoughts

### Some implementation ideas
- **Graph representation:**
    - Option 1: hash table
        - Let's store nodes in a `dict` (keys: node; values: direct connections...maybe as touples so that we can also store the edge weights?)
        - Note: if the weight of a given connection is more than `distanceThreshold`, we can just ignore it
        - We should also add edges bidirectionally
    - Option 2: adjacency matrix:
        - Rows and columns are nodes, and the entries tell us how far each node is from each other node (inf if there's no edge between the nodes)
            - I kind of like this approach, because I suspect we could use some sort of graph traversal algorithm to propagate the edges 🤔
- **Building up a table of cities within the threshold distance:**
    - Once we've added the edges, I think we'll need to do another loop through to see what's reachable within the threshold distance
    - We could do something like the following (for each node `i` in turn, in ascending order):
        - Set `d = distanceThreshold`
        - loop through everything within distance `d` of the current node.  Suppose another node, `j` is in that list and is distance `x` from node `i`:
            - Increment node `i`'s counter
            - Now search for things that are within `d - x` of node `j`
            - Keep repeating this process until there are no more nodes within the threshold distance away
            - We could use either a stack or a queue to do the searching...there's probably a way to cache some of the computations so that we don't have to re-do them each time we visit a node
- **Final loop:**
    - Initialize `minCity = [cities[0], reachable[0]]`
    - Then loop through each node in turn, replacing `minCity` if `reachable[i] < minCity[1] or (reachable[i] == minCity[1] and minCity[0] < cities[i])`
    - return `minCity[0]`
    - Note: since we know the cities range from `0...n-1`, we could also loop through in reverse order of the city numbers and just replace `minCity` if `reachable[i] < minCity[1]`

### Other notes
- I think solving this efficiently will require implementing a graph traversal algorithm.  Essentially we need to know the shortest path between all pairs of nodes, and then count (for each node) the number of nodes within `distanceThreshold`.  Then we return the node with the most reachable nodes (and if there's a tie, pick the one with the max ID value)
- On [Wikipedia's entry on shortest path graph problems](https://en.wikipedia.org/wiki/Shortest_path_problem) we can see a few options:

![Screenshot 2024-07-25 at 10 43 44 PM](https://github.com/user-attachments/assets/894ed832-b1d2-4118-85a7-a752700c4aea)
- Of these, either the Floyd-Warshall algorithm or Johnson's algorithm will give us the shortest paths between all pairs of nodes.  The entry says Johnson's algorithm is faster on sparse graphs, but we don't know whether the graph is actually sparse.  Let's just pick whatever looks easier to implement.
- The [Floyd-Warshall algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm) looks straightforward:

![Screenshot 2024-07-25 at 10 46 21 PM](https://github.com/user-attachments/assets/6ae7c96b-ba02-4a04-956d-db28c3652cc5)

- [Johnson's algorithm](https://en.wikipedia.org/wiki/Johnson%27s_algorithm) isn't quite as clearly described:

![Screenshot 2024-07-25 at 10 47 07 PM](https://github.com/user-attachments/assets/8ffade42-0d62-4216-bb0d-b4ebd0f6289b)

So...let's just go with the Floyd-Warshall algorithm.
- I think we're good to implmeent this now


## Attempted solution(s)
```python
class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # Implement the Floyd-Warshall algorithm following Wikipedia's pseudocode...
        # First: initialize the distances to infinity
        dists = [[float('inf')] * n for _ in range(n)]
        
        # The distance from each node to itself is zero
        for i in range(n):
            dists[i][i] = 0
        
        # Add the edges (bidirectionally)
        for u, v, w in edges:
            dists[u][v] = w
            dists[v][u] = w
        
        # Fill in the shortest path between all pairs
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dists[i][j] > dists[i][k] + dists[k][j]:
                        dists[i][j] = dists[i][k] + dists[k][j]

        # now loop through each node and keep track of the city wth the minimum number of neighbors (and max ID, of those)
        min_neighbors = float('inf')
        city = -1

        for i in range(n):
            # count neighbors and update the minimum if needed
            neighbors = sum([d <= distanceThreshold for d in dists[i]])

            if (neighbors < min_neighbors) or ((neighbors == min_neighbors) and (i > city)):
                min_neighbors = neighbors
                city = i

        return city
```
- Given test cases pass
- Submitting...

![Screenshot 2024-07-25 at 10 59 05 PM](https://github.com/user-attachments/assets/ca8088b1-f988-4fed-80a0-08a8970e6d17)

Solved!
