# [Problem 2181: Merge Nodes in Between Zeros](https://leetcode.com/problems/merge-nodes-in-between-zeros/description/)

## Initial thoughts (stream-of-consciousness)
- This seems pretty straightforward...
- I think we can just keep a running sum of the nodes since the previous zero
- Then once we hit another zero, set the value of the current node to the sum
- If there are no more nodes, return the head node
- Any edge cases to consider?
  - If there are two 0s in a row, what should we do?  It looks like that case is not allowed.
  - We also don't need to account for lists that don't have any closing 0s, since the list length must be greater than or equal to 3 and the first and last values are guaranteed to be 0.

## Refining the problem
- I think we can solve this in $O(n)$ time (where $n$ is the number of nodes in the original linked list)

## Attempted solution(s)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
      x = 0
      new_head = ListNode()
      current = new_head
      
      n = head.next
      while n.next is not None:
          if n.val == 0:
              current.val = x
              next_node = ListNode()
              current.next = next_node
              current = current.next
              x = 0
          else:
              x += n.val
          
          n = n.next

      current.val = x
      return new_head
```

- Both given test cases pass
- Trying a new test case: `head = [0, 1, 0, 2, 0, 1, 2, 3, 4, 5, 0, 1, 0, 10, 1000, 1000, 1000, 0, 10, 10, 10, 10, 0]` (also passes)
- Submitting...
  
![Screenshot 2024-07-03 at 10 51 14 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/ce0a50a6-9a97-4a5f-aeb6-68928f49d372)

Solved!


      
