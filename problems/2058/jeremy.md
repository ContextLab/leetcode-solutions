# [Problem 2058: Find the Minimum and Maximum Number of Nodes Between Critical Points](https://leetcode.com/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/description/)

## Initial thoughts (stream-of-consciousness)
- I think we can solve this in $O(n)$ time, where $n$ is the number of nodes in the linked list
- We can go through each node in turn, testing for critical points
- Track the first critical point (for computing max distance)
- Also track the current position in the list and the position of the previous critical point
- Once the next critical point is found:
  - update the position of the previous critical point
  - update the current minimum distance if needed
  - update the maximum distance
- Potentially tricky things to handle:
  - If there are no critical points
  - Only a single critical point
- When the list length is 2, just return [-1, -1]

## Refining the problem
- we'll need to keep track of the previous value, since there's no "self.prev.val" to reference
- we could reduce the numbers of comparisons needed-- if the list goes a --> b --> c --> d and we've already found that b < c when we're at node b, then we don't need to re-compare b and c when we're next on node c.  We could re-use the computation so that we only ever need to do forward comparisons.

## Attempted solution(s)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
    
        i = 2  # current position
        previous_val = head.val
        min_dist = -1
        max_dist = -1
        first_critical_point = -1
        last_critical_point = -1
    
        current = head.next
        while current.next is not None:
            if ((previous_val > current.val) and (current.val < current.next.val)) or ((previous_val < current.val) and (current.val > current.next.val)):
                if last_critical_point != -1:
                    next_dist = i - last_critical_point                    
                    if (min_dist == -1) or (next_dist < min_dist):
                        min_dist = next_dist
                    max_dist = i - first_critical_point
                else:
                    first_critical_point = i
                last_critical_point = i
            i += 1
            previous_val = current.val
            current = current.next
    
        return [min_dist, max_dist]
```

- All given test cases pass
- New test case: head = [1, 2, 1, 2, 1, 2, 3, 4, 5, 6, 7, 6, 7, 5, 1000, 23, 51, 2, 3, 15, 36, 2, 9, 10] (passes)
- Submitting...

![Screenshot 2024-07-04 at 11 39 25 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/1f9eb67c-5e17-435a-94d3-f74b5456c7ce)

Solved!



