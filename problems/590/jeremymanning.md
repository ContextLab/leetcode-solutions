# [Problem 590: N-ary Tree Postorder Traversal](https://leetcode.com/problems/n-ary-tree-postorder-traversal/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- This problem is the same as yesterday's, but with N-ary trees instead of binary trees
- We can solve it the same way:
    - Execute a depth-first  search, saving values to a list as we visit each node
    - Push the root, then the children (left to right) to the stack
    - At the end, return the list of values in reverse order

## Refining the problem, round 2 thoughts
- The problem description doesn't say if all children are guaranteed to be non-null if there's a least one other non-null child of the given node.  I guess we'll need to see what happens when we run the code.

## Attempted solution(s)
```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
"""

class Solution:
    def postorder(self, root: 'Node') -> List[int]:
        vals = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node is not None:
                vals.append(node.val)            
                if node.children is not None:
                    for c in node.children:
                        stack.append(c)
        return vals[::-1]
```
- Given test cases pass
- Let's try some others:
    - `root = []`: pass
    - `root = [1, null, 2, 3, 4, 5, 6, 7, 8, null, 9, 10, 11, 12, null, 13, 14, 15, 16, 17, null, 18, 19, 20, null, null, 21, 22, 23, null, 24]`: pass
- Ok; let's submit!

![Screenshot 2024-08-25 at 10 25 02 PM](https://github.com/user-attachments/assets/b8800303-2301-45f7-bbdc-9ef418d6a659)

Solved 🎉!
