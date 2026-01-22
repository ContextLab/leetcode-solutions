# [Problem 2181: Merge Nodes in Between Zeros](https://leetcode.com/problems/merge-nodes-in-between-zeros/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The list begins and ends with 0, and there are no two consecutive zeros. That suggests the list is partitioned into segments that start after a 0 and end at the next 0. For each such segment we need a single node whose value is the sum of that segment. Sounds like a straightforward single-pass accumulation: scan nodes, accumulate values until you hit a 0, then emit a node with the accumulated sum and reset.

I could either construct a new linked list of sums or try to reuse nodes in-place (e.g., write the sum into the first node after a zero and skip others). Building a new list is simpler and safe. Time should be O(n). Space is O(k) for the new list (k = number of segments), which is <= n.

Edge cases: the head is 0 so start from head.next; the final zero ends the last segment. Because values are non-negative and there are no adjacent zeros, each segment sum will be > 0, so we will always emit nodes for segments.

## Refining the problem, round 2 thoughts
- Start iterating from head.next to skip the initial 0. Keep a running sum.
- When node.val == 0, create a new node with the sum and append to result list, reset sum to 0.
- Continue until reaching the end (final zero will trigger creating the last segment node).
- No need to create nodes for zeros; they are delimiters only.
- Complexity: O(n) time, O(k) extra nodes where k = number of segments (k <= n/2 roughly).
- Alternatives: in-place modification to reuse nodes and avoid allocations — doable but more error-prone; building a new list is clear and acceptable given constraints.

## Attempted solution(s)
```python
# Definition for singly-linked list.
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: 'Optional[ListNode]' = None):
        self.val = val
        self.next = next

class Solution:
    def mergeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Dummy head for the result list
        dummy = ListNode(0)
        tail = dummy
        
        current = head.next  # skip initial 0
        acc = 0
        
        while current:
            if current.val == 0:
                # end of a segment: emit accumulated sum as a new node
                tail.next = ListNode(acc)
                tail = tail.next
                acc = 0
            else:
                acc += current.val
            current = current.next
        
        return dummy.next
```
- Notes:
  - Approach: single pass, accumulate values between zeros, create a new node with each segment sum when a zero delimiter is encountered.
  - Time complexity: O(n), where n is the number of nodes in the input list (we visit each node once).
  - Space complexity: O(k) for the output list containing k summed nodes (k is the number of segments between zeros), plus O(1) extra auxiliary space.
  - Implementation detail: start from head.next because head is guaranteed to be 0; the final zero in the input triggers creation of the final summed node.