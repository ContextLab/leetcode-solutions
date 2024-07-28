# [Problem 2045: Second Minimum Time to Reach Destination](https://leetcode.com/problems/second-minimum-time-to-reach-destination/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- This is another graph problem (sort of a shortest path problem, but with a few differences)
- There are a few twists in this problem:
    - The red/green traffic signals are going to change how we factor in edge lengths.  We'll have to come up with a way of handling this, but essentially as we traverse a path we need to use the traffic rules to figure out how long it will take.
    - Finding the "second minimum time" is a little trickier than finding the (strict) minimum time.  The standard shortest path algorithms would do something like replacing (in the adjacency matrix) the distances between two vertices if a new path had a shorter distance.  But now I think we need to maintain *two* adjacency matrices: one for the minimum distances, and one for the second minimum distances (i.e., the minimum values that are strictly greater than whatever is in the minimum distance matrix.
- Another important part of the problem is that we don't need to compute the paths between *every* pair of vertices, since we know that the only path that matters is from vertex 1 to vertex $n$.  So instead of the Floyd-Warshall algorithm, which we used for [yesterday's problem](https://github.com/ContextLab/leetcode-solutions/blob/main/problems/2976/jeremymanning.md) and the [day before yesterday's problem](https://github.com/ContextLab/leetcode-solutions/blob/main/problems/1334/jeremymanning.md), I think we should use Dijkstra's algorithm for this problem (but modified as described above).  Pasting in from yesterday's notes, here is the pseudocode for Dijkstra's algorithm:

![Screenshot 2024-07-26 at 11 33 36 PM](https://github.com/user-attachments/assets/e668dcc9-0f82-4b76-a965-45e35a22a72d)

- Ok...so now we have a general approach; let's figure out how to deal with these twists.

## Refining the problem, round 2 thoughts
- Handling traffic rules:
    - We know that all signals start off as green at time 0
    - Let's say that the current signal status when we reach vertex `i` is `isGreen`, and the journey from vertex `i` to `j` takes `x` minutes.  If `isGreen == True` and `x` is between 0 and `change` minutes, the status doesn't change (but now we only have `change - x` minutes before the next transition).  Alternatively, if `change < x <= 2 * change`, then now `isGreen == False` and we'll need to add `y = 2 * change - x` minutes to the journey from `j` to the next destination.  (If `j` is the endpoint-- i.e., vertex $n$, then we don't need to pay that extra cost.)
        - If `isGreen == False` then we need to wait until the signal turns green (this takes `y` minutes, as computed above) and then we proceed as though `isGreen == True`.
        - Only the final (up to) `2 * change` minutes of the journey matter with respect to accounting for traffic rules.  I think we can compute the cost as something like `x + extra`, where `extra` is computed as follows:
            - Start with `extra = 0`
            - If there is time remaining until the signal turns green from the remaining journey (let's call that amount `y`), then `extra += y`.  For the first journey (from vertex 1 to a neighbor) we know that `y == 0`.
            - Then take `remainder = x % (2 * change)`:
                - If `0 <= remainder < change` then keep track of how much less time we have on the *next* journey-- but we can leave the next vertex right away
                - If `change <= remainder < 2 * change` then we arrive when the signal is red, so on the next journey from the destination we'll need to wait `2 * change - remainder` minutes to leave.
    - Ok...so these notes are a little convoluted.  But what I think I'm coming to is that we're going to need to keep track of `greenTimeSpent` (amount of time spent traveling to the current vertex during the most recent green signal-- *if the signal is green when we arrive*; if we arrive when the signal is red, `greenTimeSpent = 0`).  And we also need to keep track of `timeUntilGreen`-- the amount of time left until we can leave the destination vertex.  But `timeUntilGreen` only applies if we arrive when the signal is red; otherwise (if the signal is green), then we set `timeUntilGreen = 0`.  Then, when we're computing travel times between vertices, we want to add `timeUntilGreen` to the stated travel time.  And then we *subtract* `greenTimeSpent` when we need figure out the signal status upon arrival at the destination vertex.
- Finding the second minimum time:
    - In the "standard" Dijkstra's algorithm, we continually replace the path distance from `i` to `j` with alternative smaller values if/when we find them.  But in the "second minimum" version, we'll need to maintain two parallel representations of the path distances:
        - The first representation is the standard minimum path distance
        - The second representation (which stores the second minimums) replaces the path distance from `i` to `j` with an alternative smaller value only if (a) it's smaller than the current distance in the second minimum representation *and* it's strictly greater than whatever the minimum path distance from `i` to `j` is.
- Functions to write:
    - `computeTravelTime(current_time, travel_time)`: returns the time needed to get to the next vertex, accounting for signal status
        - Actually...`travel_time` is always the same, so we can just use `computeTravelTime(current_time)`!
    - Then we just need to implement this modified version of Dijkstra's algorithm (i.e., breadth first search) to find the second minimum time needed to get from vertex 1 to $n$.
- One potential edge case: what if there is only 1 path from vertex 1 to $n$?  Then I think to get the second minimum time, we would need to double back along the trip between the nearest vertices (accounting for signal status)-- e.g., we'd need to add an extra loop (for some adjacent vertices `i` and `j`): `... --> i --> j --> i --> j --> ...`.

## Attempted solution(s)
```python
class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:
        def computeTravelTime(current_time):
            # Calculate effective travel time considering traffic lights
            cycle = 2 * change
            if (current_time // change) % 2 == 1:  # lights are red
                wait_time = cycle - (current_time % cycle)
                return current_time + wait_time + time
            else:  # lights are green
                return current_time + time

        # Build the graph
        graph = [[] for _ in range(n + 1)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        # List to keep track of the minimum and second minimum times to each vertex
        min_times = [[float('inf'), float('inf')] for _ in range(n + 1)]
        min_times[1][0] = 0
        
        # Queue for BFS
        queue = [(0, 1)]  # (current time, current vertex)
        
        while queue:
            curr_time, vertex = queue.pop(0)
            
            # Explore neighbors
            for neighbor in graph[vertex]:
                next_time = computeTravelTime(curr_time)

                if next_time < min_times[neighbor][0]:
                    min_times[neighbor][1] = min_times[neighbor][0]
                    min_times[neighbor][0] = next_time
                    queue.append((next_time, neighbor))
                elif min_times[neighbor][0] < next_time < min_times[neighbor][1]:
                    min_times[neighbor][1] = next_time
                    queue.append((next_time, neighbor))
        
        # Return the second minimum time to reach vertex n
        return min_times[n][1]
```
- Given test cases pass
- I'm out of time for thinking about this; submitting...

![Screenshot 2024-07-27 at 11 34 34 PM](https://github.com/user-attachments/assets/fcc0649a-02de-4839-9045-9f5746a79cd6)

😌 phew!

