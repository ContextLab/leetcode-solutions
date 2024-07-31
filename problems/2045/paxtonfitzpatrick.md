# [Problem 2045: Second Minimum Time to Reach Destination](https://leetcode.com/problems/second-minimum-time-to-reach-destination/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- okay, this one looks tricky. One initial thought I have is that a path that involves revisiting some node will be the second shortest path only if there aren't two paths that *don't* involve revisiting a node. So I think I can ignore that outside of those specific cases.
- It sounds like we'll need to use some algorithm that finds *all* paths between a target and destination node. Maybe I could write a modified version of BFS (rather than Djikstra since edges are essentially unweighted) where instead of stopping either once all nodes have been visited and the queue is empty, or when it first encounters the target node, it instead stops when it encounters it a second time?
- I'm realizing my inital assumption isn't necessarily true. E.g., we could have a graph like this:
  ```
                               3----------2---------1
                               |                    |
                               4--------------------5
  ```
  so instead maybe instead I could modify the way BFS keeps track of already-visited nodes to avoid revisiting them, such that it's allowed to revisit any node at most once?
  <!-- - actually, that wouldn't work either. For any cap I might put on the number of times the algorithm can revisit a node, it's possible to draw a graph like the one above where the only other path is even longer. -->
- Could I instead allow it to revisit nodes an unlimited number of times? I think theoretically yes, because each time I encounter a node, I'd enqueue all of its neighbors, so even if one or more of the paths I end up checking results in me getting stuck in an endless loop, the others should still be able to complete. It'd just add a lot of "junk" paths to the queue that I'd have to process in order to proces the "reasonable" paths.
  - in fact this would spawn a huge number of "endless loop" paths and end up taking forever, so unfortunately this probably isn't feasible...
- Actually, I think I can get away without doing that... I think tentatively I might've just had epiphany about this one...
  - The whole thing about red lights/green lights, entering but not exiting nodes on red lights, etc. is really just a confusing distraction. All the edges take the same amount of time to traverse, so we'll "hit a red light" and have to pause for `change` minutes after traversing a certain number of edges no matter where we are in the graph when that happens. So really all that matters is the number of steps it takes to get from node $1$ to node $n$. If we can track that, we can just do some math at the end to convert the number of steps taken into time taken, so there's no need to track all the timing stuff as we go.
  - I think the key insight is that for any path from node $1$ to node $n$ that takes $k$ steps, there exists a path that takes $k+2$ steps in which you "double back" and revisit any one node along that path one time. So if I run a BFS to find node $n$ from node $1$ **but** modify the algorithm such that it terminates when it encounters node $n$ the second time (or rather, via a path whose length is strictly greater than that of the first path via which it encounters node $n$), then I can compare the length of the first path $k_1$ to the length of the second path $k_2$, and if $k_2 \gt k_1 + 2$, then the second shortest path involves doubling back one time along the shortest path and is $k_1 + 2$ steps long. Otherwise, it's $k_2$ steps long, where $k_2$ must equal $k_1 + 1$.
  - I'll need to allow the algorithm to visit nodes more than once so that the same node can be used as part of multiple paths (and so node $n$ can be encountered a second time). I think I can do this using the idea I had earlier where I keep track of visited nodes, but instead of flipping them from `False` to `True` when I visit them, I'll keep a count of the number of visits, and allow them to be visited up to 2 times. I think 2 will be the max necessary -- if there's some node that both the shortest and second shortest paths pass through, then the first two times it's visited will be as part of those two paths because of the order in which BFS processes nodes.
  - I'm gonna try to implement this.
  <!-- - Since BFS processes nodes ordered by the number of steps they are from the start, the first time it encounters node n will be via the shortest path, the second time will be via the second shortest path, etc. -->
<!-- - another idea is to do a modified version of Floyd-Warshall, where I initialize a *3D* distances matrix, and instead of overwriting each entry with the new shortest path, I just append it to the list of path lengths between the pair of nodes, then choose the 2nd lowest in each node pair's list at the end.
  - there are a few potential issues I foresee with this though -- first, I'm not sure -->

## Refining the problem, round 2 thoughts

- okay, I think there's another trick I can use to reduce the overall runtime based on the idea above that the second shortest path is either $k_1 + 1$ or $k_1 + 2$ steps. Instead of waiting to terminate the BFS when it encounters node $n$ a second time, I think I can terminate the first time it's encountered, then just check whether node $n$ is currently in the BFS queue with a distance of $k_1 + 1$ (the queue will be `(node, steps_from_node_1)` tuples). If so, then the second shortest path is $k_1 + 1$ steps; otherwise, it's $k_1 + 2$. And since the BFS queue will be ordered by `steps_from_node_1`, I'll only have to check the first few queued nodes up to the first one whose `steps_from_node_1` is $\ge k_1 + 2$. This should greatly reduce the number of nodes I have to process in the BFS, on average.
  - minor addendum: I think it'd be possible for node $n$ to not have been queued yet at this point in the processing of a potential second shortest path, so I should also check whether any *neighbors* of node $n$ are in the queue with a distance of $k_1$.
