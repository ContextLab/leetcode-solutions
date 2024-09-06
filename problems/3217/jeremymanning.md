# [Problem 3217: Delete Nodes From Linked List Present in Array](https://leetcode.com/problems/delete-nodes-from-linked-list-present-in-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Let's start by changing `nums` to a `set` (instead of a `list`) so that we can match each value along the linked list to the values in `nums` in constant time (instead of $O(n)$ time, where $n$ is the length of `nums`)
- I think there are two cases we need to account for:
    - While the head is in `nums`, set `head = head.next`
    - Next, keep looping through the subsequent nodes:
        - If `node.val` is *not* in `nums`, continue to the next node (or return `head` if `node.next` is `None`)
        - If `node.val` *is* in `nums`, we need to snip out the current node by setting `prev.next = node.next`.  So that means we'll also need to keep track of the previous node we've visited

## Refining the problem, round 2 thoughts
- Since we're guaranteed that at least one node is not in `nums`, we don't have to account for the special case where there is no head to return
- The one sort of "tricky" (if it can be called that) piece is how we keep track of the previous node.  I think we can start by setting `prev = head` (once we've skipped ahead to the first node that isn't in `nums`).  Then we can start looping through by setting `current = prev.next` and then continue until `current.next` is `None`.
- Let's try it!

## Attempted solution(s)
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def modifiedList(self, nums: List[int], head: Optional[ListNode]) -> Optional[ListNode]:
        nums = set(nums)

        while head.val in nums:
            head = head.next

        prev = head
        current = head.next
        while current is not None:
            if current.val in nums:
                prev.next = current.next
                current = current.next
            else:
                prev, current = current, current.next

        return head
```
- Given test cases pass
- Off the top of my head I can't think of any particularly interesting edge cases that I'm not accounting for, so I'll just try submitting 🙂

![Screenshot 2024-09-05 at 11 28 53 PM](https://github.com/user-attachments/assets/c26d7769-a6ea-4082-ab19-88872ba8a2e5)

I'll take it!  Solved 🎉!

