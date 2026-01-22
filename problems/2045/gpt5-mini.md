# [Problem 2045: Second Minimum Time to Reach Destination](https://leetcode.com/problems/second-minimum-time-to-reach-destination/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the second smallest time to reach node n from 1, not just the shortest. Graph is unweighted in terms of edges (uniform traversal time), but traffic lights introduce time-dependent waiting so travel times depend on current time. A common technique for "k-th shortest path" (here k=2) is to record up to k best arrival times per node and do a Dijkstra-like exploration ordered by current arrival time (min-heap). Each time we pop an arrival time for a node, if it's a new distinct arrival and the node has fewer than two recorded times, append it and expand neighbors. For each neighbor, compute the next arrival considering waiting due to red lights. Stop when we have recorded two distinct arrival times for node n. Must be careful to avoid recording duplicate equal times.

This feels like: maintain times[node] list (at most 2), heap of (time, node). Compute wait as: if floor(time / change) % 2 == 1 -> currently red, wait until next multiple of change; else no wait. Add edge traversal time after waiting.

## Refining the problem, round 2 thoughts
- Use adjacency list for graph.
- Use min-heap to always expand the smallest available arrival time first so that we discover times in increasing order.
- For each popped (t, u):
  - If we already have this t recorded for u (duplicate), skip.
  - If we already have two times for u, skip.
  - Otherwise append t to times[u]. If u == n and times[n] has length 2 -> done, return t.
  - For each neighbor v, compute waiting due to traffic signals at u at time t, then arrival = t + wait + edge_time, and push (arrival, v) into heap (but only if v does not already have two recorded times — it's okay to push and filter later).
- Edge cases: identical arrival times should not be counted twice; must ensure we record only distinct times. Also the journey can revisit vertices many times but we only need two smallest arrivals per node, so bound on work is O(m * 2) expansions.
- Complexity: Each node accepted at most twice, and each edge considered at most twice, so time ~ O((n + m) log (n + m)). Space O(n + m).

## Attempted solution(s)
```python
import heapq
from collections import defaultdict
from typing import List

class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], edge_time: int, change: int) -> int:
        # Build adjacency list
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # times[i] will store up to two distinct arrival times at node i (in increasing order)
        times = [[] for _ in range(n + 1)]

        # Min-heap of (current_time, node)
        heap = [(0, 1)]  # start at node 1 at time 0

        while heap:
            t, u = heapq.heappop(heap)

            # Skip if we already recorded this exact arrival time for u
            if times[u] and t == times[u][-1]:
                continue
            # If already have two times for u, ignore further arrivals
            if len(times[u]) == 2:
                continue

            # Record this arrival time
            times[u].append(t)

            # If we reached destination with two distinct times, return the second
            if u == n and len(times[u]) == 2:
                return t

            # Expand neighbors
            for v in adj[u]:
                # Determine waiting time due to traffic signal at node u at time t
                cycle = t // change
                wait = 0
                if cycle % 2 == 1:  # currently red
                    wait = (cycle + 1) * change - t
                depart = t + wait
                arrive = depart + edge_time

                # If v already has two recorded arrival times, skip pushing (optimization)
                if len(times[v]) < 2:
                    heapq.heappush(heap, (arrive, v))

        # Problem guarantees connectivity and there will be a second minimum, but return -1 as fallback
        return -1
```
- Notes about the solution:
  - Approach: Dijkstra-like search using a min-heap, but store up to two distinct arrival times per node. Expand arrivals in increasing time order so the first two recorded for node n are the minimum and second minimum times.
  - Waiting logic: at time t, signals flip every 'change' minutes starting green at t=0. If floor(t/change) is odd, it's red and you must wait until the next multiple of change.
  - Complexity:
    - Time: O((n + m) log (n + m)) in practice because each node is accepted at most twice and each incident edge processed at most twice; heap operations dominate.
    - Space: O(n + m) for adjacency and storing up to two times per node plus heap.
  - Implementation detail: ensure we treat equal arrival times as duplicates and do not count them separately. The solution returns when the second distinct arrival time for node n is recorded.