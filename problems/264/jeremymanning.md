# [Problem 264: Ugly Number II](https://leetcode.com/problems/ugly-number-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- One way to solve this would be:
    - Start the sequence with 1
    - Each subsequent element is generated by multiplying a previous element by 2, 3, or 5
    - We could have 3 indices/pointers to keep track of the next thing to multiply by 2/3/5 (initially these should all point to the first element, which is 1).  Let's call these `i2`, `i3`, and `i5`.
    - Now we just:
        - Take the current 2/3/5 pointers' numbers and multiply by 2/3/5
        - Take the minimum of the results (this occurs for pointer `i`).  Note: it's possible that *multiple* pointers could match-- e.g., if `i2 == 3` and `i3 == 2` then both the `i2` and `i3` results will be 6.
        - Add it to the list and increment the matching pointer(s) (by 1).
        - Repeat until we've gotten `n` numbers in the sequence and then return the last number in the sequence

## Refining the problem, round 2 thoughts
- Let's see if this works...

## Attempted solution(s)
```python
class Solution:
    def nthUglyNumber(self, n: int) -> int:
        ugly_numbers = [0] * n
        ugly_numbers[0] = 1

        i2, i3, i5 = 0, 0, 0
        next2, next3, next5 = 2, 3, 5

        for i in range(1, n):
            x = min(next2, next3, next5)
            ugly_numbers[i] = x

            if x == next2:
                i2 += 1
                next2 = ugly_numbers[i2] * 2

            if x == next3:
                i3 += 1
                next3 = ugly_numbers[i3] * 3

            if x == next5:
                i5 += 1
                next5 = ugly_numbers[i5] * 5

        return ugly_numbers[n - 1]
```
- Given text cases pass
- Let's try some others:
    - `n = 1690`: pass
    - `n = 250`: pass
- Ok, it's probably good; submitting...

![Screenshot 2024-08-17 at 11 39 32 PM](https://github.com/user-attachments/assets/a221898c-7840-4834-a190-41047867352b)

Woah, apparently this was the way to solve it!

