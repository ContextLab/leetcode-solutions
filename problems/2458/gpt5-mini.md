# [Problem 2458: Height of Binary Tree After Subtree Removal Queries](https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the tree height after removing a subtree rooted at some node, for many independent queries. Naively removing a subtree and recomputing height per query is too slow (O(n) per query). I recall two common directions: (1) use Euler tour + data structures to find the maximum depth outside an interval, or (2) do a tree DP / rerooting to precompute, for every node u, the maximum depth among nodes outside u's subtree. The rerooting approach sounds promising: compute for each node the maximum depth in its subtree, then propagate "best outside" values down to children by combining parent's outside value and sibling subtree maxima. That should let answering each query in O(1).

So plan: 1) DFS to compute depth (distance from root) and subtree_max (deepest depth within subtree). 2) Another DFS to compute up_max[u] = deepest depth among nodes not in u's subtree using parent's up_max and siblings' subtree_max. Then query answer for u is up_max[u] (depth measured as edges from root).

## Refining the problem, round 2 thoughts
Details to work out:
- Represent depth as number of edges from root (root depth = 0). subtree_max[u] stores the max depth (absolute) of any node in u's subtree.
- For child v of parent u, nodes outside v's subtree include: nodes outside u's subtree (up_max[u]), the parent u itself (depth[u]), and subtrees of u's other children. So up_max[v] = max(up_max[u], depth[u], max(subtree_max[sibling] for siblings)).
- To compute max over siblings efficiently, for each node compute prefix and suffix max arrays over its children subtree_max values.
- Ensure recursion limits or use iterative DFS because n up to 1e5. I'll set recursionlimit high.
- Complexity: two DFS traversals O(n), answering m queries O(m). Space O(n).

Edge cases:
- queries[i] != root (guaranteed), so up_max[query] always defined and at least 0.
- Tree nodes labeled 1..n uniquely, so mapping by value straightforward.

## Attempted solution(s)
```python
# LeetCode submission code (Python 3)

# Definition for a binary tree node (provided by LeetCode).
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

import sys
sys.setrecursionlimit(300000)

class Solution:
    def treeQueries(self, root: 'TreeNode', queries: 'List[int]') -> 'List[int]':
        # Maps indexed by node value (1..n)
        depth = {}         # depth[val] = distance from root (edges)
        subtree_max = {}   # subtree_max[val] = maximum depth (absolute) within val's subtree
        children = {}      # children[val] = list of child values
        
        # First DFS: build children, compute depth and subtree_max
        def dfs1(node, d):
            val = node.val
            depth[val] = d
            children[val] = []
            # initialize subtree_max to own depth
            maxd = d
            if node.left:
                children[val].append(node.left.val)
                dfs1(node.left, d+1)
                maxd = max(maxd, subtree_max[node.left.val])
            if node.right:
                children[val].append(node.right.val)
                dfs1(node.right, d+1)
                maxd = max(maxd, subtree_max[node.right.val])
            subtree_max[val] = maxd
        
        dfs1(root, 0)
        
        # Second DFS: compute up_max (max depth outside subtree)
        up_max = {}  # up_max[val] = maximum depth (absolute) among nodes not in val's subtree
        # for root, nothing outside
        up_max[root.val] = -10**9
        
        def dfs2(u):
            ch = children[u]
            k = len(ch)
            # precompute prefix and suffix maxima of subtree_max for children
            pref = [ -10**9 ] * k
            suff = [ -10**9 ] * k
            for i in range(k):
                v = ch[i]
                val = subtree_max[v]
                pref[i] = val if i == 0 else max(pref[i-1], val)
            for i in range(k-1, -1, -1):
                v = ch[i]
                val = subtree_max[v]
                suff[i] = val if i == k-1 else max(suff[i+1], val)
            # propagate to children
            for i in range(k):
                v = ch[i]
                # max subtree among siblings excluding v
                left_max = pref[i-1] if i-1 >= 0 else -10**9
                right_max = suff[i+1] if i+1 < k else -10**9
                sibling_max = max(left_max, right_max)
                # up_max for child v
                up_max[v] = max(up_max.get(u, -10**9), depth[u], sibling_max)
                dfs2(v)
        
        dfs2(root.val)
        
        # Answer queries: removing subtree rooted at q -> height is max depth among nodes not in subtree = up_max[q]
        ans = []
        for q in queries:
            ans.append(up_max[q])
        return ans
```
- Notes about approach:
  - We treat depths as absolute depths (edges from root). subtree_max[u] is the deepest absolute depth inside u's subtree.
  - up_max[u] is computed by combining the parent's up_max, the parent's own depth, and the max subtree_max among the parent's other children (siblings).
  - Two DFS traversals give O(n) time and O(n) space. Answering m queries is O(m).
  - Time complexity: O(n + m). Space complexity: O(n) for maps and recursion stack.
  - Recursion limit increased to handle deep trees; iterative DFS could be used instead if preferred.