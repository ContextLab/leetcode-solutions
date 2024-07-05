# [Problem 2058: Find the Minimum and Maximum Number of Nodes Between Critical Points](https://leetcode.com/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points)

## Initial thoughts (stream-of-consciousness)
- will need to find nodes with larger node on either side, and smaller node on either side
- first and last node can't be critical nodes
- "*Given a linked list `head`...*" -- I assume `head` is the head of the linked list rather than an object that stores the full list
- I assume there's a "trick" to the optimal way of doing this (maybe some sort of sliding window?) but let's try the naïve approach first. Rough steps:
  - iterate through the list (starting with the second node), keeping track of current, previous, and next nodes in the list.
    - stopping criterion: when next node's `.next` attr is `None`
  - store indices of discovered critical nodes
    - any reason to differentiate betewen mins and maxes? I don't think so...
  - at the end, if <2 critical nodes found, return [-1, -1]
  - otherwise, we need to find the min and max difference between indices in that list
    <!-- - **then subtract 1** because we actually need to find the number of nodes *between* the two (see example 2) -->

## Refining the problem

I think I can speed up my initial solution by tracking the min distance between critical nodes while iterating through the linked list, rather than storing all indices and then finding it after via a second for loop. For the min, I'll need to keep track of the most recent critical node's index, so that when I find a critical node, I can compute the distance between the two, and update the current min distance if it's smaller. I'll also need to store the index of the first critical node, because it and the last critical node will be used to compute the max distance.

## Attempted solution(s)

### Attempt 1
```python
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        critical_ixs = []
        prev = head
        curr = head.next
        next_ = curr.next
        curr_ix = 1

        while next_:
            if prev.val < curr.val > next_.val or prev.val > curr.val < next_.val:
                critical_ixs.append(curr_ix)

            prev = curr
            curr = next_
            next_ = next_.next
            curr_ix += 1

        if len(critical_ixs) < 2:
            return [-1, -1]
        if len(critical_ixs) == 2:
            return [critical_ixs[1] - critical_ixs[0]] * 2

        max_diff = critical_ixs[-1] - critical_ixs[0]
        min_diff = 10e6   # fun fact: specifying in scientific notation uses less memory than explicit 10000000

        for i, crit_ix in enumerate(critical_ixs[:-1]):
            min_diff = min(critical_ixs[i+1] - crit_ix, min_diff)

        return [min_diff, max_diff]
```
![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/ac27fb6e-318f-4237-89b2-8687cc447d81)

### Attempt 2

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        prev = head
        curr = head.next
        next_ = curr.next
        curr_ix = 1
        first_critical_ix = False
        min_diff = 10e6
        prev_critical_ix = -10e6

        if next_ is None:
            return [-1, -1]

        while next_:
            if prev.val < curr.val > next_.val or prev.val > curr.val < next_.val:
                first_critical_ix = first_critical_ix or curr_ix
                min_diff = min(curr_ix - prev_critical_ix, min_diff)

                prev_critical_ix = curr_ix

            prev = curr
            curr = next_
            next_ = next_.next
            curr_ix += 1

        if min_diff == 10e6 or prev_critical_ix == -10e6:
            return [-1, -1]

        return [min_diff, prev_critical_ix - first_critical_ix]
```
![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/2159fca6-45d2-466b-871b-60c6c96fe74f)
