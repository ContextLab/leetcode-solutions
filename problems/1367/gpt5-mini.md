# [Problem 1367: Linked List in Binary Tree](https://leetcode.com/problems/linked-list-in-binary-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check whether the linked list exists as a downward path in the binary tree. The straightforward idea is: for every tree node, try to match the linked list starting from that node, walking down left/right children as the list advances. That suggests a "start-at-every-node" traversal combined with a "match-downwards" check. Worst-case that is O(N * L) where N is number of tree nodes and L is length of the list. I recall there's a more advanced KMP-like method to get closer to O(N + L) by treating list as a pattern, but given constraints (N <= 2500, L <= 100) the straightforward approach is fine. Need to be careful about recursion depth if the tree is skewed (depth up to N), so either use iterative traversal or bump recursion limit.

## Refining the problem, round 2 thoughts
Refinement: implement a helper match(node, listnode) that returns True if the list starting at listnode can be matched starting from tree node by descending via left/right. Then traverse the whole tree and call match at each node. Edge cases: head is None (per constraints head length >= 1 but handle defensively), root is None -> False. Match recursion depth equals list length (<=100), but tree traversal recursion depth can be up to ~2500; set recursion limit higher to be safe. Time complexity O(N * L) worst-case, space complexity O(H) recursion stack (H tree height) plus O(1) extra besides call stack. Mention alternative KMP approach for optimization, but not necessary here.

## Attempted solution(s)
```python
import sys
sys.setrecursionlimit(10000)

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
    def isSubPath(self, head: 'ListNode', root: 'TreeNode') -> bool:
        if not head:
            return True
        if not root:
            return False

        # Try to match the linked list starting at tree node "node"
        def match(node: 'TreeNode', ln: 'ListNode') -> bool:
            if not ln:
                return True
            if not node:
                return False
            if node.val != ln.val:
                return False
            # Continue matching with either left or right child
            return match(node.left, ln.next) or match(node.right, ln.next)

        # Traverse tree and attempt to match at each node
        def dfs(node: 'TreeNode') -> bool:
            if not node:
                return False
            if match(node, head):
                return True
            return dfs(node.left) or dfs(node.right)

        return dfs(root)
```
- Approach: For each tree node, attempt to match the linked list by recursively advancing down left/right children. If any start yields a full match, return True.
- Time complexity: O(N * L) in the worst case, where N is number of tree nodes and L is length of the linked list (each tree node may trigger a match attempt that explores up to L nodes).
- Space complexity: O(H) recursion stack for DFS over the tree (H is tree height). The match recursion uses O(L) stack but L <= 100; to be safe we set recursion limit to handle skewed trees (N up to 2500). 
- Notes: A more advanced solution can reduce worst-case time using a KMP-like automaton built from the linked list, yielding roughly O(N + L) time, but the simpler approach is sufficient given constraints and is easier to implement and reason about.