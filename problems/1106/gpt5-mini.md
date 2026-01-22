# [Problem 1106: Parsing A Boolean Expression](https://leetcode.com/problems/parsing-a-boolean-expression/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to evaluate a boolean expression given as a string with operators: ! (NOT), & (AND), | (OR), parentheses, and comma-separated subexpressions. The expression is guaranteed valid. A stack-based approach comes to mind: scan the string, push tokens until you hit a ')', then pop until the matching '(' to collect the subexpressions, apply the operator that precedes the '(' and push back the result. Commas can be ignored. Alternatively, a recursive descent parser could be used too (parsing function that reads an expression and advances a pointer), but stack-based parsing is straightforward and O(n) time/space.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Single-character expressions like "t" or "f" should return True or False respectively.
- Operator appears immediately before '(' (e.g., '&(') — when scanning sequentially, pushing the operator and then '(' means when we pop until '(' we can then pop the '(' and the operator will be on top of the stack.
- For '!' operator there will be exactly one operand inside parentheses; for '&' and '|' there may be many.
- Commas are separators and can safely be ignored.
- For efficiency, represent intermediate values as characters 't' / 'f' on the stack and compute using simple checks instead of converting repeatedly to booleans.
- Time complexity O(n) since each character is pushed/popped at most once. Space complexity O(n) for the stack.

## Attempted solution(s)
```python
class Solution:
    def parseBoolExpr(self, expression: str) -> bool:
        stack = []
        for ch in expression:
            if ch == ',':
                continue
            if ch != ')':
                # push operands, operators, and '('
                stack.append(ch)
            else:
                # ch == ')': collect until '('
                vals = []
                while stack and stack[-1] != '(':
                    vals.append(stack.pop())  # vals are 't' or 'f'
                # pop the '('
                if stack and stack[-1] == '(':
                    stack.pop()
                # operator is just before '('
                op = stack.pop() if stack else None

                if op == '!':
                    # vals should have exactly one element
                    v = vals[0]
                    res = 't' if v == 'f' else 'f'
                elif op == '&':
                    # AND: result true iff all operands are 't'
                    res = 't'
                    for v in vals:
                        if v == 'f':
                            res = 'f'
                            break
                elif op == '|':
                    # OR: result true if any operand is 't'
                    res = 'f'
                    for v in vals:
                        if v == 't':
                            res = 't'
                            break
                else:
                    # Shouldn't happen for valid input, but default
                    res = 'f'

                # push result back as 't' or 'f'
                stack.append(res)

        # After processing, stack should have single 't' or 'f'
        return stack[-1] == 't'
```
- Notes about the solution:
  - Approach: single-pass stack-based evaluation. Push everything except commas. When a ')' is encountered, pop until '(' to collect the operands (they will be popped in reverse order, but order doesn't matter for AND/OR/NOT). Then pop the '(' and operator (operator is on stack just before '('), compute the result as 't' or 'f', and push it back onto the stack. At the end the stack contains either 't' or 'f'.
  - Time complexity: O(n), where n = len(expression). Each character is pushed/popped at most once.
  - Space complexity: O(n) for the stack.
  - Implementation details: operands and intermediate results are kept as characters 't' and 'f' to keep operations inexpensive. Commas are ignored during the scan. The code handles all valid inputs as guaranteed by the problem.