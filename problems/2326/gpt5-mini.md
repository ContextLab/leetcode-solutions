# [Problem 2326: Spiral Matrix IV](https://leetcode.com/problems/spiral-matrix-iv/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to fill an m x n matrix in clockwise spiral order with values from a singly linked list. The leftover cells (if the list ends before filling the matrix) should be -1.

First idea: simulate the spiral traversal using four boundaries (top, bottom, left, right). Initialize the matrix with -1s, then walk the spiral and replace cells with linked-list values until the list is exhausted. That way, any remaining cells are already -1 and no extra pass is required.

Be careful about updating boundaries and stopping when the list runs out. Also consider single-row or single-column cases where directions overlap.

Constraints: m * n <= 1e5 so an O(m*n) traversal is fine. Memory O(m*n) required for the matrix.

## Refining the problem, round 2 thoughts
Refinements:
- Initialize matrix filled with -1 so we only need to assign values while traversing.
- Use top, bottom, left, right boundaries and loop while there are nodes and valid boundaries.
- After each directional fill (top row left->right, right column top->bottom, bottom row right->left, left column bottom->top) update the corresponding boundary and check if the list is exhausted.
- Edge cases: single row (top == bottom) or single column (left == right) — ensure we don't double write or traverse invalid ranges by checking bounds and list presence at each direction step.
- Complexity: time O(m*n) worst-case because we may traverse all cells; space O(m*n) for the result.

## Attempted solution(s)
```python
from typing import Optional, List

# Definition for singly-linked list is provided by LeetCode environment:
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def spiralMatrix(self, m: int, n: int, head: Optional['ListNode']) -> List[List[int]]:
        # Initialize matrix with -1
        res = [[-1] * n for _ in range(m)]
        
        top, bottom = 0, m - 1
        left, right = 0, n - 1
        node = head
        
        while node and top <= bottom and left <= right:
            # fill top row left -> right
            for c in range(left, right + 1):
                if not node:
                    break
                res[top][c] = node.val
                node = node.next
            top += 1
            if not node:
                break
            
            # fill right column top -> bottom
            for r in range(top, bottom + 1):
                if not node:
                    break
                res[r][right] = node.val
                node = node.next
            right -= 1
            if not node:
                break
            
            # fill bottom row right -> left (if still valid)
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    if not node:
                        break
                    res[bottom][c] = node.val
                    node = node.next
                bottom -= 1
            if not node:
                break
            
            # fill left column bottom -> top (if still valid)
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    if not node:
                        break
                    res[r][left] = node.val
                    node = node.next
                left += 1
        
        return res
```
- Approach: Initialize the result matrix with -1. Simulate spiral traversal using four boundaries (top, bottom, left, right), assigning node values as we go and advancing the linked list. Stop when the list is exhausted; remaining cells stay as -1.
- Time complexity: O(m * n) in the worst case (we may visit every cell).
- Space complexity: O(m * n) for the output matrix. Additional extra space is O(1).
- Implementation details: We check for node presence before each assignment and after completing each directional fill to avoid extra work and to prevent index mistakes in single-row or single-column edge cases.