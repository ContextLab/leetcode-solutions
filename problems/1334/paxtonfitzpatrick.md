# [Problem 1334: Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- I feel like this is one of those problems that's supposed to cue you to some particular algorithm that I'm just not familiar with. I'll probably end up googling for this eventually, but I wanna take a stab at a solution first.
- okay so to answer the problem I need to find the number of other nodes within `distanceThreshold` of each node. My first thought is I could do a DFS (BFS?) from each node where I stop going down a particular path when I reach the threshold distance, but that seems like it'd be slow...
- I could reduce the overall number of paths upfront by dropping any whose weights are greater than the threshold distance, because I know they'll never contribute to a viable path anyway. This would require an additional $O(n)$ operation to filter the initial edge list, but if `distanceThreshold` is low, it could easily pay off. There are even a few instances of this in the examples, so I feel like it's something we're meant to notice.
  - actually, I'll need to iterate through the list of edges at least once to build the graph anyway, so I could just filter out the edges that are too long as I go. So this wouldn't add a whole extra $O(n)$ operation and is definitely worth doing, I think
- hmmm... another scenario potentially worth accounting for: if a node has no edges to any other nodes, then I know that 0 is the smallest number of neighbors. I'm not even sure whether they'd include a case like this, but it feels conspicuous that we're given `n` in addition to the `edges` list -- if all `n` nodes were necessarily in `edges`, `n` would be redundant.
- let's switch over to a different part of the problem -- I'll need some way of representing the graph to traverse it. I think this format will likely follow the traversal method I come up with, but my initial thought is to create a dict where keys are the IDs for each node and their values are a lists of (neighbor, edge weight) tuples.
- maybe the DFS approach would be manageable with some sort of caching or memoization? E.g., I could do a normal DFS for the first node I search from (up to `distanceThreshold`), and then store distances from that node to all nodes within `distanceThreshold` of it. Then whenever I DFS from another node and encounter that one, I can check that record instead of going further down that path.
  - actually I'm not sure this would end up being faster... I'll end up checking more nodes than I would have if I'd just done a normal DFS because some within `distanceThreshold` of the node whose record I check won't be within `distanceThreshold` of the node I'm searching from. Might've helped if this were a binary tree, but since it's a graph I'll also end up checking lots of nodes via both DFS and other nodes' records
  - then again, if some node is within `distanceThreshold` of the node I'm currently DFSing from via the node whose record I'm checking and via some other route, I'd have ended up checking it twice anyway via 2 DFSes instead of 1 DFS + 1 record check... so maybe the savings of being able to stop the DFS for a certain path when I hit a node with record data would outweigh the extra checks I'd do because of it? I'm not sure...
- maybe there's a more efficient way to take advantage of work already done? This idea of considering nodes as "waypoints" to compare different paths seems promising -- i.e., "is the path between node `a` and node `b` via node `c` shorter than the path between them via node `d`/the shortest path between them I've found so far?" But to get to a point where I could check that I'd have to already know the distance between node `d` and each other node... which is the problem I'm trying to solve in the first place. So I'm not sure how to get there.
- what if I represented the minimum distance between each pair of nodes in a 2D array (upper and lower triangles would be duplicates... maybe I can optimize that away?). Then for each node in the graph `i`, for each of its neighbors `j`, for each node in the graph `k`, I could check whether the path from `i` to `k` via `j` is shorter than `distances_matrix[i][k]`, and update it if so.
  - hmmm though I'm not sure whether this would work for graphs with nodes separated by > 2 degrees... that doesn't show up in any of the example graphs.
- okay I ended up googling around and it turns out this is basically the "Floyd-Warshall algorithm"! I just needed to make `j` all nodes in the graph instead of just the neighbors of `i`. I'll try implementing that now... though since the algorithm has $O(n^3)$ time complexity, I'm still not sure whether this would actually be more efficient than the BFS/DFS approach...


## Refining the problem, round 2 thoughts

Given the way the Floyd-Warshall algorithm works, I don't think it'll be worth removing edges > `distanceThreshold` from the initial `edges` list because it wouldn't save us any checks during the main processing of the pairwise distances. However, since the algorithm takes $O(n^3)$ time, I *do* think it'll be worth checking upfront whether any nodes have no edges to any other nodes, because that would take comparatively little time, I think

## Attempted solution(s)

```python
class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # initialize min distances matrix
        min_dists = [[float('inf')] * n for _ in range(n)]
        # set to keep track of nodes with no edges
        no_edges = set(range(n))
        # add weights from edges list, remove nodes with edges from set
        for from_node, to_node, weight in edges:
            min_dists[from_node][to_node] = weight
            min_dists[to_node][from_node] = weight
            no_edges.discard(from_node)
            no_edges.discard(to_node)
        # if any nodes have no edges, return the one with the greatest ID
        if no_edges:
            return max(no_edges)
        # # set diagonal to 0 -- actually, not needed since we skip the diagonal
        # # in the main loop anyway
        # for i in range(n):
        #     min_dists[i][i] = 0
        # run Floyd-Warshall
        for via_node in range(n):
            for from_node in range(n):
                for to_node in range(n):
                    if from_node == to_node:
                        continue
                    dist_via_intermediate = min_dists[from_node][via_node] + min_dists[via_node][to_node]
                    if dist_via_intermediate < min_dists[from_node][to_node]:
                        min_dists[from_node][to_node] = dist_via_intermediate
        # find highest-numbered node with fewest reachable nodes within distanceThreshold
        min_reachable = n
        for node_id, dists in enumerate(min_dists):
            reachable = sum(1 for dist in dists if dist <= distanceThreshold)
            if reachable <= min_reachable:
                min_reachable = reachable
                min_reachable_node = node_id
        return min_reachable_node
```

![](https://github.com/user-attachments/assets/f4fb89c1-536b-454e-a7e7-a89b8b9c4e20)
