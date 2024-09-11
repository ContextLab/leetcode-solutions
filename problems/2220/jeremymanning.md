# [Problem 2220: Minimum Bit Flips to Convert Number](https://leetcode.com/problems/minimum-bit-flips-to-convert-number/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- First we need to convert each number to its binary representation.  We can do that using `bin(x)[2:]`
- Next, we need to append leading 0s as needed.  We need to append `abs(len(start) - len(goal))` leading 0s to whichever (of `start` or `goal`) has a shorter binary representation
- Finally, now that the two representations have the same length, we can just loop through bit by bit and count up the number of mismatches

## Refining the problem, round 2 thoughts
- Nothing too complex here; let's implement it!

## Attempted solution(s)
```python
class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        start = bin(start)[2:]
        goal = bin(goal)[2:]

        leading_zeros = ''.join('0' * abs(len(start) - len(goal)))
        if len(start) < len(goal):
            start = leading_zeros + start
        else:
            goal = leading_zeros + goal

        flips = 0
        for i, j in zip(start, goal):
            if i != j:
                flips += 1
        return flips
```
- Given test cases pass
- Submitting...

![Screenshot 2024-09-10 at 11 18 01 PM](https://github.com/user-attachments/assets/1b2f904a-897c-4df4-8563-33cc785bb26b)

Solved!  Easy peasy lemon squeezy! 🍋

  
