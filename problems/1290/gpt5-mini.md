# [Problem 1290: Convert Binary Number in a Linked List to Integer](https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The linked list gives bits from most-significant (head) to least-significant (tail). A straightforward way is to traverse the list left-to-right and build the integer as we go: for each bit, shift the current value left by 1 (multiply by 2) and add the bit. That avoids storing the bits or reversing the list. Another simple approach would be to collect bits into a string and use int(string, 2), but that adds string overhead. Since the number of nodes ≤ 30, performance isn't critical, but the shifting method is clean and O(1) extra space.

Recursion is also possible (compute value of tail and combine), but iterative is simpler and avoids recursion depth reasoning (though depth ≤ 30 so it's safe). Edge-case: list could be just one node (0 or 1). The problem states list is non-empty.

## Refining the problem, round 2 thoughts
I'll implement the iterative bit-accumulation approach:
- Initialize result = 0.
- For each node value b: result = (result << 1) | b (or result = result * 2 + b).
- Return result at the end.

This is O(n) time (one pass) and O(1) extra space. Alternative string-based approach would be O(n) time and O(n) space. Recursion would be O(n) time and O(n) call-stack space. Given constraints, iterative bit shifting is simplest and most efficient.

Edge cases: single-node list, all zeros (should return 0), leading zeros (handled naturally). No need for special checks for empty since constraints say non-empty; I'll still write code that would return 0 if head is None.

## Attempted solution(s)
```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def getDecimalValue(self, head: ListNode) -> int:
        """
        Traverse the linked list from head (most-significant bit) to tail,
        shifting the accumulated value left by 1 and adding the current bit.
        """
        value = 0
        node = head
        while node:
            value = (value << 1) | (node.val & 1)
            node = node.next
        return value

# Example usage:
# Construct linked list [1,0,1] -> should return 5
# n3 = ListNode(1)
# n2 = ListNode(0, n3)
# n1 = ListNode(1, n2)
# print(Solution().getDecimalValue(n1))  # Output: 5
```
- Approach: Iterative accumulation using bit shifting: value = (value << 1) | bit.
- Time complexity: O(n), where n is the number of nodes (single pass).
- Space complexity: O(1) extra space (only a few variables regardless of input size).
- Implementation notes: Using bitwise OR with node.val ensures the bit is added cleanly; node.val is guaranteed to be 0 or 1 per constraints. The method also safely returns 0 if head is None.