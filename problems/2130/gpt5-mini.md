# [Problem 2130: Maximum Twin Sum of a Linked List](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum sum of pairs where the i-th node is paired with (n-1-i)-th node. The list length is even. Straightforward ways:
- Convert linked list to array of values, then compute max(values[i] + values[n-1-i]) for i in [0, n/2). Simple and easy (O(n) time, O(n) extra space).
- In-place approach: find the middle, reverse the second half, then walk from head and reversed second half simultaneously to compute sums. This uses O(1) extra memory and O(n) time. After computing, we could restore the list by reversing again (not required for this problem).

The in-place approach is preferred for lower space.

## Refining the problem, round 2 thoughts
Edge cases: n is guaranteed even and at least 2, so no worry about odd lengths or empty list. For even n, the slow/fast pointer technique (advance slow by 1 and fast by 2) will leave slow at the start of the second half when the loop exits, which is exactly where we want to reverse. After reversing the second half, pair nodes from the start and from the reversed half until the reversed half is exhausted (n/2 steps).

Time complexity: O(n) (one pass to find middle, one pass to reverse, one pass to compute sums). Space complexity: O(1) extra (in-place).

I'll implement the in-place method. I'll not restore the list afterward because LeetCode does not require it.

## Attempted solution(s)
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def pairSum(self, head: 'ListNode') -> int:
        # Find middle (start of second half) using slow/fast pointers
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Reverse the second half starting from slow
        prev = None
        curr = slow
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        # prev is head of reversed second half
        
        # Compute maximum twin sum by pairing from head and prev
        max_sum = 0
        p1 = head
        p2 = prev
        while p2:  # exactly n/2 iterations
            max_sum = max(max_sum, p1.val + p2.val)
            p1 = p1.next
            p2 = p2.next
        
        return max_sum
```
- Notes:
  - Approach: find middle, reverse second half in-place, then pairwise sum nodes from the front and the reversed back half to compute the maximum twin sum.
  - Time complexity: O(n) — one pass to find middle, one to reverse, one to compute sums.
  - Space complexity: O(1) extra space (in-place reversal).
  - The solution mutates the input list by reversing the second half; if restoring the original list is required, reverse the second half again after computing the sums.