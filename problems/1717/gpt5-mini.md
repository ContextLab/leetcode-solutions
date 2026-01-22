# [Problem 1717: Maximum Score From Removing Substrings](https://leetcode.com/problems/maximum-score-from-removing-substrings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to maximize points by removing "ab" for x points and "ba" for y points. Removals change adjacency, so the order of removals matters: removing one type may create or destroy opportunities for the other type. Greedy comes to mind: always remove the higher-value substring first where possible, because removing lower-value ones first could block higher-value removals that yield more total points. Implementation-wise, a stack can simulate removals in a single pass: push characters and whenever the top of stack + current char form the desired pair, pop and add points. After removing all occurrences of the higher-value pair, the residual string can be processed similarly to remove the other pair.

## Refining the problem, round 2 thoughts
- Decide which pair to remove first based on x vs y:
  - If x >= y: remove "ab" first then "ba".
  - Else: remove "ba" first then "ab".
- Use one pass over s with a stack to remove all occurrences of the first pair greedily. This handles cascading removals created by earlier deletions.
- Then process the remaining characters (the content of the stack) in order with another stack to remove the other pair.
- Complexity: each character is pushed/popped at most once per pass => O(n) time, O(n) space worst-case.
- Edge cases: s may contain other letters; they are pushed normally and can serve as separators that prevent pair formation. Equal x and y: either order works; choose one deterministically (x >= y branch).

## Attempted solution(s)
```python
class Solution:
    def maximumGain(self, s: str, x: int, y: int) -> int:
        # Decide order: remove higher-value pair first
        if x >= y:
            first_left, first_right, first_val = 'a', 'b', x
            second_left, second_right, second_val = 'b', 'a', y
        else:
            first_left, first_right, first_val = 'b', 'a', y
            second_left, second_right, second_val = 'a', 'b', x

        total = 0
        stack = []
        # First pass: remove all occurrences of the higher-value pair
        for ch in s:
            if stack and stack[-1] == first_left and ch == first_right:
                stack.pop()
                total += first_val
            else:
                stack.append(ch)

        # Second pass: remove occurrences of the other pair from the residual characters
        stack2 = []
        for ch in stack:
            if stack2 and stack2[-1] == second_left and ch == second_right:
                stack2.pop()
                total += second_val
            else:
                stack2.append(ch)

        return total
```
- Notes:
  - The solution uses a two-pass greedy approach with stacks: first remove whichever pair gives more points, then remove the other from the remaining characters.
  - Time complexity: O(n), where n = len(s), because each character is pushed/popped at most once per pass.
  - Space complexity: O(n) worst-case for the stacks.
  - This greedy ordering (removing the higher-value pair first) is optimal because any removal of a lower-value pair that blocks a higher-value pair would be suboptimal; performing higher-value removals eagerly cannot reduce the number of possible higher-value removals.