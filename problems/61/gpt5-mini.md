# [Problem 61: Rotate List](https://leetcode.com/problems/rotate-list/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to rotate a singly linked list to the right by k places. The naive approach would be to move the last node to the front k times, but that could be O(k * n) which is too slow when k is large (k up to 2e9). Observations: rotating by k where k >= n is equivalent to rotating by k % n, so I should compute the length n and reduce k first. If k % n == 0, the list stays the same. If I know the length and the tail, I can connect tail to head to form a circle and then break the circle at the right point to produce the rotated list. Specifically, after making a circular list, the new tail will be at position n - (k % n) - 1 (0-indexed) and the new head at position n - (k % n). Then break tail.next = None and return new head.

## Refining the problem, round 2 thoughts
Edge cases: empty list (head is None), single node, and k == 0. Also handle large k by taking k %= n. Make sure to update pointers carefully to avoid cycles left behind. Time complexity should be O(n) to compute length and perform pointer adjustments; space O(1). Alternative would be to collect nodes in an array and rewire, but that uses O(n) extra space. The circular-list trick is concise and efficient.

## Attempted solution(s)
```python
# Definition for singly-linked list.
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next or k == 0:
            return head

        # Compute length and get tail
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        k %= length
        if k == 0:
            return head

        # Make it circular
        tail.next = head

        # Find new tail: (length - k - 1) steps from head (0-indexed)
        steps_to_new_tail = length - k - 1
        new_tail = head
        for _ in range(steps_to_new_tail):
            new_tail = new_tail.next

        # New head is next of new_tail
        new_head = new_tail.next

        # Break the circle
        new_tail.next = None

        return new_head
```
- Approach: compute list length, reduce k by modulo, connect tail to head to form a circle, walk to new tail, set new head and break the circle.
- Time complexity: O(n) where n is the number of nodes (one pass to compute length, one pass to find new tail).
- Space complexity: O(1) extra space (in-place pointer manipulation).
- Important details: handle empty list or single node early; reduce k with k %= length to avoid unnecessary rotations. Making the list circular simplifies pointer manipulation and avoids extra arrays.