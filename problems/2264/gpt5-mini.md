# [Problem 2264: Largest 3-Same-Digit Number in String](https://leetcode.com/problems/largest-3-same-digit-number-in-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[I need to find substrings of length 3 that are composed of the same digit. The easiest way is to scan the string and check every window of length 3. If s[i] == s[i+1] == s[i+2], that's a candidate. Keep the maximum candidate. Since all candidates have length 3, string comparison corresponds to numeric order (because they are the same length and use digits). I can keep a single best digit or best string. Edge cases: leading zeros allowed, return "" if none. Input length up to 1000, so an O(n) scan is trivial.]

## Refining the problem, round 2 thoughts
[Refinement: iterate i from 0 to len(num)-3, check the 3 characters. When a triple is found, either update best if current digit > best digit. Alternatively, I could check digits from '9' to '0' and return the first 'ddd' that appears in num using substring search — also fine but single-pass is simpler and clearly O(n). Time complexity O(n), space O(1). Edge cases: no triple -> return "". Implementation detail: use class Solution with method largestGoodInteger for LeetCode.]

## Attempted solution(s)
```python
class Solution:
    def largestGoodInteger(self, num: str) -> str:
        n = len(num)
        best = ""  # store best triple string, or "" if none
        for i in range(n - 2):
            a, b, c = num[i], num[i+1], num[i+2]
            if a == b == c:
                triple = a * 3
                # since all triples have length 3, lexicographic compare works
                if triple > best:
                    best = triple
        return best
```
- Notes:
  - Approach: single-pass sliding window of size 3 checking equality of the three characters. Keep the lexicographically largest triple found.
  - Time complexity: O(n), where n = len(num) (one pass over the string).
  - Space complexity: O(1) extra space (only a few variables).
  - Implementation detail: comparing strings of equal length of digits is equivalent to numeric comparison, so using string comparison is correct.