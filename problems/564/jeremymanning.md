# [Problem 564: Find the Closest Palindrome](https://leetcode.com/problems/find-the-closest-palindrome/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- One interesting aspect of the problem is that `n` is limited to at most 18 digits.  So I'm guessing the algorithm will be $O(\mathrm{len}(n)^x)$, where $x$ is potentially something large.
- Off the top of my head, I can see a few categories of scenarios we might encounter:
    - If `n` is *already* a palindrome, then we need to find a *different* palindrome.
        - If `len(n)` is odd, we can just add or subtract 1 (as allowed) to the middle digit and see which is closer to `n` (or if they're equally close, just subtract 1).
        - If `len(n)` is even, it's trickier.  I guess we could add or subtract 1 to the *two* middle digits (again, as allowed)
    - If `n` is *not* a palindrome, then:
        - If `len(n)` is odd, maybe we just return `n[:len(n)//2 + 1] + n[:len(n)//2][::-1]`?
        - And if `len(n)` is even, we could return `n[:len(n)//2] + n[:len(n)//2][::-1]`?
- The problem must not be this simple.  Let's make something up...suppose `n = "293847"`.  Since `n` is not a palindrome, and `len(n)` is even, is `293392` the closest palindrome?  The difference is 455.  What about 294492?  The difference is 645, which is larger.  But maybe there's a scenario where increasing or decreasing the middle digits might be helpful?  I don't think it could hurt to check.  It'd still be a very simple/fast solution.
- What if `n = 9283743`?  Then, using the above procedure, we'd return 9283829 (diff = 86).  What about 9284829?  (diff = 1086, which is larger).  Or 9282829?  (diff = 914, which is also larger than 86).
- One scenario we'll need to cover is if `len(n) == 1`.  If `n == '0'` then we just return `'1'`.  Otherwise we should return `str(int(n) - 1)`.
- Hmm.  Well...I suppose we can just try this and see what happens?  We'll need to test with a bunch of examples.

## Refining the problem, round 2 thoughts
- First we'll need to check if `n` is a palindrome.  We could use:
```python
def is_palindrome(n):
    return n[:len(n) // 2] == n[-(len(n) // 2):][::-1]
```
    - Actually, this was easier than I thought it'd be-- we don't need to differentiate from even vs. odd-length `n`s, since the middle digit doesn't matter if `len(n)` is odd (it doesn't affect the "palindrome" status of `n`).
- We can also write a convenience function to check distances between string representations of different numbers:
```python
def dist(a, b):
    return abs(int(a) - int(b))
```
- And also some code for incrementing or decrementing the middle digit(s):
```python
def wiggle_middle_digits(n):
    x1 = n.copy()
    x2 = n.copy()

    x1_middle = str(int(n[len(n) // 2]) - 1)
    x2_middle = str(int(n[len(n) // 2]) + 1)
    
    if len(n) % 2 == 0:
        x1[len(n) // 2] = x1_middle
        x1[len(n) // 2 + 1] = x1_middle
        x2[len(n) // 2] = x2_middle
        x2[len(n) // 2 + 1] = x2_middle
    else:
        x1[len(n) // 2 + 1] = x1_middle
        x2[len(n) // 2 + 1] = x2_middle

    if dist(n, x1) <= dist(n, x2):
        return x1
    else:
        return x2
```

- Other than that, we just need to implement the above rules.  Let's see if it works!

## Attempted solution(s)
```python
from copy import copy

class Solution:
    def nearestPalindromic(self, n: str) -> str:
        def is_palindrome(n):
            return n[:len(n) // 2] == n[-(len(n) // 2):][::-1]

        def dist(a, b):
            return abs(int(a) - int(b))

        def wiggle_middle_digits(n):
            x1 = list(copy(n))
            x2 = list(copy(n))
        
            x1_middle = str(int(n[len(n) // 2]) - 1)
            x2_middle = str(int(n[len(n) // 2]) + 1)
            
            if len(n) % 2 == 0:
                x1[len(n) // 2] = x1_middle
                x1[len(n) // 2 + 1] = x1_middle
                x2[len(n) // 2] = x2_middle
                x2[len(n) // 2 + 1] = x2_middle
            else:
                x1[len(n) // 2 + 1] = x1_middle
                x2[len(n) // 2 + 1] = x2_middle

            x1 = ''.join(x1)
            x2 = ''.join(x2)
            
            if dist(n, x1) <= dist(n, x2):
                return x1
            else:
                return x2
        
        if len(n) == 1:
            if n == "0":
                return "1"
            else:
                return str(int(n) - 1)

        if is_palindrome(n):
            return wiggle_middle_digits(n)
        elif len(n) % 2 == 0:
            return n[:len(n)//2] + n[:len(n)//2][::-1]
        else:
            return n[:len(n)//2 + 1] + n[:len(n)//2][::-1]
```
- Both given test cases pass
- Let's try a bunch of other examples:
    - `n = "32459827345987"`: pass
    - `n = "4387348756345786"`: pass
    - `n = "438734878437834": fail!  (note: I also had to fix up the "wiggle" code syntax).
        - There seems to be an issue with the `wiggle_middle_digits` code-- it doesn't seem to be working as expected.  However, I'm out of time for tonight, so I'll have to come back to this!
