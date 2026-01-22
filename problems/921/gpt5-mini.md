# [Problem 921: Minimum Add to Make Parentheses Valid](https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness, but here is a concise summary of the approach: traverse the string while tracking the number of unmatched opening parentheses. For each ')' encountered, if there is an unmatched '(', pair it; otherwise count one required insertion for a missing '('. After the traversal, any remaining unmatched '(' require corresponding ')' insertions. This yields the minimum number of insertions.

## Refining the problem, round 2 thoughts
- We only need a single integer counter for unmatched '(' (call it open_count) and another integer for insertions required for unmatched ')'.
- For each character:
  - If it is '(', increment open_count.
  - If it is ')':
    - If open_count > 0, decrement open_count (we matched a previous '(').
    - Otherwise, increment needed_insertions (we need an extra '(' before this ')').
- At the end, remaining open_count indicates how many ')' we need to add.
- Edge cases:
  - s consists entirely of '(' -> answer is len(s).
  - s consists entirely of ')' -> answer is len(s).
  - Mixed but balanced -> answer is 0.
- Time complexity: O(n) where n = len(s).
- Space complexity: O(1) extra space.

## Attempted solution(s)
```python
class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        open_count = 0  # number of unmatched '('
        insertions = 0  # number of insertions needed for unmatched ')'

        for ch in s:
            if ch == '(':
                open_count += 1
            else:  # ch == ')'
                if open_count > 0:
                    open_count -= 1
                else:
                    insertions += 1

        # Remaining unmatched '(' need closing ')'
        return insertions + open_count
```
- Notes:
  - Approach: Greedy single-pass counting unmatched opens and unmatched closes.
  - Time complexity: O(n) — we scan the string once.
  - Space complexity: O(1) — only two integer counters used.
  - This is optimal and straightforward; a stack-based approach would work but is unnecessary since we only need counts, not positions.