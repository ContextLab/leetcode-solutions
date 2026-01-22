# [Problem 1910: Remove All Occurrences of a Substring](https://leetcode.com/problems/remove-all-occurrences-of-a-substring/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to remove occurrences of `part` from `s` repeatedly, always removing the leftmost occurrence until none remain. My first mental model: repeatedly search for `part` in `s` using `s.find(part)` and remove the found slice until `find` returns -1. That will work but can be O(n^2) in worst cases because string removals and repeated scans are expensive.

A more efficient approach is to simulate building the final string left-to-right and whenever the suffix equals `part`, remove that suffix. This is a stack-like approach: push characters onto a result list; after each push, check whether the last len(part) characters equal `part`; if so, pop them. This implicitly always removes the leftmost possible occurrence as we build `s` from left to right.

Edge cases: overlapping occurrences, `part` length 1, or `s` length up to 1000 (so O(n*m) is okay in practice). Could optimize the suffix-check with KMP-style automation if needed.

## Refining the problem, round 2 thoughts
The stack-like approach preserves the "leftmost removal" rule because as we scan from left to right, whenever the just-formed suffix equals `part`, that corresponds to removing the earliest occurrence that ends at the current index (and any future removals cannot be to the left of that point because we've processed left positions already). This yields the same final string as iteratively removing leftmost occurrences.

Implementation details:
- Use a list of characters `res` as the stack to allow efficient append/pop.
- Compare the suffix of `res` to `part` each time the length condition is met. For clarity, pre-convert `part` into a list `part_list` and compare `res[-m:] == part_list`. This comparison performs a slice but given constraints (s and part <= 1000) this is acceptable.
- Time complexity: O(n * m) in the worst case (n = len(s), m = len(part)). Space: O(n) for the result list.
- If required for larger constraints, we could avoid O(m) suffix comparisons by maintaining KMP-style automaton or storing for each appended character the matched prefix length; that would give O(n + m).

## Attempted solution(s)
```python
class Solution:
    def removeOccurrences(self, s: str, part: str) -> str:
        res = []
        m = len(part)
        part_list = list(part)
        for ch in s:
            res.append(ch)
            if len(res) >= m and res[-m:] == part_list:
                # remove last m characters
                del res[-m:]
        return ''.join(res)
```
- Notes:
  - Approach: Use a stack-like list `res` to build the resulting string. After appending each character from `s`, check whether the suffix of `res` matches `part`. If it does, pop that suffix. This emulates repeatedly removing the leftmost occurrences as we scan left-to-right.
  - Time complexity: O(n * m) worst-case where n = len(s) and m = len(part) because each character append may trigger an O(m) suffix comparison/removal. Given constraints (both <= 1000), this is acceptable.
  - Space complexity: O(n) for the `res` list (plus O(m) for `part_list`).