# [Problem 1190: Reverse Substrings Between Each Pair of Parentheses](https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- I can think of a few potential ways to solve this:
  - a recursive solution that'll entail checking whether `s` contains parentheses and if so, calling `reverseParentheses` on the substring between the outermost pair of parentheses before reversing `s`
  - a solution where we build up the output string by concatenating letters from either the beginning or end of `s`, switching back and forth between the two ends when we encounter open/close parentheses (switch from forward to backward if the running count of `(` is odd)
- The recursive solution seems simpler to me, so I'll start with that. I think it'll probably be less efficient than the single-pass, forward/reverse version though.
- Recursive solution:
  - check if `s` contains parenthesis
  - if no (base case), return `s[::-1]`
  - if yes (recursive case):
    - extract substring before first `(`, call this `before`
    - extract substring after last `)`, call this `after`
    - call `reverseParentheses` on substring between first `(` and last `)`, call the result `new_substr`
    - return `f"{before}{new_substr}{after}"[::-1]`
  - actually... all of the test cases happen to have the full string surrounded by parentheses, but this doesn't seem to be guaranteed, so I don't necessarily want to reverse the *whole* string at the end (outermost call). So I think I'll need to reverse each substring "one level up" from the call in which it's `s` -- i.e., my base case should just return `s` and my recursive case should return `f"{before}{new_substr[::-1]}{after}"`
  - what if we have a string containing `()`? Could add a 3rd condition that just returns `s` if `s` is an empty string, but probably not worth it because the base case will return the right result anyways.

## Refining the problem, round 2 thoughts

## Attempted solution(s)

### First attempt

```python
class Solution:
    def reverseParentheses(self, s: str) -> str:
        if "(" in s:
            open_ix = s.index("(")
            close_ix = s.rindex(")")
            return f"{s[:open_ix]}{self.reverseParentheses(s[open_ix+1:close_ix])[::-1]}{s[close_ix+1:]}"
        return s
```

Failed on test case 14, `s = "ta()usw((((a))))"` -- I didn't account for the fact that not all parentheses will necessarily be nested inside each other, so the first `(` won't necessarilly be paired with the last `)` 🤦

### Second attempt

Okay then, in that case, I don't think a recursive solution will work. But I think I can solve it a similar way as what I was thinking, using a `while` loop instead:

- while `s` contains parentheses:
  - find the index of the last (rightmost) `(`
  - find the index of the first (leftmost) `)` *that appears **after** the last (rightmost) `(`*
  - set `s` equal to the substring up to the last `(`, plus the substring between that and the first subsequent `)`, plus the substring after that `)`.

```python
class Solution:
    def reverseParentheses(self, s: str) -> str:
        while "(" in s:
            open_ix = s.rindex("(")
            close_ix = s.index(")", open_ix)
            s = f"{s[:open_ix]}{s[open_ix+1:close_ix][::-1]}{s[close_ix+1:]}"
        return s
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/1eefa486-ed2b-4576-9697-0545cd700f09)
