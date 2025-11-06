"""
Common data structures used in LeetCode problems.
"""

from typing import Optional


class TreeNode:
    """
    Definition for a binary tree node.
    This is the standard TreeNode class used in LeetCode binary tree problems.
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


class ListNode:
    """
    Definition for singly-linked list node.
    This is the standard ListNode class used in LeetCode linked list problems.
    """
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"ListNode({self.val})"
