# [Problem 1028: Recover a Tree From Preorder Traversal](https://leetcode.com/problems/recover-a-tree-from-preorder-traversal/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The input is a single string encoding a preorder traversal where each node is represented by D dashes (depth) followed by its value. I need to reconstruct the binary tree. The natural first step is to parse the string into a sequence of (depth, value) pairs. Once I have the pairs in preorder, I can reconstruct the tree using a stack that keeps the current path from root to the current node. For each new node with depth d, the parent should be the node on the stack at depth d-1. If the stack is longer than d, I pop until its length equals d (so top of stack is parent). Then I attach as left child if parent's left is empty, otherwise as right child, then push node onto stack.

This stack-based approach feels straightforward and linear time. Another approach could be recursive parsing with an index and expected depth, but the stack approach is simpler to implement and reason about.

## Refining the problem, round 2 thoughts
Edge cases:
- Multi-digit values (need to parse numbers).
- The first node has depth 0 (root).
- The traversal guarantees that if a node has only one child it is the left child, so when attaching a child we try left first then right.
- Depths in the input should never jump in ways impossible for a tree; still, stack popping until correct depth is robust.
Complexity: parsing the string is O(n) where n is string length; constructing nodes and stack operations are O(m) where m is number of nodes. Total time O(n) (n ~ length of traversal) and space O(m) for the stack and nodes.

I'll implement parsing by scanning the string: count consecutive '-' for depth, then parse consecutive digits for value. Then apply stack reconstruction.

## Attempted solution(s)
```python
# Definition for a binary tree node (LeetCode standard).
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

def recoverFromPreorder(traversal: str) -> Optional[TreeNode]:
    # Parse traversal into list of (depth, value) pairs
    n = len(traversal)
    i = 0
    nodes = []  # list of (depth, value)
    while i < n:
        depth = 0
        while i < n and traversal[i] == '-':
            depth += 1
            i += 1
        # parse number (value)
        val = 0
        start = i
        while i < n and traversal[i].isdigit():
            val = val * 10 + (ord(traversal[i]) - ord('0'))
            i += 1
        # Add parsed pair
        nodes.append((depth, val))

    # Reconstruct tree using a stack that holds the path of nodes
    stack = []
    root = None
    for depth, val in nodes:
        node = TreeNode(val)
        if depth == 0:
            # this is the root
            root = node
            stack = [node]
            continue
        # Ensure stack length equals depth (parent at depth-1 is stack[depth-1])
        while len(stack) > depth:
            stack.pop()
        parent = stack[-1]
        # attach as left if empty, else as right
        if parent.left is None:
            parent.left = node
        else:
            parent.right = node
        stack.append(node)

    return root
```
- Notes:
  - Approach: parse traversal into (depth, value) pairs, then use a stack to maintain the current root-to-node path and attach each node to its parent based on depth.
  - Time complexity: O(L) where L is the length of the traversal string (parsing) plus O(N) for node attachments; overall O(L) ~ O(N) where N is number of characters or nodes.
  - Space complexity: O(N) for storing nodes/pairs and the stack (N = number of nodes).
  - Implementation details: parsing handles multi-digit values. The stack pop loop ensures the top of stack corresponds to the parent at depth-1. When attaching, left child is preferred per problem statement; if left exists, attach to right.