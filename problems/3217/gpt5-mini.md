# [Problem 3217: Delete Nodes From Linked List Present in Array](https://leetcode.com/problems/delete-nodes-from-linked-list-present-in-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to remove from a linked list every node whose value appears in nums. The straightforward idea is to check each node against a fast membership structure built from nums (a set). Using a set gives O(1) average membership checks. For deleting nodes in a singly-linked list, I have to carefully handle deletions at the head and consecutive deletions. A common pattern is to create a dummy head and maintain a previous pointer; when current node's value is in the set, skip it by prev.next = cur.next, otherwise advance prev. Alternatively I could build a new list consisting only of nodes not in the set (which is essentially equivalent). Edge cases to watch: deleting the original head(s), multiple consecutive deletions, and the guarantee that at least one node remains not in nums simplifies things a bit (we won't return None).

## Refining the problem, round 2 thoughts
Use a hash set for nums for O(1) membership. Use a dummy node pointing to head to simplify head deletions. Iterate once through the linked list; for each node:
- if value in set: skip it by not moving prev (prev.next = cur.next)
- else: move prev to cur
Always advance cur to next node after handling current.
Time complexity O(n + m) where n is number of nodes and m is len(nums). Space complexity O(m) for the set (plus O(1) extra pointers). Alternative: rebuild new list via tail pointer which is equivalent in complexity. Make sure to handle contiguous deletions and head deletions — dummy handles that.

## Attempted solution(s)
```python
# Definition for singly-linked list.
from typing import Optional, List

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

class Solution:
    def deleteNodes(self, nums: List[int], head: Optional[ListNode]) -> Optional[ListNode]:
        remove_set = set(nums)
        dummy = ListNode(0, head)
        prev = dummy
        cur = head

        while cur:
            if cur.val in remove_set:
                # skip current node
                prev.next = cur.next
            else:
                prev = cur
            cur = cur.next

        return dummy.next
```
- Notes:
  - Approach: Build a set from nums for O(1) membership checks. Use a dummy node and two-pointer traversal (prev and cur) to remove nodes in-place by skipping them.
  - Time complexity: O(n + m) where n is the number of nodes in the linked list and m = len(nums).
  - Space complexity: O(m) for the set; O(1) additional extra space for pointers.
  - Implementation detail: Using a dummy head removes the need for special-case logic when the original head must be deleted. When deleting, prev does not advance so consecutive deletions are handled correctly.