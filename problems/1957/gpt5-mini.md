# [Problem 1957: Delete Characters to Make Fancy String](https://leetcode.com/problems/delete-characters-to-make-fancy-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to remove the minimum number of characters so that no three consecutive characters are equal. The straightforward idea is to iterate through the string and build the resulting string greedily: keep characters unless adding the current character would create three identical characters in a row. That suggests a stack or result list; for each character, check the last two characters of the result — if both equal the current character, skip it; otherwise append it. This should be optimal because removing earlier characters can't make it possible to keep a later character without violating the "no three equal" rule, and skipping exactly those characters that would form a triple is minimal.

## Refining the problem, round 2 thoughts
Edge cases: strings shorter than 3 should be unchanged. Long runs of the same character should be reduced to at most two copies. Implementation detail: using a list for building the result is efficient (amortized O(1) append) and then join at the end. Time complexity should be O(n) and space O(n) (for the result). Another approach would be to count consecutive run lengths and append min(2, run_length) for each run, but the simple check on the last two characters is cleaner and equally efficient.

## Attempted solution(s)
```python
class Solution:
    def makeFancyString(self, s: str) -> str:
        res = []
        for ch in s:
            # If the last two characters in res are equal to ch, skipping ch avoids a triple.
            if len(res) >= 2 and res[-1] == res[-2] == ch:
                continue
            res.append(ch)
        return ''.join(res)
```
- Notes:
  - Approach: Greedy build using a list as a stack. For each character, skip it only if it would make three equal consecutive characters.
  - Time complexity: O(n), where n = len(s), since each character is processed once.
  - Space complexity: O(n) for the output (in the worst case the output is as long as the input).
  - This produces the unique minimal-deletion result required by the problem.