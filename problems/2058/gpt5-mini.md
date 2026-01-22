# [Problem 2058: Find the Minimum and Maximum Number of Nodes Between Critical Points](https://leetcode.com/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find nodes that are local minima or maxima in a singly linked list. A node can only be critical if it has both a previous and a next node, so the first and last nodes are never critical. I can traverse the list once, checking for each middle node whether its value is strictly greater than both neighbors (local max) or strictly smaller than both neighbors (local min). I should collect the positions (indices) of all critical points. Once I have indices, the minimum distance between any two critical points is the minimum difference between consecutive indices, and the maximum distance is the difference between the last and first critical indices. If fewer than two critical points exist, return [-1, -1].

## Refining the problem, round 2 thoughts
- Use a single pass (O(n)) and O(k) extra space to store critical indices (k = number of critical points).
- Use 1-based indexing to match examples.
- Edge cases:
  - List length < 3 -> no critical points -> return [-1, -1].
  - Equal neighbor values cannot form a strict local min/max.
- After collecting indices, if len(indices) < 2 return [-1,-1]. Otherwise:
  - minDistance = min(difference between consecutive indices)
  - maxDistance = indices[-1] - indices[0]
- This is straightforward and efficient.

## Attempted solution(s)
```python
# Definition for singly-linked list.
# Provided by LeetCode; included here for completeness.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

from typing import Optional, List

class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        # If fewer than 3 nodes, no critical points possible
        if not head or not head.next or not head.next.next:
            return [-1, -1]
        
        indices = []
        prev = head
        curr = head.next
        idx = 2  # curr is node #2 in 1-based indexing
        
        while curr.next:
            nxt = curr.next
            # check local max or local min
            if (curr.val > prev.val and curr.val > nxt.val) or (curr.val < prev.val and curr.val < nxt.val):
                indices.append(idx)
            # move forward
            prev = curr
            curr = nxt
            idx += 1
        
        if len(indices) < 2:
            return [-1, -1]
        
        # min distance between consecutive critical points
        min_dist = min(indices[i] - indices[i-1] for i in range(1, len(indices)))
        # max distance between first and last critical point
        max_dist = indices[-1] - indices[0]
        
        return [min_dist, max_dist]
```

- Notes about the solution:
  - Approach: Single-pass traversal to identify critical points and record their 1-based positions. Compute min distance as minimum gap between consecutive critical indices and max distance as gap between first and last critical index.
  - Time complexity: O(n), where n is the number of nodes, because we visit each node at most once.
  - Space complexity: O(k), where k is the number of critical points (worst-case O(n) but typically much smaller). The extra space holds the list of critical indices.
  - Important details: Use strict comparisons for maxima/minima (>, <). First and last nodes are never considered because they lack both neighbors.