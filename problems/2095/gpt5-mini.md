# [Problem 2095: Delete the Middle Node of a Linked List](https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to remove the "middle" node defined as floor(n/2) using 0-based indexing. The straightforward ways:
- Count nodes in a first pass, compute middle index, then a second pass to remove that index. That's simple and guaranteed correct.
- Two-pointer (slow/fast) technique can locate the middle in one pass: advance fast by 2 and slow by 1; keep a pointer to the node before slow so we can unlink slow when fast reaches the end.
The two-pointer approach is preferable since it does the job in a single traversal and O(1) extra space. Edge cases: list of length 1 -> return None; ensure we handle small lengths (2,3) correctly.

## Refining the problem, round 2 thoughts
Using slow/fast:
- Initialize slow = head, fast = head, prev = None.
- While fast and fast.next: set prev = slow, slow = slow.next, fast = fast.next.next.
- At loop exit, slow points to the middle node (floor(n/2) index) and prev is the node before it (unless list length is 1, prev stays None).
- If prev is None, we're deleting head -> return head.next.
- Otherwise, unlink with prev.next = slow.next and return head.

Complexity:
- Time O(n) single pass.
- Space O(1).
Alternative: two-pass counting method also O(n) time but needs two passes; slightly simpler but less optimal in passes (still linear).

## Attempted solution(s)
```python
# Definition for singly-linked list.
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: 'Optional[ListNode]' = None):
        self.val = val
        self.next = next

class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # If there's only one node, deleting the middle results in an empty list.
        if head is None or head.next is None:
            return None
        
        prev = None
        slow = head
        fast = head
        
        # Move fast by 2 and slow by 1; prev tracks node before slow.
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        
        # slow is the middle node; remove it by skipping it.
        if prev:
            prev.next = slow.next
        else:
            # prev None only happens if list had 1 element (handled above), but keep safe fallback.
            head = head.next
        
        return head
```
- Notes:
  - This uses the standard fast/slow pointer pattern. After the loop, slow points to the floor(n/2)-th node (0-based) which we remove.
  - Time complexity: O(n) — one traversal of the list.
  - Space complexity: O(1) — only a few pointers used.
  - Handles the edge case n = 1 by returning None immediately.