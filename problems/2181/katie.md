# [Problem 2181: Merge Nodes In Between Zeros](https://leetcode.com/problems/merge-nodes-in-between-zeros/description/)

## Initial thoughts (stream-of-consciousness)
Essentially I want to hang on to each zero node, and progressively check the next nodes. Every node that isn't zero, the sum should be added to the OG node and then should be dropped out of the list by making a new link between the OG node and the nextnext node. 
When we get to another 0, we want to repeat this process.

## Refining the problem
The final 0 is annoying... I'll add a statement where if the next.next is None, then break out of the loop

## Attempted solution(s)
```
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def mergeNodes(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        node = head
        while node.next != None:
            if node.next.val != 0:
                node.val += node.next.val
                node.next = node.next.next
            else:
                if node.next.next == None:
                    node.next = None
                    break
                node = node.next
        return head
```
<img width="609" alt="Screen Shot 2024-07-04 at 4 18 32 PM" src="https://github.com/KatieONell/leetcode-solutions/assets/12962290/68480f6c-a1ee-4745-888b-dcbc7ac9ceab">
