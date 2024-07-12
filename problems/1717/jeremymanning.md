# [Problem 1717: Maximum Score From Removing Substrings](https://leetcode.com/problems/maximum-score-from-removing-substrings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I think all of the examples could be solved using something like:
    - prioritize `'ab'` if `x > y` and `'ba'` otherwise
    - remove the higher-priority pattern (tracking points) until there are none left
    - then remove the lower-priority pattern (tracking points) until there are none left
- For trickier inputs, it's possible that new instances of the higher-priority pattern could emerge only after removing the lower-priority patterns.  In fact, maybe this could happen even after just a single lower-priority pattern removal.  So maybe we need to do something like:
    - loop until nothing else can be done:
        - remove higher priority patterns until there are none left
        - remove a single lower priority pattern
            - if none found, return the current score
    - return the current score
- This is very inefficient: finding substrings requires looping through all of `s` in $O(n)$ time, where $n$ is the length of `s`, every time we search for another instance.  In the worst case (e.g., something like `abababababab...ababab` it'll take $O(n^2)$ time, which may be too long given that `s` can be up to $10^5$ characters long
- One potential way to optimize would be to break the string into segments bounded by non-a/b characters.  Then we could compute the max score for each of these parts and sum them together.
- Another thing we can do to optimize would be to replace every consecutive sequence of non-a/b characters with a single non-a/b character (e.g., "x").  That might substantially shorten the total length of the string.
- A hypothetical edge case that I'm not sure can happen (but if so, we'll need to take it into account) is if there were some case where we could get *two* matches of the lower-priority string by sacrificing *one* instance of the higher-priority string.  Actually: a simple case might be: `s = 'abab'`, where `x < y`.  But if `x > y/2` then our best move *isn't* to remove the middle "ba" sequence-- it's to remove each "ab" sequence in turn to cash in two instances of the lower point value to get a higher total.  So those solutions above won't quite work; we need to take this into account.  I wonder if we might even encounter an example where sacrificing one higher priority string could lead to *three* (or more) matches of lower-priority strings.
- Let's try to think through some potential cases of what can happen with a given sequence of a/b characters:
    - If the length is less than or equal to two, there's nothing to search (either we have a match of one of the patterns, or not)
    - If the length is equal to three, we can only remove at most one substring (so if both are available we just return `max(x, y)` and otherwise we return the value for whichever string is found in the sequence, if any, or 0 otherwise).
    - If the length is equal to four, let's see what the possibilities are:
        - aaaa
        - aaab
        - aaba
        - aabb
        - abaa
        - abab
        - abba
        - abbb
        - baaa
        - baab
        - baba
        - babb
        - bbaa
        - bbab
        - bbba
        - bbbb
    - Aside: this is like counting in binary...maybe there's some shortcut we could take based on that?
- after taking a pause....
- Ok, in re-thinking the "abab" example above, it's not correct as I described it.  If we remove "ba" first, then we're still left with an instance of "ab" which we can use to get those points.  So actually, prioritizing the higher-scoring substring *does* seem to make sense.  The real issue is with efficiency.
- another pause...
- let's try a "stack" implementation to avoid having to loop through the same string a gajillion times:
    - to detect (with priority) the two-character substring `sub` with point value `p`:
        - loop through each character, `c` of `s`:
            - if the stack is not empty, and if the top of the stack + `c` matches `sub`:
                - increment total points by `p`
                - pop the top of the stack ("removes" the substring)
            - otherwise push `c` to the stack
        - return the total points, along with `''.join(stack)` (i.e., the updated string, with matches removed)
        - run this first for the higher-priority substring, and then for the lower-priority substring, and then return the sum of the resulting point totals

## Refining the problem, round 2 thoughts
- thinking through edge cases:
    - can we have an empty input string?  no, we're given that `1 <= s.length <= 10^5`
    - can the "points values" (`x` or `y`) ever be negative?  no, we're given that `1 <= x, y <= 10^4`
- let's try this!

## Attempted solution(s)
```python
class Solution:
    def maximumGain(self, s: str, x: int, y: int) -> int:
        def helper(s, pattern, p):
            stack = []
            points = 0
            for c in s:
                if len(stack) > 0 and stack[-1] + c == pattern:
                    stack.pop()
                    points += p
                else:
                    stack.append(c)
            return ''.join(stack), points

        if x > y:
            high, low, p1, p2 = 'ab', 'ba', x, y
        else:
            high, low, p1, p2 = 'ba', 'ab', y, x

        first_pass, total1 = helper(s, high, p1)
        _, total2 = helper(first_pass, low, p2)

        return total1 + total2
```
- given test cases: pass
- other tests:
    - 's = "ababababab"`, `x = 5`, `y = `10`: pass
    - 's = "ababababab"`, `x = 10`, `y = `5`: pass
    - `s = "abacbabcabacbabc"`, `x = 1`, `y = 1`: pass
- ok, looks reasonable...submitting...

![Screenshot 2024-07-12 at 9 05 26 AM](https://github.com/user-attachments/assets/0010d7ff-d2e1-46ac-9c8f-43a428c6405c)

done!

