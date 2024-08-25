# [Problem 145: Binary Tree Postorder Traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- A nice easy one today!  This is just a depth-first search

## Refining the problem, round 2 thoughts
- Nothing too tricky here.  The order should be "left, right, root"
- I think we can just return the visited notes in reverse order

## Attempted solution(s)
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        vals = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node is not None:
                vals.append(node.val)            
                stack.extend([node.left, node.right])
        return vals[::-1]
```
- Given test cases pass
- New test case:
    - `root = [1,null,2,3, 4, 5, 6, 7, null, 8, null, 9, 10, -100, -100]`: pass
- Let's submit...

![Screenshot 2024-08-24 at 8 59 51 PM](https://github.com/user-attachments/assets/ace94bdb-eab7-409d-a465-469f71e73edb)

- Solved!
