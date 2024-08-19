# [Problem 650: 2 Keys Keyboard](https://leetcode.com/problems/2-keys-keyboard/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- If `n` is a power of 2 (1, 2, 4, 8, etc.) then we can return `log2(n)`
- If `n` is a power of `x` then we can return `logx(n)`
- If `n` is *not* an integer power of anything, then we might just need to copy the first 'A' and then paste it `n` times...although...maybe there's a faster way?
- Maybe there's a dynamic programming solution: if `n` is divisible by some integer `x`, then:
    - First get `x` As
    - Then copy
    - Then paste `n // x` times
- So maybe we can build up iteratively:
    - If `n` is 1, then the number of steps is 0
    - If `n` is 2: copy + paste
    - If `n` is 3: copy + paste + paste
    - If `n` is 4: solve for 2 (2 steps), then copy + paste
    - If `n` is 5: copy + paste + paste + paste + paste
    - If `n` is 6: min(solve for 3 (3 steps), then copy + paste, solve for 2 (2 steps), then copy + paste + paste)
    - And so on...
- If `n` is prime, we just need to copy and then paste `n - 1` times
- If `n` is divisible by some integer `x`, then (as listed above) we first compute the number of steps required to get `x` As, then copy, then paste `n // x` times
    - We'll have to compute the minimum over all possible `x`s (i.e., factors of `n`)
        - Suppose we're up to `i` As.  Do we need to check all the way to `i`?  I think we just need to check up to `sqrt(i)`-- e.g., if `i` is 12 then we can factorize `i` into (1, 12), (2, 6), or (3, 4).  In general, if we can factorize `i` to the product of `x` and `y`, then either `x` or `y` must be less than or equal to `sqrt(i)`.  (At most, `x == y == sqrt(i)`.)
        - The number of steps needed to get `i` As (where `x` and `y` are factors) is `min(i, steps[x - 1] + (i // x), steps[y - 1] + (i // y))`.  But then we need to potentially update this (to a new minimum) for any other factors that require fewer steps.

## Refining the problem, round 2 thoughts
- We just need to initialize an array to store the number of steps needed to get to each number of As, up to `n`.  We can skip `n <= 1`, since we know that requires 0 steps.
- Then we just loop through `i in range(2, n + 1)` and:
    - Set `steps[i - 1] = i`
    - For `j in range(2, int(math.sqrt(i)) + 1)`:
        - `if i % j == 0:`
            - `steps[i - 2] = min(steps[i - 1], steps[j - 1] + (i // j), steps[i // j - 1] + j)`
- Then return `steps[n - 1]`
- Let's try this...

## Attempted solution(s)
```python
import math

class Solution:
    def minSteps(self, n: int) -> int:
        if n <= 1:
            return 0
        steps = [0] * n

        for i in range(2, n + 1):
            steps[i - 1] = i
            for j in range(2, int(math.sqrt(i)) + 1):
                if i % j == 0:
                    steps[i - 1] = min(steps[i - 1], steps[j - 1] + (i // j), steps[i // j - 1] + j)

        return steps[n - 1]
```
- Given test cases pass
- More tests:
    - `n = 1000`: pass
    - `n = 500`: pass
    - `n = 64`: pass
    - `n = 999`: pass
- Ok...seems good; submitting...

![Screenshot 2024-08-18 at 11 26 10 PM](https://github.com/user-attachments/assets/10337fc3-59ad-4383-adaa-804b66b48f03)

Solved!

