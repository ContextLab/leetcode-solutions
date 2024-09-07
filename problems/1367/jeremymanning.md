# [Problem 1367: Linked List in Binary Tree](https://leetcode.com/problems/linked-list-in-binary-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- First we need to find all nodes in the tree whose values match the head of the linked list's value.  These are "candidate starts of paths."
- Then, for each candidate:
    - Start with the head of the linked list, and the candidate node.  If we ever reach a point where the linked list node's `next` value is `None`, return `True`.
    - Otherwise, if any of the children of the current binary tree node have the same value as the current linked list's next node, then move along in the linked list to the next node, and move along in the tree to the corresponding child.
        - Tricky special case: if *both* children match, then we need to enqueue *both* options.  So actually, maybe the queue of possible paths should include touples of the place to start in the linked list and the place to start in the binary tree.  That way we can just keep adding possibilities until they're all exhausted.  (Or...maybe we should add options in a stack instead of a queue, since that way shorter paths will appear near the end and can be more quickly eliminated?)
    - If *neither* of the current binary tree node's children match the next linked list node, continue on to the next path possibility
    - If we ever run out of options (stack is empty), return `False`

## Refining the problem, round 2 thoughts
- I think this is a straightforward approach.  We can start with a breadth-first search to seed the stack.

## Attempted solution(s)
```python
from collections import deque
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubPath(self, head: Optional[ListNode], root: Optional[TreeNode]) -> bool:
        # first find all possible starts of the tree path, using BFS of the tree
        options = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                continue
            if node.val == head.val:
                options.append((node, head))
            queue.extend([node.left, node.right])

        # now use DFS of all possible options
        while options:
            next_root, next_head = options.pop()
            if next_head.next is None:
                return True
            if next_root.left is not None and next_root.left.val == next_head.next.val:
                options.append((next_root.left, next_head.next))
            if next_root.right is not None and next_root.right.val == next_head.next.val:
                options.append((next_root.right, next_head.next))
        
        return False
```
- Given test cases pass
- I'm in a rush tonight, so I'm just going to submit!

![Screenshot 2024-09-06 at 10 02 01 PM](https://github.com/user-attachments/assets/90897c63-7c1d-4d7b-ab6a-fb98000c62b2)

Great, it worked!

