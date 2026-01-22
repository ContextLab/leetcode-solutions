# [Problem 2116: Check if a Parentheses String Can Be Valid](https://leetcode.com/problems/check-if-a-parentheses-string-can-be-valid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Observations: positions with locked[i] == '0' can be freely changed to '(' or ')', so they behave like wildcards; locked '1' positions are fixed.
- If n is odd, impossible to form a valid parentheses string.
- This is analogous to the "valid parentheses with '*' wildcards" problem: maintain a range of possible open-parentheses counts while scanning.
- A greedy scan left-to-right that tracks the minimum and maximum possible balance (unmatched '(' count) should determine feasibility.

## Refining the problem, round 2 thoughts
- Represent each character as affecting the balance:
  - locked == '1' and s[i] == '(' => +1 to both min and max.
  - locked == '1' and s[i] == ')' => -1 to both min and max.
  - locked == '0' => can be '(' or ')' so min-- and max++ (expands range).
- Clamp min to at least 0 because we cannot have negative guaranteed unmatched '('.
- If at any point max < 0, there are too many ')' even in the best case => impossible.
- At the end, if min == 0 then we can assign choices to achieve a balanced string (otherwise there are leftover forced '(').
- Time complexity O(n), space O(1). Handle edge case: if n is odd => return False immediately.

## Attempted solution(s)
```python
class Solution:
    def canBeValid(self, s: str, locked: str) -> bool:
        n = len(s)
        # If length is odd, can't be valid
        if n % 2 == 1:
            return False

        # low: minimum possible number of unmatched '('
        # high: maximum possible number of unmatched '('
        low = 0
        high = 0

        for i in range(n):
            if locked[i] == '1':
                # fixed character
                if s[i] == '(':
                    low += 1
                    high += 1
                else:  # s[i] == ')'
                    low -= 1
                    high -= 1
            else:
                # unlocked: can be '(' (+1) or ')' (-1)
                low -= 1   # if we choose ')'
                high += 1  # if we choose '('

            # we can't have fewer than 0 guaranteed unmatched '('
            if high < 0:
                return False
            if low < 0:
                low = 0

        # If minimum possible unmatched '(' is 0, we can balance
        return low == 0
```
- Notes:
  - Approach: greedy tracking of an interval [low, high] of possible unmatched '(' counts after processing each prefix.
  - If high ever becomes negative, even with optimal choices there are too many ')' — return False.
  - Clamp low to zero since we cannot have a guaranteed negative number of unmatched '('.
  - Final check low == 0 ensures there is some assignment of unlocked positions making the whole string balanced.
  - Time complexity: O(n). Space complexity: O(1).