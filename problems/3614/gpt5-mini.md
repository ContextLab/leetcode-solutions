# [Problem 3614: Process String with Special Operations II](https://leetcode.com/problems/process-string-with-special-operations-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the k-th character (0-indexed per examples) of the final string after processing a sequence of operations: append letter, '*' removes last char, '#' duplicates the whole current string (concatenate with itself), '%' reverses the current string. The final string length can be up to 1e15 and k up to 1e15, so we cannot build the final string explicitly.

Classic trick: simulate forward only lengths (capped to a large sentinel >1e15), then walk the operations backward mapping the requested index k into the previous state's index. Similar to problems that ask for kth character after repeated doubling/operations. For each operation we can invert it:

- Letter appended: if k equals length_before -> we found the letter; otherwise k remains the same.
- '*': removed last char (if any) — in the backward mapping, this just means previous length = current length + 1 (if previous had >0). But observed mapping: every valid current index corresponds to same index in previous (the removed last char has no counterpart), so k stays same.
- '#': duplication doubled length: if k < L -> k maps to k; if k >= L -> k maps to k - L.
- '%': reversal: index k maps to L - 1 - k.

So compute prefix lengths, then iterate backward to map k until we either hit a letter (and return) or exhaust operations (then return '.').

## Refining the problem, round 2 thoughts
Edge cases and details:
- We must use a large cap (>= 1e15) when computing lengths to avoid overflow; use something like INF = 10**18.
- '*' when previous length is 0 does nothing; mapping is trivial.
- If final computed total length <= k => k out of bounds => return '.'.
- Maintain lengths array len_after[i] = length after processing s[:i+1], and derive length_before = len_after[i-1] or 0.
- Time: O(n) to build lengths + O(n) to walk backward mapping => O(n). Space: O(n) for lengths array.

I'll implement findKthCharacter(s, k) as required.

## Attempted solution(s)
```python
class Solution:
    def findKthCharacter(self, s: str, k: int) -> str:
        # k is 0-indexed per problem statement/examples
        n = len(s)
        INF = 10**18  # safe cap > 1e15
        lengths = [0] * n  # length after processing s[0..i]
        cur = 0
        for i, ch in enumerate(s):
            if 'a' <= ch <= 'z':
                cur += 1
            elif ch == '*':
                if cur > 0:
                    cur -= 1
            elif ch == '#':
                cur = min(INF, cur * 2)
            elif ch == '%':
                # reverse doesn't change length
                pass
            lengths[i] = min(INF, cur)

        total_len = lengths[-1] if n > 0 else 0
        if k >= total_len:
            return '.'

        # Walk backwards mapping k to previous indices
        for i in range(n-1, -1, -1):
            ch = s[i]
            prev_len = lengths[i-1] if i > 0 else 0
            if 'a' <= ch <= 'z':
                # appended at position prev_len
                if k == prev_len:
                    return ch
                # otherwise index lies within previous string; k stays same
            elif ch == '*':
                # This operation removed the last char of previous if prev_len>0.
                # Valid current indices correspond to same indices in previous.
                # So k remains same. (If prev_len == 0, still nothing changed.)
                # Nothing to do.
                pass
            elif ch == '#':
                # result was previous concatenated to itself: length = 2 * prev_len
                # If k in second half, map to k - prev_len
                if prev_len == 0:
                    # duplication of empty string => still empty; nothing to map.
                    pass
                else:
                    if k >= prev_len:
                        k -= prev_len
            elif ch == '%':
                # reversed previous: index k maps to prev_len - 1 - k
                if prev_len == 0:
                    # reversing empty does nothing
                    pass
                else:
                    k = prev_len - 1 - k

        # If we exit loop without returning, index is out of bounds
        return '.'
```
- Notes about approach:
  - We first compute the resulting length after each character without building the string. We cap lengths using INF = 1e18 (safe given constraints).
  - If k >= final length return '.' immediately.
  - Then we invert operations from right to left mapping the desired index in the current state to the corresponding index in the previous state. When we hit an appended letter whose index equals the mapped k we return it.
  - Time complexity: O(n) to build lengths + O(n) backward mapping = O(n), where n = len(s).
  - Space complexity: O(n) for the lengths array.
  - All operations use integer arithmetic within safe bounds because lengths are capped above the possible k and problem limit.