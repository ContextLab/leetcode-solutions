# [Problem 2699: Modify Graph Edge Weights](https://leetcode.com/problems/modify-graph-edge-weights/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to assign positive integer weights to all edges originally labeled -1 so that the shortest-path distance from source to destination equals target. We cannot change positive edges. Because the graph is small (n <= 100), repeated Dijkstra runs are fine. The classic approach for this kind of problem is to reason about extremes: treat unknown edges as very large to see the shortest path using only fixed edges, and treat them as smallest (1) to see the minimum possible shortest path. If target lies between those extremes, we can adjust some -1 edges to hit exactly target.

I recall a standard solution:
- Run Dijkstra with -1 considered infinity (effectively ignored) from destination to get distances dist_fixed_to_dest using only fixed edges. If dist_fixed_to_dest[source] < target then impossible (there's already a strictly shorter fixed-only path that can't be increased).
- Run Dijkstra with -1 considered weight 1 from source to get dist_min. If dist_min[destination] > target impossible (even with all -1 = 1 we are too large).
- If dist_fixed_to_dest[source] == target we can set all -1 to a huge value and done.
- Otherwise, run a Dijkstra from source and when relaxing a -1 edge u->v, if using weight 1 yields a path that can still be extended via fixed-only path from v to destination to be <= target, we can set that -1 edge's weight to a computed value so that dist(source->u) + w + dist_fixed_to_dest[v] == target. Use that dynamic weight in Dijkstra. After we finish we verify the resulting full-weight graph yields shortest path equal to target.

## Refining the problem, round 2 thoughts
Key details:
- Must handle undirected edges (add adjacency both ways).
- Need to keep track per-edge assignment for final output (use index of edge).
- Use a very large INF (like 1e18) when treating -1 edges as infinity. For final filler value for unused -1 edges we can set a large allowed value (2*10^9) per problem constraints.
- After constructing the candidate assignment, run one final Dijkstra on the fully assigned graph to be safe and ensure shortest path equals target; otherwise return [].
- Complexity: Each Dijkstra is O(E log V). We'll run a handful (constant) Dijkstras, acceptable for constraints.

Now provide the implementation.

