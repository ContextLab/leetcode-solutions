# [Problem 725: Split Linked List in Parts](https://leetcode.com/problems/split-linked-list-in-parts/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- There are two parts to this problem: figuring out the sizes of each list segment and actually doing the splitting
- Let's consider how to solve each in turn

## Refining the problem, round 2 thoughts
- To figure out the sizes of the segments, I think we can:
    - First, figure out how long the list is with an initial pass through the list.  Let's say the length is `n`.
    - We can then compute a "base" size of each segment as `n // k`.  This is the "default" segment length, and it's also the minimum segment lenght.
    - But some of the segments might need to be augmented by 1 additional element.  The number of segments that need augmenting is `n % k`.  We can create an `extra = n % k` variable, and then while `extra > 0` we augment the given segment with an additional element and then decrement `extra`.
- Splitting the segments requires setting the `next` property of the last element of the previous segment to `None` and then appending the first element of the next segment to the to-be-outputted list of segments.
- Note: I'm assuming that the output should be a list of heads of each segment's linked list, as opposed to "regular" (`list`) lists of the values of each segment's nodes
- Assuming that this is the desired output format, I think I'm ready to implement the solution

## Attempted solution(s)
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        # first compute the length of the list
        n = 0
        node = head
        while node is not None:
            node = node.next
            n += 1

        # now compile the actual segments
        base_length = n // k
        extras = n % k

        segments = []
        node = head
        
        for i in range(k):
            part_head = node
            part_length = base_length + (1 if extras > 0 else 0)
            extras -= 1 if extras > 0 else 0

            # finish off this segment
            for j in range(part_length - 1):
                if node:
                    node = node.next
            
            # tie off the current segment and get ready for the next one
            if node:
                next_part = node.next
                node.next = None
                node = next_part

            segments.append(part_head)

        return segments
```
- Given examples pass
- Submitting...

![Screenshot 2024-09-07 at 10 10 14 PM](https://github.com/user-attachments/assets/1c36ab06-c7e2-4b34-88f0-278f96c97e2d)

Solved!

