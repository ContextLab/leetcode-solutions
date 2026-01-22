# [Problem 2196: Create Binary Tree From Descriptions](https://leetcode.com/problems/create-binary-tree-from-descriptions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a list of (parent, child, isLeft) triples describing edges in a binary tree with unique node values. The simplest approach is to create a mapping from value -> TreeNode for every value encountered, then link children to parents according to isLeft. To find the root, observe that the root is the one value that never appears as a child. So track which values appear as children; the root is a parent value not in that child set. The input guarantees a valid binary tree so there should be exactly one root.

## Refining the problem, round 2 thoughts
- We need to ensure we create TreeNode objects lazily (when first seen) for both parents and children.
- Use a set to track all child values.
- Use a set or dict keys to track parent values; final root is any parent value that is not in the child set (parents - children).
- Complexity: each description is processed once -> O(n) time, O(n) space for nodes and sets.
- Edge cases: repeated references to the same parent/child are expected (multiple children of same parent). The problem guarantees validity, so we don't need to handle contradictory edges.
- Implementation detail: build nodes dict, children set, parents set; after linking pick root and return its TreeNode.

## Attempted solution(s)
```python
# Definition for a binary tree node (LeetCode standard).
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import List, Optional

class Solution:
    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        nodes = {}      # val -> TreeNode
        children = set()
        parents = set()
        
        for parent, child, isLeft in descriptions:
            if parent not in nodes:
                nodes[parent] = TreeNode(parent)
            if child not in nodes:
                nodes[child] = TreeNode(child)
            
            if isLeft == 1:
                nodes[parent].left = nodes[child]
            else:
                nodes[parent].right = nodes[child]
            
            children.add(child)
            parents.add(parent)
        
        # root is a parent that is never a child
        root_vals = parents - children
        if not root_vals:
            return None
        root_val = next(iter(root_vals))
        return nodes[root_val]
```
- Notes:
  - Approach: Create TreeNode for every value encountered, link according to isLeft, track children, then pick parent not in children as root.
  - Time complexity: O(n), where n = len(descriptions). Each description is processed once and map/set ops are O(1) average.
  - Space complexity: O(n) for the nodes dictionary and the sets.
  - The solution relies on the problem guarantee that the descriptions form a valid binary tree, so (parents - children) will have exactly one element.