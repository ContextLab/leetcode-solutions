# [Problem 2326: Spiral Matrix IV](https://leetcode.com/problems/spiral-matrix-iv/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Another linked list problem-- yay 🥳!
- First of all, filling in the "extra" -1s is going to be a pain.  So instead of figuring out (directly) which spots are missed, let's just start by initializing a matrix of -1s: `matrix = [[-1] * n for _ in range(m)]`
- Then...there are two ways of filling stuff in.  One option is to keep track of the upper/right-most/lower/left-most "bounds" that we've filled in so far, and then keep looping through until we hit one less than the current limits in the current direction (cycling through top-most left to right --> right-most top to bottom --> bottom-most right to left --> left-most bottom to top).  Another option would be to cycle through the same order, but instead of explicitly keeping track of the bounds, just stop when we get to a value that's less than 0.  This will "work" because the nodes' values are guaranteed to be greater than or equal to 0 (and less than or equal to 1000, but that doesn't matter here).
- So the idea could be something like:
    - Start with current position = `matrix[0][0]` and `current_direction = 'right'`.  Then initiate `move_right(current_pos)` until either we hit the limits of the matrix along that dimension, or until we encounter a -1, or until we hit the end of the linked list.  As we move, we're replacing -1s in the matrix with the values in the linked list, and progressing along the linked list (from node to node).
    - The directions go in order (`['right', 'down', 'left', 'up']`) and we'll need functions to move in each direction

## Refining the problem, round 2 thoughts
- Let's think through how to implement "moving"...
- I think (after initializing the `matrix` we'll ultimately return), we should iterate through moves in a `while` loop, like this:
```python
matrix = [[-1] * n for _ in range(m)]
pos = [0, 0]
node = head
while True:
    for func in [move_right, move_down, move_left, move_up]:
        pos, node = func(pos, node)
        if node is None:
            return matrix
```
- Then we just need to implement each of `move_right`, `move_down`, `move_left`, and `move_up`:
```python
def move_right(pos, node):
    while node is not None and pos[1] < n and matrix[pos[0]][pos[1]] == -1:
        matrix[pos[0]][pos[1]] = node.val
        pos[1] += 1
        node = node.next
    pos[1] -= 1  # undo last move
    pos[0] += 1  # move to next viable position
    return pos, node

def move_down(pos, node):
    while node is not None and pos[0] < m and matrix[pos[0]][pos[1]] == -1:
        matrix[pos[0]][pos[1]] = node.val
        pos[0] += 1
        node = node.next
    pos[0] -= 1  # undo last move
    pos[1] -= 1  # move to next viable position
    return pos, node

def move_left(pos, node):
    while node is not None and pos[1] >= 0 and matrix[pos[0]][pos[1]] == -1:
        matrix[pos[0]][pos[1]] = node.val
        pos[1] -= 1
        node = node.next
    pos[1] += 1  # undo last move
    pos[0] -= 1  # move to next viable position
    return pos, node

def move_up(pos, node):
    while node is not None and pos[0] >= 0 and matrix[pos[0]][pos[1]] == -1:
        matrix[pos[0]][pos[1]] = node.val
        pos[0] -= 1
        node = node.next
    pos[0] += 1  # undo last move
    pos[1] += 1  # move to next viable position
    return pos, node
```
- Ok...let's put it all together!

## Attempted solution(s)
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def spiralMatrix(self, m: int, n: int, head: Optional[ListNode]) -> List[List[int]]:
        def move_right(pos, node):
            while node is not None and pos[1] < n and matrix[pos[0]][pos[1]] == -1:
                matrix[pos[0]][pos[1]] = node.val
                pos[1] += 1
                node = node.next
            pos[1] -= 1  # undo last move
            pos[0] += 1  # move to next viable position
            return pos, node
        
        def move_down(pos, node):
            while node is not None and pos[0] < m and matrix[pos[0]][pos[1]] == -1:
                matrix[pos[0]][pos[1]] = node.val
                pos[0] += 1
                node = node.next
            pos[0] -= 1  # undo last move
            pos[1] -= 1  # move to next viable position
            return pos, node
        
        def move_left(pos, node):
            while node is not None and pos[1] >= 0 and matrix[pos[0]][pos[1]] == -1:
                matrix[pos[0]][pos[1]] = node.val
                pos[1] -= 1
                node = node.next
            pos[1] += 1  # undo last move
            pos[0] -= 1  # move to next viable position
            return pos, node
        
        def move_up(pos, node):
            while node is not None and pos[0] >= 0 and matrix[pos[0]][pos[1]] == -1:
                matrix[pos[0]][pos[1]] = node.val
                pos[0] -= 1
                node = node.next
            pos[0] += 1  # undo last move
            pos[1] += 1  # move to next viable position
            return pos, node

        matrix = [[-1] * n for _ in range(m)]
        pos = [0, 0]
        node = head
        while True:
            for func in [move_right, move_down, move_left, move_up]:
                pos, node = func(pos, node)
                if node is None:
                    return matrix
```
- Given test cases pass
- Let's test some edge cases:
    - Filling in every position in the matrix:
        - `m = 4, n = 5, head = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]`: pass
    - Just a single node, $1 \times 1$ matrix: `m = 1, n = 1, head = [1]`: pass
- Ok, ready to submit!

![Screenshot 2024-09-09 at 12 19 00 AM](https://github.com/user-attachments/assets/bd7dd57e-9817-42c1-bb96-114c383132f5)

Solved!
