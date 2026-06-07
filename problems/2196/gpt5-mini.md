# [Problem 2196: Create Binary Tree From Descriptions](https://leetcode.com/problems/create-binary-tree-from-descriptions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't provide my internal stream-of-consciousness, but here's a concise summary of my initial thoughts and approach: build the tree by creating TreeNode objects for every value seen, use the descriptions to attach children to parents (left or right), track which nodes appear as children, and finally pick the node that never appears as a child as the root.

## Refining the problem, round 2 thoughts
Refinements and considerations:
- The input guarantees a valid binary tree, so there will be exactly one root (a node that never appears as a child).
- We'll lazily create TreeNode objects when we first encounter a value (parent or child).
- Keep a set of child values to identify the root after processing all descriptions.
- Complexity: each description is processed once, so time is O(n) and space O(n) where n = number of descriptions (or unique nodes).
- Edge cases: single description, node values large (up to 1e5) — but using dict keyed by value handles that fine.

## Attempted solution(s)
```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def createBinaryTree(self, descriptions: list[list[int]]) -> TreeNode:
        # map value -> TreeNode
        nodes = {}
        children = set()
        parents = set()
        
        for parent_val, child_val, is_left in descriptions:
            if parent_val not in nodes:
                nodes[parent_val] = TreeNode(parent_val)
            if child_val not in nodes:
                nodes[child_val] = TreeNode(child_val)
            
            parent_node = nodes[parent_val]
            child_node = nodes[child_val]
            
            if is_left == 1:
                parent_node.left = child_node
            else:
                parent_node.right = child_node
            
            children.add(child_val)
            parents.add(parent_val)
        
        # root is a parent that is not any node's child
        root_candidates = parents - children
        root_val = root_candidates.pop()  # guaranteed by problem constraints
        return nodes[root_val]
```
- Notes:
  - Approach: create node objects on demand, attach children based on descriptions, track children set, pick parent not in children as root.
  - Time complexity: O(n) where n = len(descriptions) (each description processed once, dict operations average O(1)).
  - Space complexity: O(m) where m = number of unique node values (<= 2 * n); used for nodes dictionary and children set.
  - Implementation detail: the problem guarantees validity, so there will be exactly one root candidate; using pop() on the set is safe.