# [Problem 1790: Check if One String Swap Can Make Strings Equal](https://leetcode.com/problems/check-if-one-string-swap-can-make-strings-equal/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share raw stream-of-consciousness. Here is a concise approach summary instead:

- Compare s1 and s2 position by position and record indices where characters differ.
- If there are 0 differences, the strings are already equal → return True.
- If there are exactly 2 differences at indices i and j, check whether swapping characters in one string would make them equal: s1[i] == s2[j] and s1[j] == s2[i] → return True if so.
- In all other cases (1 difference or more than 2 differences), return False.

## Refining the problem, round 2 thoughts
I can’t provide internal chain-of-thought, so here is a concise refinement and edge-case checklist:

- Edge cases:
  - s1 == s2: return True (no swap needed).
  - If exactly 1 differing position: impossible to fix with a single swap → False.
  - If exactly 2 differing positions: check cross-equality as above.
  - If >2 differing positions: impossible with one swap → False.
- Complexity considerations:
  - Time: single pass over strings → O(n).
  - Space: store differing indices (at most n, but we only need to keep up to 2 to decide) → O(1) extra if capped, otherwise O(n).

## Attempted solution(s)
```python
class Solution:
    def areAlmostEqual(self, s1: str, s2: str) -> bool:
        # collect indices where s1 and s2 differ
        diffs = []
        for i, (a, b) in enumerate(zip(s1, s2)):
            if a != b:
                diffs.append(i)
                # early exit if more than 2 differences
                if len(diffs) > 2:
                    return False

        # if no differences, strings are already equal
        if not diffs:
            return True

        # if exactly two differences, check if swapping resolves them
        if len(diffs) == 2:
            i, j = diffs
            return s1[i] == s2[j] and s1[j] == s2[i]

        # any other case (exactly 1 difference) cannot be fixed by one swap
        return False
```
- Notes:
  - Approach: single pass to collect differing positions; at most two differences are relevant.
  - Time complexity: O(n), where n = len(s1) = len(s2).
  - Space complexity: O(1) additional (we store at most 2 indices; worst-case if not early-exiting is O(n), but we early-return when >2).