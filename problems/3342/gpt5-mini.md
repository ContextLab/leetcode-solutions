# [Problem 3342: Find Minimum Time to Reach Last Room II](https://leetcode.com/problems/find-minimum-time-to-reach-last-room-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimum time to reach (n-1, m-1) in a grid where moving to an adjacent room alternates costs 1,2,1,2,... starting with 1 for the first move. Each cell moveTime[i][j] is the earliest time when you are allowed to start moving into that cell. You can wait arbitrarily at your current room before starting a move.

This looks like a shortest-path problem on a graph where nodes are (i, j, parity) — parity capturing whether the next move cost is 1 or 2 (i.e., how many moves done so far mod 2). From a state (i,j,p), you can go to neighbor (ni,nj,1-p) with:
- start_time = max(current_time, moveTime[ni][nj]) (you may wait)
- travel_time = 1 if p == 0 else 2
- arrival_time = start_time + travel_time

So Dijkstra on n*m*2 states should work. Need to be careful about performance since n,m up to 750 (so ~1.1M states). Use a heap, early exit when we pop the target state for the first time.

## Refining the problem, round 2 thoughts
Edge cases:
- We start at (0,0) at t=0 with parity 0 (next move costs 1).
- Waiting does not change the parity (parity depends on number of moves taken).
- moveTime can be large up to 1e9, but arithmetic fits in Python ints.
- There is always a way to wait and then move (no forbidden waiting), so the Dijkstra approach will find a solution.

Complexity:
- States: 2 * n * m
- Each state has up to 4 outgoing edges.
- Dijkstra with a binary heap: O((n*m) log (n*m)) up to constants.
- Memory: O(n*m) for dist array.

Implementation details:
- dist[i][j][p] = best time to reach (i,j) when next move cost parity is p (p=0 => next cost 1).
- Start with dist[0][0][0] = 0.
- Use heap of (time, i, j, p).
- When popping a target cell (n-1,m-1) for the first time we can return its time (Dijkstra's property).
- If we finish without popping target (shouldn't happen), return min(dist[target][0], dist[target][1]).

## Attempted solution(s)
```python
import heapq

class Solution:
    def minimumTime(self, moveTime):
        n = len(moveTime)
        m = len(moveTime[0])
        INF = 10**30

        # dist[i][j][p]: min time to be at (i,j) with next move parity p (0 -> next cost 1, 1 -> next cost 2)
        dist = [[[INF, INF] for _ in range(m)] for __ in range(n)]
        dist[0][0][0] = 0  # start at (0,0), next move cost is 1
        heap = [(0, 0, 0, 0)]  # (time, i, j, parity)

        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        target_i, target_j = n-1, m-1

        while heap:
            t, i, j, p = heapq.heappop(heap)
            # stale entry
            if t != dist[i][j][p]:
                continue
            # if we reached target, this is the minimal time overall (first pop)
            if i == target_i and j == target_j:
                return t

            move_cost = 1 if p == 0 else 2
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m:
                    # must start moving at time >= moveTime[ni][nj]
                    start = t if t >= moveTime[ni][nj] else moveTime[ni][nj]
                    arrival = start + move_cost
                    np = 1 - p
                    if arrival < dist[ni][nj][np]:
                        dist[ni][nj][np] = arrival
                        heapq.heappush(heap, (arrival, ni, nj, np))

        # Fallback (shouldn't be needed)
        return min(dist[target_i][target_j][0], dist[target_i][target_j][1])
```
- Approach: Dijkstra on (i,j,parity) states. From a state, for each neighbor compute earliest start time (max(current_time, moveTime[neighbor])) and then add the move duration (1 or 2) depending on parity; update neighbor state with flipped parity.
- Time complexity: O(n*m*log(n*m)) in the worst case (two states per cell).
- Space complexity: O(n*m) for distance storage plus heap overhead.
- Important detail: We return as soon as we pop the target state from the heap because that pop gives the globally minimum arrival time for that state, and since we want the minimum over both parities, the first popped target (either parity) is the answer due to the monotonicity of Dijkstra.