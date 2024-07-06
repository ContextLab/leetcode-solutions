# [Problem 2582: Pass the Pillow](https://leetcode.com/problems/pass-the-pillow/description/)

## Initial thoughts (stream-of-consciousness)
I took a couple examples and wrote them down in a grid like so:

| 1 | 2 | 3 | 4 |
|---|---|---|---|
| x | 1 | 2 | 3 |
| 6 | 5 | 4 | x |
| x | 7 | 8 | 9 |
| . | . | . | . |

Which made me realize it was a parity problem. If you take `n-1` as your divisor, the quotient will tell you what row it ends up on and the remainder will tell you how many indeces in from the edge you have to go (the direction changes based on the parity of the quotient).

## Refining the problem
* first, divide `time` by `n-1` and get the remainder
* then check the parity of the quotient:
*   if even, return `r+1`
*   if odd, return `n-r`

## Attempted solution(s)
```python
class Solution:
    def passThePillow(self, n: int, time: int) -> int:
        r = time%(n-1)
        if (time//(n-1))%2 == 0:
            return (r+1)
        else:
            return (n-r)
```
<img width="714" alt="Screen Shot 2024-07-05 at 9 31 05 PM" src="https://github.com/KatieONell/leetcode-solutions/assets/12962290/1e1c5756-94ed-4a40-b12b-724d6e914755">
