# [Problem 3120: Count the Number of Special Characters I](https://leetcode.com/problems/count-the-number-of-special-characters-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want to count letters that appear both in lowercase and uppercase in the string. The simplest way is to record which lowercase letters appear and which uppercase letters appear, then count how many letters are present in both sets. Using Python sets seems natural: collect lowercase characters, collect uppercase characters (converted to lowercase), and take the intersection size. The input size is small (<=50), so anything linear in the string length is fine. Watch out for repeated letters — sets handle that naturally. Edge cases: all-lowercase or all-uppercase -> result 0.

## Refining the problem, round 2 thoughts
Refinement: build two sets:
- lower = {chars in word that are lowercase}
- upper_lower = {lowercase version of chars in word that are uppercase}

The special letters are lower ∩ upper_lower. Complexity: one pass to build sets O(n) time, and intersection is O(26) = O(1) effectively. Space: O(1) extra (bounded by 26 letters), or O(min(n,26)). Alternative: use an array of 26 booleans for lower/upper; but sets are concise and clear.

Edge cases: empty string isn't possible per constraints (length >= 1), but algorithm still handles it. Case where characters outside a-z/A-Z don't exist per constraints.

## Attempted solution(s)
```python
class Solution:
    def countSpecialCharacters(self, word: str) -> int:
        # Set of lowercase letters present
        lower = {ch for ch in word if ch.islower()}
        # Set of letters (in lowercase form) that appear in uppercase in the word
        upper_lower = {ch.lower() for ch in word if ch.isupper()}
        # The special letters are those present in both sets
        return len(lower & upper_lower)
```
- Notes:
  - Approach: collect lowercase letters and uppercase letters (normalized to lowercase), then count the intersection.
  - Time complexity: O(n), where n = len(word). Each character is inspected once; set operations are O(1) average.
  - Space complexity: O(1) extra (bounded by the alphabet size, at most 26 elements in each set).