# [Problem 2096: Step-By-Step Directions From a Binary Tree Node to Another](https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I recognize this as a shortest path in a tree problem where directions are restricted to left, right, and up. The path between two nodes in a tree always goes up from the start to their lowest common ancestor (LCA) and then down from the LCA to the destination. So if I can get the path from the root to start and the root to dest, I can find the common prefix (which corresponds to the path to the LCA), then convert the remaining moves from start's path to 'U' and append remaining moves from LCA to dest. One straightforward approach: find root->start and root->dest paths (strings of 'L'/'R'), compute the longest common prefix index, produce 'U' * (len(startPath) - common) + destPath[common:].

I should be careful about recursion depth for skewed trees (n up to 1e5). A recursive DFS may hit Python recursion limit, so an iterative DFS (using an explicit stack) or BFS is safer for path extraction. Another approach is to build parent pointers and then walk up to find LCA — but building parent pointers also needs some traversal and then computing LCA may require extra work (or converting to ancestor sets). The path-string approach from root is simple and clean.

## Refining the problem, round 2 thoughts
- Implementation detail: implement getPath(root, target) iteratively (stack storing (node, path_string)) to avoid recursion depth issues.
- Complexity: each node will be visited at most once per path search, so two searches -> O(n) time, O(n) space for the worst-case stack/path storage. Could also do a single traversal filling parent pointers and then build paths up to the root for both nodes, then find LCA by comparing reversed paths; that is equivalent complexity.
- Edge cases: start and dest could be root or direct ancestor/descendant. The algorithm handles these naturally: common prefix could be entire startPath (if start is ancestor of dest) or entire destPath (if dest is ancestor of start). startValue != destValue guaranteed.
- Need to ensure getPath returns an empty string if target == root (root->root path is ""), which is fine.

## Attempted solution(s)
```python
# Definition for a binary tree node (provided by LeetCode environment).
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def getDirections(self, root: 'TreeNode', startValue: int, destValue: int) -> str:
        def getPathIter(root, target):
            # Iterative DFS to find path from root to target as a string of 'L'/'R'
            stack = [(root, "")]  # (node, path_from_root)
            while stack:
                node, path = stack.pop()
                if node is None:
                    continue
                if node.val == target:
                    return path
                # push right first so left is processed first (not necessary, but deterministic)
                if node.right:
                    stack.append((node.right, path + "R"))
                if node.left:
                    stack.append((node.left, path + "L"))
            return None  # should not happen if target exists in tree

        startPath = getPathIter(root, startValue)
        destPath = getPathIter(root, destValue)

        # find longest common prefix length
        i = 0
        min_len = min(len(startPath), len(destPath))
        while i < min_len and startPath[i] == destPath[i]:
            i += 1

        # moves up from start to LCA, then follow dest's remaining moves
        ups = "U" * (len(startPath) - i)
        downs = destPath[i:]
        return ups + downs
```
- Notes on approach:
  - We compute the path from root to start and root to destination as strings of 'L' and 'R'.
  - The LCA corresponds to the last common character position in these two paths (their longest common prefix). To go from start to LCA we need one 'U' per remaining step in startPath; then to go from LCA to dest we follow the remaining suffix of destPath unchanged.
- Complexity:
  - Time: O(n) in the worst case. Each getPathIter can traverse much of the tree (at most all nodes), so two traversals -> O(n).
  - Space: O(n) worst-case for the explicit stack and path strings (path length up to tree height).
- Implementation details:
  - getPathIter is iterative to avoid recursion depth limits on skewed trees.
  - The function assumes the tree contains both startValue and destValue (per problem constraints).