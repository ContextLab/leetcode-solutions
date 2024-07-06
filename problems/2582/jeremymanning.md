# [Problem 2582: Pass the Pillow](https://leetcode.com/problems/pass-the-pillow)

## Initial thoughts (stream-of-consciousness)
  - I think this is pretty straightforward
  - For a list of length $n$, it takes $n - 1$ passes to get to the last person, and another $n - 1$ passes (backwards through the line) to get back to the first person.  So the cycle resets every $2(n - 1)$ passes.
  - Therefore we can immediately mod the number of passes by $2(n - 1)$ without affecting the final position
  - After doing so, if the remainder is less than $n$, return the remainder + 1.  Otherwise (the remainder must be greater than or equal to $n$ and less than $2(n - 1)$ ) return $2n$ - the remainder - 1.

## Refining the problem
  - Any special cases to deal with?
    - If $n == 1$, should we just return 1?  --> It looks like $2 \leq n \leq 1000$, so we don't need to handle this case
    - If time is 0, just return 1?  --> Again, it looks like $1 \leq \mathrm{time} \leq 1000$, so no need to handle this case either

## Attempted solution(s)

```python
class Solution:
    def passThePillow(self, n: int, time: int) -> int:
        time %= 2 * (n - 1)
        if time < n:
            return time + 1
        else:
            return 2 * n - time - 1
```
- given test cases pass
- new test cases:
  - n = 1000, time = 1000: pass
  - n = 50, time = 324: pass
  - n = 4, time = 999: pass
  - n = 2, time = 1000: pass
- There don't seem to be any important edge cases that I'm missing; submitting...

<img width="690" alt="Screenshot 2024-07-05 at 11 11 29 PM" src="https://github.com/ContextLab/leetcode-solutions/assets/9030494/163e0790-5c4a-408d-9fca-3ce769b83c4e">

Solved!