## Attempted solution(s)
```python
import heapq

class Solution:
    def modifiedGraphEdges(self, n, edges, source, destination, target):
        # Build adjacency with edge indices for undirected graph
        adj = [[] for _ in range(n)]
        for i, (u, v, w) in enumerate(edges):
            adj[u].append((v, w, i))
            adj[v].append((u, w, i))

        INF = 10**18
        BIG_FINAL = 2 * 10**9  # allowed maximum value to assign to -1 edges for final output

        def dijkstra(start, neg1_as):
            # neg1_as: integer weight to use for -1 edges (e.g., 1 or INF)
            dist = [INF] * n
            dist[start] = 0
            heap = [(0, start)]
            while heap:
                d, u = heapq.heappop(heap)
                if d != dist[u]:
                    continue
                for v, w, _ in adj[u]:
                    ww = w if w != -1 else neg1_as
                    nd = d + ww
                    if nd < dist[v]:
                        dist[v] = nd
                        heapq.heappush(heap, (nd, v))
            return dist

        # 1) dist when all -1 are INF (effectively ignored) from destination
        dist_to_dest_using_fixed = dijkstra(destination, INF)

        # If fixed-only shortest path < target impossible (can't increase positive edges)
        if dist_to_dest_using_fixed[source] < target:
            return []

        # If fixed-only shortest path == target: set all -1 to BIG_FINAL and return
        if dist_to_dest_using_fixed[source] == target:
            res = []
            for u, v, w in edges:
                if w == -1:
                    res.append([u, v, BIG_FINAL])
                else:
                    res.append([u, v, w])
            return res

        # 2) dist when all -1 are 1 from source (minimum possible)
        dist_min_with_ones = dijkstra(source, 1)
        if dist_min_with_ones[destination] > target:
            return []

        if dist_min_with_ones[destination] == target:
            # set all -1 to 1
            res = []
            for u, v, w in edges:
                if w == -1:
                    res.append([u, v, 1])
                else:
                    res.append([u, v, w])
            return res

        # 3) We know dist_min_with_ones[destination] < target < dist_to_dest_using_fixed[source]
        # Run a custom Dijkstra from source, assigning weights to -1 edges on the fly.
        dist = [INF] * n
        dist[source] = 0
        heap = [(0, source)]
        # assigned_weights for edges (index -> assigned w if we choose >1), initialize None
        assigned = [None] * len(edges)

        while heap:
            d, u = heapq.heappop(heap)
            if d != dist[u]:
                continue
            if u == destination:
                break
            for v, w, idx in adj[u]:
                if w != -1:
                    nd = d + w
                    if nd < dist[v]:
                        dist[v] = nd
                        heapq.heappush(heap, (nd, v))
                else:
                    # Decide weight for this -1 edge when going u -> v
                    # If we can make a path through this edge that equals target using fixed-only path v->dest,
                    # compute required w; otherwise use 1.
                    req = None
                    if dist_to_dest_using_fixed[v] < INF:
                        # want: d + w + dist_to_dest_using_fixed[v] == target => w = target - d - dist_to_dest_using_fixed[v]
                        w_needed = target - d - dist_to_dest_using_fixed[v]
                        if w_needed >= 1:
                            req = w_needed
                    use_w = req if req is not None else 1
                    nd = d + use_w
                    if nd < dist[v]:
                        dist[v] = nd
                        heapq.heappush(heap, (nd, v))
                        # record assignment only if we use a weight > 1
                        if use_w > 1:
                            assigned[idx] = use_w

        # After this Dijkstra, check if we achieved target
        if dist[destination] != target:
            return []

        # Build final edge list: for -1 edges, if we assigned a positive value use it; else set to BIG_FINAL
        res_edges = []
        for i, (u, v, w) in enumerate(edges):
            if w != -1:
                res_edges.append([u, v, w])
            else:
                if assigned[i] is not None:
                    res_edges.append([u, v, assigned[i]])
                else:
                    res_edges.append([u, v, BIG_FINAL])

        # Final verification: ensure shortest path equals target with these assignments
        # Build adjacency for final graph and dijkstra check
        adj_final = [[] for _ in range(n)]
        for i, (u, v, w) in enumerate(res_edges):
            adj_final[u].append((v, w))
            adj_final[v].append((u, w))

        def final_dijkstra(s):
            distf = [INF] * n
            distf[s] = 0
            h = [(0, s)]
            while h:
                dd, uu = heapq.heappop(h)
                if dd != distf[uu]:
                    continue
                for vv, ww in adj_final[uu]:
                    nd = dd + ww
                    if nd < distf[vv]:
                        distf[vv] = nd
                        heapq.heappush(h, (nd, vv))
            return distf

        final_dist = final_dijkstra(source)
        if final_dist[destination] != target:
            return []
        return res_edges
```
- Approach notes:
  - Use multiple Dijkstra runs with different treatments of -1 edges: INF to simulate ignoring them, 1 to simulate minimum possible, and a custom Dijkstra that assigns particular -1 edges a computed weight when beneficial.
  - assigned array stores per-edge special weights chosen during the custom Dijkstra; any remaining -1 edges are set to a large allowed value to avoid creating unintended shorter paths.
  - Complexity: each Dijkstra is O(E log V). We run a constant number of them (3–4), so overall O(E log V). With n ≤ 100 and E up to ~n(n-1)/2 this is efficient. Space O(n + E) for adjacency and helper arrays.
  - Important details: graph is undirected, so edges are added both ways. Use a very large INF when treating -1 as infinity (to avoid overflow but larger than any meaningful path), and use 2*10^9 for final filler values within problem limits. Final Dijkstra validation ensures correctness.