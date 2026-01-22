# [Problem 2109: Adding Spaces to a String](https://leetcode.com/problems/adding-spaces-to-a-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks to insert spaces before certain indices in a string. The indices in `spaces` are strictly increasing, which suggests a single pass merging-like approach: walk through the string by index and when the current index equals the next entry in `spaces`, append a space first. Using a list to accumulate characters and joining at the end is the usual efficient way in Python (avoid repeated string concatenation). A set look-up would also work, but since `spaces` is sorted, a two-pointer approach is even simpler and uses only sequential checks.

## Refining the problem, round 2 thoughts
- Edge cases: `spaces` can contain 0 (leading space), can contain the last index (space before last char). All indices are valid and strictly increasing.
- Complexity: single pass over `s` while advancing through `spaces` at most once -> O(n + m) time where n = len(s), m = len(spaces). Space complexity is O(n + m) for the output string (exactly len(s) + len(spaces) characters).
- Implementation detail: use a list for accumulating characters (append operations are O(1)), then ''.join(list) to produce final string.
- Alternative: build an iterator over `spaces` and call next() to avoid index arithmetic, but a simple integer pointer is clear and efficient.

## Attempted solution(s)
```python
class Solution:
    def addSpaces(self, s: str, spaces: list[int]) -> str:
        res = []
        sp_i = 0
        m = len(spaces)
        for i, ch in enumerate(s):
            if sp_i < m and i == spaces[sp_i]:
                res.append(' ')
                sp_i += 1
            res.append(ch)
        return ''.join(res)
```
- Notes:
  - Approach: Two-pointer / single-pass. Iterate through s by index; if current index matches the next space index, append a space first and advance the space pointer. Append the current character afterwards.
  - Time complexity: O(n + m) which simplifies to O(n) since m <= n in constraints. Each character and each space index is processed once.
  - Space complexity: O(n + m) for the resulting string (res list), plus O(1) extra auxiliary space.