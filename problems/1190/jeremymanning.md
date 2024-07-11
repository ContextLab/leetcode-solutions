# [Problem 1190: Reverse Substrings Between Each Pair of Parentheses](https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- The simplest solution would be to use recursion:
    - Start with `result = ''`
    - Append characters to `result` until if/when we encounter an open parenthesis (at position `i`)
        - If so, set `counter = 1`
        - Now continue to move forward through the string (starting at `i + 1`):
            - If we encounter an open parenthesis, `counter += 1`
            - If we encounter a closed parenthesis, `counter -= 1`
            - If we ever get to `counter == 0` (at position `j`):
                - set `result += reverseParenthesis(s[i + 1:j])[::-1]`
                - set `i = j + 1`
                - continue
    - Then once we run out of characters, return `result`
- I can see that the recursive solution will "work," but it's inefficient.  E.g., the string can be 2000 characters long, so if it's something like `s = (((((....((()))...)))))` we'll need to potentially recurse to a depth of up to 1000, which would be (a) memory inefficient (we have to copy all of the variables with each new recurse), and (b) potentially beyond the recursion limit.
- Another approach would be to maintain two "result" strings-- one for the starting characters (moving from the beginning to the end) and the other for the ending characters (moving from the end to the beginning)
- Or...maybe we can just use two indices (`i` moves from beginning to end and `j` moves from the end to the beginning)?
    - We could do something like:
        - Keep track of whether we need to reverse (parenthesis depth is odd) or not (parenthesis depth is even).  Start with `reverse = False`, `i = 0`, `j = len(s) - 1`, `result = ''`, 
        - While `i < j`:
            - simple case: we're at an even depth (`reverse` is `False`): just append each character in turn to `result` and increment `i` by 1 until we hit an open parenthesis
            - complicated: if we're at an odd depth, i think we need to do something like:
                - move `i` forward *and* `j` backwards, keep track of stuff in the forward direction in one variable and in the backwards direction in another variable.  We'll want to prepend each new character `s[i]` to the forward direction string and append each new character `s[j]` to the backwards direction string
                - if we hit an open parenthesis in the forward direction we stop moving forward, and if we hit a backwards parenthesis in the backwards direction we stop moving backwards
                - to figure out: what do we *do* with those temporary strings...
                    - I guess we could append the backwards direction string to `result` immediately...but what happens to the forward direction string 🤔?  Kind of tricky!
- Hmm...
- Could we do an "in place" reverse?
    - Look for the outermost open parenthesis
    - Look for the matching close parenthesis
    - Keep the stuff outside those outermost parentheses
    - Remove the parentheses + reverse the stuff inside them (now the string shrinks in length by 2...maybe this isn't terrible?)
    - Would this work... 🤔...
        - Suppose we had something like `s = 'a(bc(de)fg)h'`.  What happens?
        - We have parentheses:
            - `before = 'a'`; `after = 'h'`; `to_reverse = 'bc(de)fg`
            - Now set `s = before + to_reverse[::-1] + after` -- so `s` is now `'agf)ed(cbh'`...so clearly we'll need to match *both* open and closed parentheses.  If the parentheses weren't guaranteed to be balanced, this would be a problem.  Actually, maybe when we reverse things we can just flip the directions of the parentheses?  That'd give us `'agf(ed)cbh'`...
        - There are still parentheses remaining, so now:
            - `before = 'agf'`; `after = 'cbh'`; `to_reverse = 'ed'`
            - Now we set `s = before + to_reverse[::-1].replace('(', '*').replace(')', '(').replace('*', ')') + after` (aside: this is a mess...), so `s = 'agfdecbh'`.  Which seems...correct...
    - Is this efficient?
        - Potentially involves reshuffling stuff lots of times in memory, which seems sub-optimal, but maybe it's ok?
        - The solution is $O(np)$ where $n$ is the string length and $p$ is the number of parenthesis pairs.  If $n = 2000, p = 1000$ that could be slow...although in that "worst case" the string would actually keep shrinking, so we'd probably get closer to something like $O(p \log n)$ runtime...
    - Another test case to consider: what happens if pairs of parentheses are side by side-- e.g., `s = 'ab(cd)ef(gh)'`.  Then, actually, this solution won't work, because the "cd" open parenthesis will get paired with the "gh" closed parenthesis.  So we might need to either manually track this or do something clever...
- I'm about out of time for tonight, so I'm just going to try quickly implementing the recursive solution and see if it works...

## Refining the problem, round 2 thoughts
- Any special cases to consider?
- Eh....it's just inefficient.  I don't think it'll be "wrong" per se.  I'm guessing it'll time out on one of the test cases though.

## Attempted solution(s)
```python
class Solution:
    def reverseParentheses(self, s: str) -> str:
        def helper(s):
            result = ''
            i = 0
            while i < len(s):
                if s[i] != '(':
                    result += s[i]
                else:                    
                    depth = 1
                    j = i + 1
                    while j < len(s):
                        if s[j] == '(':
                            depth += 1
                        elif s[j] == ')':
                            depth -= 1

                        if depth == 0:
                            result += helper(s[i + 1:j])[::-1]
                            i = j
                            break
                        j += 1
                i += 1
            
            return result

        return helper(s)
```
- The given test cases pass
- I don't have time to think up more clever test cases, so I'll just submit...

![Screenshot 2024-07-10 at 11 43 29 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/21571097-ef6a-47d2-ad1f-d490187ad9bb)

Huh, I guess it worked!