- I've been thinking there must be an analytical formula I can use to calculate the time taken from the number of steps at the end, but I'm not sure what it is... I don't think it's as simple as (something like) `time_taken = n_steps * time + (n_steps * time // change) * time` because the light can change to red while we're moving from one node to the next, in which case some of the traversal time and waiting-for-green-light time will elapse simultaneously... if I can't figure out a formula that'd give me the answer in $O(1)$ time, I might actually be better off tracking the time during the BFS than doing another loop at the end.
  - Actually, never mind, I do think it'd still be better to calculate it at the end even if I have to do it in a loop, because that'd require only number-of-steps-in-second-shortest-path operations, versus doing it during the BFS would require that same operation for (up to) every node in the graph.
- I think the best way to represent the graph for traversal here will be an adjacency list, so that I can access all neighbors for a given node in constant time.
- edge cases to consider?
  - the constraints say $n$ will always be $\ge 2$, so don't need to worry about node $1$ and node $n$ being the same.
  - if $n = 2$, the second shortest path will automatically be 3, so I guess we could check for that up front and skip the very short BFS we'd otherwise have to run? Not sure that would be worth it.

### Other notes

## Attempted solution(s)

```python
class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:
        # build adjacency list
        adj_list = [[] for _ in range(n)]
        for node1, node2 in edges:
            adj_list[node1 - 1].append(node2 - 1)
            adj_list[node2 - 1].append(node1 - 1)

        # modified BFS:
        queue = deque([(0, 0)])  # (node - 1, steps from node 1)
        visited = [0] * n
        visited[0] = 1
        while queue:
            node, min_steps = queue.popleft()
            if node == n - 1:
                break
            for neighbor in adj_list[node]:
                if visited[neighbor] < 2:
                    visited[neighbor] += 1
                    queue.append((neighbor, min_steps + 1))

        node_n_neighbors = set(adj_list[n - 1])
        for node, second_min_steps in queue:
            if second_min_steps > min_steps + 1:
                second_min_steps = min_steps + 2
                break
            if node == n - 1 and second_min_steps == min_steps + 1:
                break
            if node in node_n_neighbors and second_min_steps == min_steps:
                second_min_steps = min_steps + 1
                break
        else:
            second_min_steps = min_steps + 2

        # calculate time taken
        total_time = 0
        for _ in range(second_min_steps):
            if total_time // change % 2:
                total_time += time + change - total_time % change
            else:
                total_time += time

        return total_time
```

![](https://github.com/user-attachments/assets/dd5481b0-417a-4f94-9b7d-d61807d27a28)

- Hmmmm something's wrong here... the graph is too big to debug manually, but the expected second shortest time is smaller than my answer, so I think that means I'm missing finding a $k_1 + 1$ path when one exists... The only way I can think of for that to happen is if my restriction on the number of times a node can be visited is preventing me from finding a path that involves revisiting a node that's already been visited by two (or more) other iterations.
- So how could I ensure that the two visits each node is allowed are made by the two shortest paths? Maybe instead of my `visited` list containing the number of times each node has been visited, I could have where each element is a 2-item list, (initialized to `[[float('inf'), float('inf')], ...]`), where the first item in each sublist is the min distance from the start node to that node, and the second item is the second (strictly larger) shortest distance. Then I could enqueue each neighbor of each node I encounter if its distance is less than the second shortest distance, and track the first and second smallest? This would sometimes allow more than 2 paths if a later path is shorter than a previous one, and it'd also take up more memory than the count version, but at least it'd work... I think...
  - actually, I think 2 lists of $n$ integers will be smaller in memory than one list of $n$ 2-item lists, so I'll do that.

```python
class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:
        # build adjacency list
        adj_list = [[] for _ in range(n)]
        for node1, node2 in edges:
            adj_list[node1 - 1].append(node2 - 1)
            adj_list[node2 - 1].append(node1 - 1)

        # modified BFS:
        queue = deque([(0, 0)])  # (node - 1, steps from node 1)
        INF = float('inf')
        min_dists = [INF] * n
        second_min_dists = [INF] * n
        while queue:
            node, min_steps = queue.popleft()
            if node == n - 1:
                break
            for neighbor in adj_list[node]:
                if min_steps + 1 == min_dists[neighbor] or min_steps + 1 >= second_min_dists[neighbor]:
                    continue
                queue.append((neighbor, min_steps + 1))
                if min_steps + 1 < min_dists[neighbor]:
                    min_dists[neighbor], second_min_dists[neighbor] = min_steps + 1, min_dists[neighbor]
                else:
                    second_min_dists[neighbor] = min_steps + 1

        # check the queue for the second shortest path
        node_n_neighbors = set(adj_list[n - 1])
        for node, second_min_steps in queue:
            if second_min_steps > min_steps + 1:
                second_min_steps = min_steps + 2
                break
            if node == n - 1 and second_min_steps == min_steps + 1:
                break
            if node in node_n_neighbors and second_min_steps == min_steps:
                second_min_steps = min_steps + 1
                break
        else:
            second_min_steps = min_steps + 2

        # calculate time taken
        total_time = 0
        for _ in range(second_min_steps):
            if total_time // change % 2:
                total_time += time + change - total_time % change
            else:
                total_time += time

        return total_time
```

![](https://github.com/user-attachments/assets/7d85cc19-707c-4ea4-8f7e-82029543b37b)

![](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTNrb2FweXk5bTU2cGlobHdzZnZ3cGUxa2dlNmcxNDlzeHJoY3p5ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/WIg8P0VNpgH8Q/giphy.gif)

yaaaaaaay
