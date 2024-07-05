Thoughts:
* run through each node
* check if it's an extreme
* if extreme, compare index to previous extreme to check for min distances
* also compare index to first extreme index, this will always increase so no need to compare

```python
class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:       
        min_dist = 10**5
        max_dist = 0
        prev_index = None
        node = head
        n = 1
        while node.next.next:
            if (node.val < node.next.val > node.next.next.val) or (node.val > node.next.val < node.next.next.val):
                if prev_index is None:
                    first_extreme = n
                else:
                    min_dist = min(min_dist, n - prev_index)
                    max_dist =  n - first_extreme
                prev_index = n
            node = node.next
            n+=1

        if max_dist == 0:
            return [-1,-1]
        else:
            return [min_dist, max_dist]
```
