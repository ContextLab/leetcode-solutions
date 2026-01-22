# [Problem 3163: String Compression III](https://leetcode.com/problems/string-compression-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is essentially a run-length encoding task but with the constraint that each encoded segment's count must be at most 9 (a single digit). The straightforward idea is to scan the string and count consecutive identical characters and when the count reaches 9, emit "9" + character and reset the count for any remaining repeats. A simple linear pass that emits chunks of length up to 9 will work. Need to ensure it's efficient for up to 2e5 characters and builds the output using a list + join to avoid repeated string concatenation.

## Refining the problem, round 2 thoughts
- Edge cases: single character string, all different characters, very long run of the same character.
- For a long run (e.g., 20 'a's), we should output "9a9a2a" — so repeatedly output segments of up to 9 until the run is exhausted.
- Implementation detail: use two pointers or a pointer + counter. Stop counting a run when we either hit a different char or reach count 9, emit, and continue.
- Complexity: a single linear scan O(n) time, and O(n) space for the output string. Use list append and join for efficiency.

## Attempted solution(s)
```python
class Solution:
    def compressString(self, s: str) -> str:
        n = len(s)
        i = 0
        parts = []
        while i < n:
            # Count up to 9 characters equal to s[i]
            cnt = 1
            j = i + 1
            while j < n and s[j] == s[i] and cnt < 9:
                cnt += 1
                j += 1
            parts.append(str(cnt))
            parts.append(s[i])
            i = j
        return "".join(parts)
```
- Notes:
  - Approach: single pass run-length encoding, capping counts at 9 and emitting segments repeatedly until a run is exhausted.
  - Time complexity: O(n), where n = len(s). Each character is visited a constant number of times.
  - Space complexity: O(n) for the output (plus O(1) auxiliary), and we build the output using a list of small strings then join.