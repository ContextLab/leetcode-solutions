# [Problem 2322: Minimum Score After Removals on a Tree](https://leetcode.com/problems/minimum-score-after-removals-on-a-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks us to remove two edges from a tree to produce three components, compute the XOR of node values in each component, and minimize the difference between the largest and smallest XORs. A brute force over all possible pairs of edges could be done by splitting the tree each time, but re-computing component XORs explicitly would be expensive.

Observation: removing an edge in a tree splits it into a subtree (the child side) and the rest. If we root the tree (say at 0) and compute subtree XORs for every node, then any single-edge removal corresponds to removing the connection to a node's parent and yields component XOR equal to that node's subtree XOR. For two removed edges (between parent-child for two child nodes a and b), there are three relative positions:
- a is ancestor of b (or vice versa): then the three components are subtree(b), subtree(a) minus subtree(b), and the rest (total XOR ^ subtree(a)).
- a and b are in disjoint subtrees: components are subtree(a), subtree(b), and the rest (total XOR ^ subtree(a) ^ subtree(b)).

Thus if we precompute subtree XORs and an ancestor test (tin/tout timestamps), we can iterate over all pairs of child nodes (n-1 choices each) and compute the resulting three XORs in O(1) per pair. That gives O(n^2) time which is acceptable since n ≤ 1000.

## Refining the problem, round 2 thoughts
Edge cases:
- Root has no parent, so we only consider nodes with a parent as the "cut" endpoint (that's n-1 possible edges).
- Must not pick the same edge twice — iterating pairs of distinct child nodes handles that.
- XOR properties: the XOR of the remainder can be derived as totalXor ^ subtreeXor[...] (or ^ both for two disjoint subtrees).

Complexity:
- Building adjacency and one DFS to compute parent, tin, tout, subtreeXor: O(n).
- Iterating over all pairs of edges (represented by child endpoints) costs O(n^2).
- Overall time O(n^2), space O(n).

This approach is straightforward to implement and fits constraints.

## Attempted solution(s)
```python
from typing import List
import sys
sys.setrecursionlimit(10000)

class Solution:
    def minimumScore(self, nums: List[int], edges: List[List[int]]) -> int:
        n = len(nums)
        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        parent = [-1] * n
        tin = [0] * n
        tout = [0] * n
        subtree_xor = [0] * n
        time = 0

        def dfs(u: int, p: int):
            nonlocal time
            parent[u] = p
            time += 1
            tin[u] = time
            sx = nums[u]
            for v in g[u]:
                if v == p:
                    continue
                dfs(v, u)
                sx ^= subtree_xor[v]
            subtree_xor[u] = sx
            time += 1
            tout[u] = time

        dfs(0, -1)
        total_xor = subtree_xor[0]

        # collect nodes that represent child-side of an edge (i.e., nodes with parent != -1)
        nodes = [i for i in range(n) if parent[i] != -1]
        ans = float('inf')

        def is_ancestor(a: int, b: int) -> bool:
            # returns True if a is ancestor of b (in rooted tree)
            return tin[a] <= tin[b] and tout[b] <= tout[a]

        m = len(nodes)
        for i in range(m):
            a = nodes[i]
            for j in range(i + 1, m):
                b = nodes[j]
                if is_ancestor(a, b):
                    # a ancestor of b
                    x1 = subtree_xor[b]
                    x2 = subtree_xor[a] ^ subtree_xor[b]
                    x3 = total_xor ^ subtree_xor[a]
                elif is_ancestor(b, a):
                    # b ancestor of a
                    x1 = subtree_xor[a]
                    x2 = subtree_xor[b] ^ subtree_xor[a]
                    x3 = total_xor ^ subtree_xor[b]
                else:
                    # disjoint subtrees
                    x1 = subtree_xor[a]
                    x2 = subtree_xor[b]
                    x3 = total_xor ^ subtree_xor[a] ^ subtree_xor[b]

                mx = max(x1, x2, x3)
                mn = min(x1, x2, x3)
                ans = min(ans, mx - mn)

        return ans
```
- Approach notes: Root the tree, compute subtree XOR for each node and Euler tin/tout timestamps for ancestor checks. Represent each removable edge by its child node (node with parent). For every pair of such child nodes, determine relative positions (ancestor/disjoint) and compute the three component XORs in O(1). Track the minimum difference.
- Time complexity: O(n^2) due to iterating over all pairs of edges; computing subtree XORs and timestamps is O(n).
- Space complexity: O(n) for adjacency list, parent, subtree_xor, tin/tout arrays.