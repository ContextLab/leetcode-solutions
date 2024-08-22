# [Problem 476: Number Complement](https://leetcode.com/problems/number-complement/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- This one is trivial-- there are built-in functions that can help

## Refining the problem, round 2 thoughts
- We just need to return `int(bin(num)[2:].replace('0', 'x').replace('1', '0').replace('x', '1'), 2)`

## Attempted solution(s)
```python
class Solution:
    def findComplement(self, num: int) -> int:
        return int(bin(num)[2:].replace('0', 'x').replace('1', '0').replace('x', '1'), 2)
```
- Given test cases pass
- Submitting...

![Screenshot 2024-08-21 at 8 08 15 PM](https://github.com/user-attachments/assets/0c32eac5-1704-46af-9ca3-24a00928b7ef)

Solved!
