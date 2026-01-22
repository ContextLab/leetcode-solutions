# [Problem 2807: Insert Greatest Common Divisors in Linked List](https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to walk the linked list and between every adjacent pair insert a node whose value is gcd(value1, value2). That suggests a single pass through the list where for each node I look at node.next, compute gcd(node.val, node.next.val), create a new ListNode for that gcd and splice it between them. Careful to advance properly so I don't re-process inserted nodes. Edge case: single node — nothing to insert. GCD computation is cheap (values <= 1000). Complexity will be linear in number of nodes (original nodes), with extra O(1) per pair for gcd.

## Refining the problem, round 2 thoughts
Refinements:
- Use math.gcd for correctness and speed.
- When inserting, after splicing the new node, advance current pointer to new.next (the original next node) to continue processing original adjacent pairs.
- Confirm constraints: up to 5000 nodes, node values 1..1000 — no overflow concerns.
- Alternative would be to collect values to a list, build new list with inserted gcds, but that uses extra O(n) space; in-place insertion is simpler and O(1) extra space.
- Time complexity: O(n * cost_gcd) ~ O(n log M) where M <= 1000, practically O(n).
- Space complexity: O(1) extra (not counting output nodes); final list size becomes up to 2n-1 nodes.

## Attempted solution(s)
```python
# Definition for singly-linked list.
from typing import Optional
import math

class ListNode:
    def __init__(self, val: int = 0, next: 'Optional[ListNode]' = None):
        self.val = val
        self.next = next

class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        
        curr = head
        while curr and curr.next:
            nxt = curr.next
            g = math.gcd(curr.val, nxt.val)
            new_node = ListNode(g, nxt)
            curr.next = new_node
            # Advance to the next original node (skip inserted node)
            curr = nxt
        return head
```

- Notes:
  - Approach: iterate original list, compute gcd(curr.val, curr.next.val), insert new node with that gcd between them, then move to the next original node.
  - Time complexity: O(n * log M) where n is number of original nodes and M is max node value (M ≤ 1000). Practically O(n).
  - Space complexity: O(1) extra space (in-place insertion). Output linked list will have up to 2n-1 nodes.
  - Important implementation detail: after insertion set curr = nxt (not curr.next) to skip the inserted node and continue processing original adjacent pairs. This avoids infinite loop or re-processing inserted nodes.