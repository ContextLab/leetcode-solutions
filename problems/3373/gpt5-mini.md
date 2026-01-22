# [Problem 3373: Maximize the Number of Target Nodes After Connecting Trees II](https://leetcode.com/problems/maximize-the-number-of-target-nodes-after-connecting-trees-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The phrase "target if the number of edges on the path is even" immediately suggests parity of distances. In a tree all distances parity from any node partition nodes into two groups (even/odd) — i.e., the tree is bipartite. If we connect node i in tree1 to some node t in tree2 by a single new edge, then:
- For nodes x in tree1, distances to i remain the same; x is target iff dist1(i,x) is even.
- For nodes y in tree2, dist(i,y) = 1 + dist2(t,y); so y is target iff dist2(t,y) is odd.

Therefore the total number of targets for i equals:
  (# nodes in tree1 at even dist from i) + (# nodes in tree2 at odd dist from chosen t).

In any tree, nodes at even distance from a node are exactly the nodes in the same bipartition color as that node. So for tree1, for node i the even-count = size of color class of i. For tree2, for a chosen t the odd-count = size of the opposite color class of t. There are only two color class sizes in tree2, so picking the best t simply gives the larger of those two class sizes.

So answer[i] = size_of_color_class_in_tree1_for_i + max(color_count_tree2).

This leads to an O(n+m) algorithm: bipartition both trees (BFS/DFS), get color sizes, then compute answers.

## Refining the problem, round 2 thoughts
Edge cases:
- Trees are connected, n,m >= 2 so BFS/DFS from node 0 covers the whole tree (but I'll still code robustly).
- Use iterative traversal to avoid recursion limits for large inputs.
- Complexity target: O(n + m) time and O(n + m) memory for adjacency lists and color arrays.

No other constraints (like restricting which t can be chosen per i) — queries are independent — so the simple formula holds for every i.

## Attempted solution(s)
```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def maxValueAfterConnectingTrees(self, edges1: List[List[int]], edges2: List[List[int]]) -> List[int]:
        # Build adjacency lists
        n = len(edges1) + 1
        m = len(edges2) + 1
        g1 = [[] for _ in range(n)]
        g2 = [[] for _ in range(m)]
        for a,b in edges1:
            g1[a].append(b)
            g1[b].append(a)
        for u,v in edges2:
            g2[u].append(v)
            g2[v].append(u)

        # Helper: BFS to color a tree (0/1) and count sizes, return colors list and counts tuple
        def bipartite_color(adj):
            length = len(adj)
            color = [-1] * length
            counts = [0,0]
            # Graph is a tree (connected), so single component; but still loop for safety
            for start in range(length):
                if color[start] != -1:
                    continue
                dq = deque([start])
                color[start] = 0
                counts[0] += 1
                while dq:
                    u = dq.popleft()
                    for v in adj[u]:
                        if color[v] == -1:
                            color[v] = color[u] ^ 1
                            counts[color[v]] += 1
                            dq.append(v)
            return color, counts

        color1, counts1 = bipartite_color(g1)
        color2, counts2 = bipartite_color(g2)

        max_odd_in_tree2 = max(counts2)  # as explained, best odd-count we can get from tree2

        ans = [0] * n
        for i in range(n):
            ans[i] = counts1[color1[i]] + max_odd_in_tree2

        return ans

# Example usage:
# sol = Solution()
# print(sol.maxValueAfterConnectingTrees([[0,1],[0,2],[2,3],[2,4]], [[0,1],[0,2],[0,3],[2,7],[1,4],[4,5],[4,6]]))
```
- Approach notes: color both trees into two bipartition classes. For a node i in tree1 the number of nodes at even distance equals the size of the color class of i. For tree2, the number of nodes at odd distance from a chosen node t equals the size of the opposite color class of t; maximizing that across t gives the larger bipartition size. So answer[i] = size(color_of_i in tree1) + max(size color0 in tree2, size color1 in tree2).
- Time complexity: O(n + m) to build adjacencies and traverse both trees.
- Space complexity: O(n + m) for adjacency lists and color/count arrays.