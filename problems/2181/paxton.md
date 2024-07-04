# [Problem 2181: Merge Nodes in Between Zeros](https://leetcode.com/problems/merge-nodes-in-between-zeros/description)

## Initial thoughts (stream-of-consciousness)
- start off by iterating through the linked list from the head node
- whenever we encounter a node with a `.val` of 0, start incrementing a running total of node values beginning with the next node
- when we reach another 0-value node:
  - construct a `ListNode` whose `.val` is the running total (and `.next` is `None`, for now)
  - if this is the first `ListNode` we've created, it's the head node we need to return at the end...
  - ...otherwise, the last node we made needs to point to it -- so set *that* node's `.next` to this new `ListNode`
  - store the newly created `ListNode` so that we can update its `.next` the next time we create a new node (if we do)
  - reset the running total and keep going
- the last `ListNode` in the input list will have a `.next` of `None`, so we can iterate over the input list using a `while` loop with that as our stopping condition.
  - but since that will break the loop before we can create the last `ListNode` from the current running total, we'll need to create the last one after the loop breaks

## Refining the problem

## Attempted solution(s)
```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr_input_node = head.next
        curr_sum = 0
        while curr_input_node.next is not None:
            if curr_input_node.val == 0:
                new_merged_node = ListNode(val=curr_sum)
                try:
                    prev_merged_node.next = new_merged_node
                except NameError:
                    new_head_node = new_merged_node
                curr_sum = 0
                prev_merged_node = new_merged_node
            else:
                curr_sum += curr_input_node.val

            curr_input_node = curr_input_node.next

        try:
            prev_merged_node.next = ListNode(val=curr_sum)
        except NameError:
            new_head_node = ListNode(val=curr_sum)

        return new_head_node
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/bd8a392e-113c-48de-a3f7-ae5217980630)

That's kinda slow... there's definitely a more efficient way to do this; might revisit this one at some point.
