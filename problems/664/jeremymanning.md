# [Problem 664: Strange Printer](https://leetcode.com/problems/strange-printer/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Ugh, *another* dynamic programming problem!?  I hope this sequence ends soon 😱
- Ok, so how can we solve this one... 🤔
    - First we can do some housekeeping by removing any repeated characters.  This will take $O(n)$ time, which is "free" since the full algorithm will almost certainly by slower than that:
    ```python
    def simplify(s):
        x = s[0]
        for c in s[1:]:
            if c != x[-1]:
                x += c
        return x
    ```
    - Next, we should define a helper function:
        - Take in...what?  Maybe a start index and end index for a substring of the (simplified) `s`?  We could also pass in a substring directly, but that'd require copying the substrings in memory (inefficient).  Since nothing will get modified, I think we can just reference using indices.
        - The helper function should return the turns required for that substring
        - To figure out: how will this work?
    - Then the function will be something like
    ```python
    s = simplify(s)
    return helper(0, len(s) - 1)
    ```
- I'm guessing `helper` will end up calling the same indices multiple times recursively, so we should also cache the results to avoid re-computing them:
```python
cache = {}
def helper(a, b):
    if (a, b) in cache:
        return cache[(a, b)]
    
    turns = <do computations, probably call helper recursively>
    cache[(a, b)] = turns
    return turns
```
- So the "trick" here will be figuring out how that `helper` function should look.

## Refining the problem, round 2 thoughts
- If the substring is empty, return 0.  This happens if `a > b`.
- If the substring is just a single character, return 1 (`a == b`)
- We'll need to iteratively improve on the number of turns.  The worst case would be `b - a + 1` (i.e., one turn per character).
    - If there are duplicated characters (since we've already simplified, these will be separated by intervening characters), we can improve on this worst case.  So we'll need to detect duplicates.
    - We could start at the first character, and see if there are any duplicates of *that* character.  If we find a duplicate (say the first one occurs at position `j`) then we can save one turn (print the duplicate character, then figure out how many turns are needed for `s[a + 1:j]`.  So the total for that sub-sequence would be `1 + helper(a, j - 1)`.  Then we can skip over character `j`.  Then we need to compute the number of turns needed for `s[j + 1:b]`.  We can update `min_turns = min(min_turns, helper(a, j - 1) + helper(j + 1, b))`
    - If we find *another* duplicate later on in the sequence, we can just repeat this process.  But the cache will avoid re-computing things many times.
- Let's try this...it might not be too bad.  I might be missing something, but I'm surprised this is a "hard" problem; the recent "medium" problems have seemed trickier!

## Attempted solution(s)
```python
class Solution:
    def strangePrinter(self, s: str) -> int:
        def simplify(s):
            x = s[0]
            for c in s[1:]:
                if c != x[-1]:
                    x += c
            return x

        s = simplify(s)
        cache = {}
        def helper(a, b):
            if a > b:
                return 0
            elif a == b:
                return 1
            elif (a, b) in cache:
                return cache[(a, b)]

            min_turns = b - a + 1
            for i in range(a + 1, b + 1):
                if s[a] == s[i]:
                    min_turns = min(min_turns, helper(a, i - 1) + helper(i + 1, b))
            cache[(a, b)] = min_turns
            return min_turns
        
        return helper(0, len(s) - 1)
```
- Given test cases pass
- Let's try some longer strings:
    - `s = "abaabababaabababababbbabababacccbbcbcbabaababa"`: pass(!!)
    - `s = "ddzdmpdnrmndphslxhewdhrnwlmlinkpttuopysqgvhssxqxiozhffyxwvyfcwhkpxxcmxzxvodtjsiiuzzmxveddcvtuhxanzgb": womp womp...fail 😞
        - Ok...let's brainstorm...I think there are a few possible things that could be happening:
            - Most likely: the logic of just checking for the first matching character might not make sense.  How do we match other characters?
            - Actually, maybe we should initialize `min_turns` to `1 + helper(a + 1, b)`.  That way each recursive call will consider matches of the "new `a`" in turn.  I wonder if that will just fix the problem "for free."
```python
class Solution:
    def strangePrinter(self, s: str) -> int:
        def simplify(s):
            x = s[0]
            for c in s[1:]:
                if c != x[-1]:
                    x += c
            return x

        s = simplify(s)
        cache = {}
        def helper(a, b):
            if a > b:
                return 0
            elif a == b:
                return 1
            elif (a, b) in cache:
                return cache[(a, b)]

            min_turns = 1 + helper(a + 1, b)
            for i in range(a + 1, b + 1):
                if s[a] == s[i]:
                    min_turns = min(min_turns, helper(a, i - 1) + helper(i + 1, b))
            cache[(a, b)] = min_turns
            return min_turns
        
        return helper(0, len(s) - 1)
```
- That fixes the above test cases!  Let's try some more...
- `s = "niqmxxbwvonppouiypidwbqmodqvtnlaxxdgpayhmzywnyojfkqobatdyhfkzayazifwqyfpgxlpbupyascdfnqtnmrdlwwkagiq": pass
- `s = "naajdcjcrvbhmjxgkenbqdkikmnxufughnjwasclwuvrenhksnosyigmnovmexmegklcqllfmxbbhtvazzcqhltoiukvsvgnwyvl": pass
- What about some silly cases?
    - `s = "aaaaaaaaaaa": pass
- Ok, let's try submitting...

![Screenshot 2024-08-20 at 11 12 39 PM](https://github.com/user-attachments/assets/281bcbb9-80ea-419e-bf2c-727c81ab59b7)

Solved!

