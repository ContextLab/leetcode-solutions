# [Problem 3372: Maximize the Number of Target Nodes After Connecting Trees I](https://leetcode.com/problems/maximize-the-number-of-target-nodes-after-connecting-trees-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have two trees. For every node i in the first tree, we must connect that node i to some single node j in the second tree (we can choose j to maximize the number of nodes within distance ≤ k from i in the combined graph). We then return the maximum count for each i independently.

Observations:
- In a tree, distances between nodes are unique and can be computed by BFS from each node.
- Adding a single bridge i↔j between the trees can change distances:
  - Distances between nodes inside the same original tree remain at most as before; going out to the other tree and back would require traversing the bridge twice (cost +2) so it cannot shorten any intra-tree shortest path.
  - Distances from i (in tree1) to nodes in tree2 after adding edge (i,j) are simply 1 + dist2[j][v].
  - So the number of nodes reachable from i within k after linking to j is:
      count1(i) = number of nodes u in tree1 with dist1[i][u] ≤ k (independent of j)
      count2(j) = number of nodes v in tree2 with dist2[j][v] ≤ k-1 (depends only on j and k)
    Therefore answer[i] = count1(i) + max_j count2(j).

This simplifies the problem a lot: precompute counts per node in each tree and combine.

## Refining the problem, round 2 thoughts
- We only need for tree1: count1[i] for radius k.
- For tree2: count2[j] for radius k-1 (if k == 0 then this is zero).
- Both trees have up to 1000 nodes, so BFS from each node (O(V+E) each) is acceptable: overall time O(n^2 + m^2) which is fine for 1000.
- Edge cases:
  - k = 0: tree2 contributes nothing; answer[i] should be number of nodes in tree1 within distance 0 (i.e., 1).
  - k = 1: tree2 contributes nodes at distance 0 from chosen j (i.e., itself), so count2[j] = 1 for every j.
- Implementation detail: build adjacency lists, BFS from every node but stop exploring beyond the given limit to save time.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def maximizeTheNumberOfTargetNodes(self, edges1: List[List[int]], edges2: List[List[int]], k: int) -> List[int]:
        # Derive n and m from edges lengths
        n = len(edges1) + 1
        m = len(edges2) + 1

        # Build adjacency lists
        adj1 = [[] for _ in range(n)]
        for a, b in edges1:
            adj1[a].append(b)
            adj1[b].append(a)

        adj2 = [[] for _ in range(m)]
        for u, v in edges2:
            adj2[u].append(v)
            adj2[v].append(u)

        def counts_within_radius(adj: List[List[int]], radius: int) -> List[int]:
            # If radius < 0, no nodes are reachable
            if radius < 0:
                return [0] * len(adj)

            N = len(adj)
            res = [0] * N
            for s in range(N):
                # BFS from s up to given radius
                dist = [-1] * N
                q = deque([s])
                dist[s] = 0
                cnt = 1  # s itself (dist 0 <= radius)
                while q:
                    u = q.popleft()
                    du = dist[u]
                    # explore neighbors only if du < radius (so neighbor dist <= radius)
                    if du < radius:
                        nd = du + 1
                        for w in adj[u]:
                            if dist[w] == -1:
                                dist[w] = nd
                                # If nd <= radius we count and may push
                                if nd <= radius:
                                    cnt += 1
                                    q.append(w)
                res[s] = cnt
            return res

        # count1: number of tree1 nodes within distance k from each node i
        count1 = counts_within_radius(adj1, k)
        # count2: number of tree2 nodes within distance k-1 from each node j
        count2 = counts_within_radius(adj2, k - 1)

        max_count2 = max(count2) if count2 else 0

        # For each i in tree1, best is count1[i] + max_count2
        ans = [c1 + max_count2 for c1 in count1]
        return ans
```
- Approach: BFS from each node in each tree to compute how many nodes lie within the required radius. Use the observation that connecting node i in tree1 to node j in tree2 only affects distances from i to nodes in tree2 (they become 1 + dist2[j][v]), and intra-tree distances in tree1 remain the same. So maximize over j reduces to adding the best count2 (independent of i).
- Time complexity: O(n*(n + edges1) + m*(m + edges2)) = O(n^2 + m^2) in worst case (trees have O(n) edges each). For n, m ≤ 1000 this is acceptable.
- Space complexity: O(n + m) for adjacency lists plus O(max(n, m)) per BFS temporary arrays.
- Important detail: when radius < 0 (k == 0 implies radius for tree2 = -1) we return zeros for tree2 counts.