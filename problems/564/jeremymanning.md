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

## Coming back to this...
- I'm debugging the `wiggle_middle_digits` code, and I notice a few issues:
    - My indexing is off by 1 (the "changing" part should be):
    ```python
    if len(n) % 2 == 0:
        x1[len(n) // 2 - 1] = x1_middle
        x1[len(n) // 2] = x1_middle
        x2[len(n) // 2 - 1] = x2_middle
        x2[len(n) // 2] = x2_middle
    else:
        x1[len(n) // 2] = x1_middle
        x2[len(n) // 2] = x2_middle
    ```
- Here's the updated code:
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
                x1[len(n) // 2 - 1] = x1_middle
                x1[len(n) // 2] = x1_middle
                x2[len(n) // 2 - 1] = x2_middle
                x2[len(n) // 2] = x2_middle
            else:
                x1[len(n) // 2] = x1_middle
                x2[len(n) // 2] = x2_middle
        
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
- Now this test case passes.
- Let's try submitting...

![Screenshot 2024-08-24 at 4 01 56 PM](https://github.com/user-attachments/assets/a824a5ad-935d-4e3a-b7f5-ca510f9343ba)

- Ah.  I forgot to account for this case (when `n = "10"` the correct answer should be `"9"`, not `"11"`).
- In general, there could be a whole range of these sorts of cases (not just when there are only two digits).  E.g., when `n = "100000"` we should output `"99999"`.
- I think we could handle this with one more check: if `is_palindrome(str(int(n) - 1))` then return that:
```python
from copy import copy

class Solution:
    def nearestPalindromic(self, n: str) -> str:
        def is_palindrome(n):
            return len(n) == 1 or n[:len(n) // 2] == n[-(len(n) // 2):][::-1]

        def dist(a, b):
            return abs(int(a) - int(b))
        
        def wiggle_middle_digits(n):
            x1 = list(copy(n))
            x2 = list(copy(n))
        
            x1_middle = str(int(n[len(n) // 2]) - 1)
            x2_middle = str(int(n[len(n) // 2]) + 1)
            
            if len(n) % 2 == 0:
                x1[len(n) // 2 - 1] = x1_middle
                x1[len(n) // 2] = x1_middle
                x2[len(n) // 2 - 1] = x2_middle
                x2[len(n) // 2] = x2_middle
            else:
                x1[len(n) // 2] = x1_middle
                x2[len(n) // 2] = x2_middle
        
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

        if is_palindrome(str(int(n) - 1)):
            return str(int(n) - 1)

        if is_palindrome(n):
            return wiggle_middle_digits(n)
        elif len(n) % 2 == 0:
            return n[:len(n)//2] + n[:len(n)//2][::-1]
        else:
            return n[:len(n)//2 + 1] + n[:len(n)//2][::-1]
```
- Now `n = "10"` and `n = "1000000"` both pass; re-submitting...

![Screenshot 2024-08-24 at 4 08 00 PM](https://github.com/user-attachments/assets/a668f936-01f1-48d3-8c39-7a0dab6e5583)

- Oof 🤦.  Right...`"00"` isn't a valid output, but the `"1"'s in `"11"` are technically the "middle digits".  
- There are a bunch of these sorts of edge cases.  I think we actually need to generate a *set* of candidates, and then pick the closest (or smallest + closest if there's a tie):
    - First try mirroring the left half of the string
    - Also try wiggling the middle digit(s)
    - Check if we're in a "close to a power of 10" scenario.  We can just add `"9" * (len(n) - 1)` and `"1" + "0" * (len(n) - 1) + "1"` to the set of candidates manually
    - In case any of these have reproduced the original number, remove it
    - If we have empty strings, all zeros, etc., we'll remove those too
    - Of the remaining candidates, find the closest to `n` that is also the smallest-- we can do this by returning `min(candidates, key=lambda x: (dist(n, x), int(x)))`
- Updated solution:
```python
class Solution:
    def nearestPalindromic(self, n: str) -> str:
        def is_palindrome(x):
            return x == x[::-1]
        
        def dist(a, b):
            return abs(int(a) - int(b))

        def wiggle_middle_digits(n):
            x1 = list(n)
            x2 = list(n)
        
            mid_index = len(n) // 2
            if len(n) % 2 == 0:
                left_part = n[:mid_index]
                x1_middle = str(int(left_part) - 1)
                x2_middle = str(int(left_part) + 1)
                x1 = x1_middle + x1_middle[::-1]
                x2 = x2_middle + x2_middle[::-1]
            else:
                left_part = n[:mid_index + 1]
                x1_middle = str(int(left_part) - 1)
                x2_middle = str(int(left_part) + 1)
                x1 = x1_middle + x1_middle[:-1][::-1]
                x2 = x2_middle + x2_middle[:-1][::-1]
            
            # new special cases (e.g., 999 vs. 1001)
            if len(x1) < len(n) or x1 == '':
                x1 = "9" * (len(n) - 1)
            if len(x2) > len(n) or x2 == '':
                x2 = "1" + "0" * (len(n) - 1) + "1"
            
            return (x1, x2)

        if n == "1":
            return "0"
        
        candidates = set()

        # mirroring
        if len(n) % 2 == 0:
            mid_index = len(n) // 2
            mirrored = n[:mid_index] + n[:mid_index][::-1]
        else:
            mid_index = len(n) // 2
            mirrored = n[:mid_index + 1] + n[:mid_index][::-1]
        
        candidates.add(mirrored)

        # wiggling
        wiggle_candidates = wiggle_middle_digits(n)
        candidates.add(wiggle_candidates[0])
        candidates.add(wiggle_candidates[1])

        # edge cases (for when we're "near" a power of 10)
        candidates.add("9" * (len(n) - 1))
        candidates.add("1" + "0" * (len(n) - 1) + "1")

        # remove bad candidates (including the original number)
        candidates.discard(n)
        candidates = {c for c in candidates if c and c.isdigit()}

        # return the closest/smallest
        return min(candidates, key=lambda x: (dist(n, x), int(x)))
```
- Test cases pass, including previously failing edge cases
- Submitting... 🤞

![Screenshot 2024-08-24 at 4 23 14 PM](https://github.com/user-attachments/assets/2f803edd-b809-4a60-9a4e-871e2a461bdd)

- Solved!
