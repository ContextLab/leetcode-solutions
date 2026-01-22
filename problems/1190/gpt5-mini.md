# [Problem 1190: Reverse Substrings Between Each Pair of Parentheses](https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to reverse substrings inside matching parentheses, starting from innermost pairs, and produce the final string without any parentheses. The straightforward idea is using a stack: whenever I see '(', push current accumulated characters; when I see ')', pop and reverse the current block then append to the popped context. That is simple and intuitive.

However, repeated string/list concatenations when reversing inside many nested parentheses could be somewhat inefficient. There's another neat trick: first precompute matching parentheses indices with a stack, then do a single pass through the string while moving forward/backward using those pairs and toggling direction when hitting parentheses. That yields a linear algorithm without many allocations.

Edge cases: a string with no parentheses (just return it), deeply nested parentheses, many small parentheses, guaranteed balanced parentheses so I don't need to handle mismatches.

## Refining the problem, round 2 thoughts
- Two valid approaches:
  1. Stack-of-strings (or lists) approach: easy to implement, clear logic; worst-case it's fine for n <= 2000.
  2. Parentheses mapping + two-pointer directional traversal: precompute pairs, then walk and flip direction at parentheses — this is O(n) time and O(n) extra space and is elegant.

- I'll implement the mapping + traversal approach for O(n) time and O(n) space.
- Complexity: building the pair map is O(n), traversing is O(n) since each index is visited once. Space: pair array O(n) and result buffer O(n).
- Edge cases: empty or no parentheses; only letters; parentheses at edges like "(abcd)"; nested deeply like "(((a)))".

## Attempted solution(s)
```python
class Solution:
    def reverseParentheses(self, s: str) -> str:
        n = len(s)
        pair = [-1] * n
        stack = []
        # Build matching pairs of parentheses
        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            elif ch == ')':
                j = stack.pop()
                pair[i] = j
                pair[j] = i

        res = []
        i = 0
        direction = 1  # 1 means move right, -1 means move left
        while 0 <= i < n:
            if s[i] == '(' or s[i] == ')':
                # Jump to the matching parenthesis and flip direction
                i = pair[i]
                direction = -direction
            else:
                res.append(s[i])
            i += direction

        return ''.join(res)
```
- Notes about the solution:
  - We first compute matching indices for each parenthesis using a stack; pair[i] gives the index of the matching parenthesis for i.
  - Then we traverse the string with a pointer i and a direction variable. When we hit parentheses we jump to the matching index and reverse direction; when we hit letters we append them to the result.
  - Time complexity: O(n) — building pairs is O(n) and traversal is O(n).
  - Space complexity: O(n) for the pair mapping and the result buffer.
  - This method visits each character a constant number of times and avoids repeated costly reversals or concatenations.