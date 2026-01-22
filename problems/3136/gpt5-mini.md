# [Problem 3136: Valid Word](https://leetcode.com/problems/valid-word/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to check a small set of conditions for a given word:
- length at least 3,
- contains only digits and English letters (so any '@', '#', '$' or other chars -> invalid),
- contains at least one vowel (a, e, i, o, u, case-insensitive),
- contains at least one consonant (any letter that is not a vowel).

First idea: iterate once through the string, validate characters (isalnum covers letters+digits), track presence of vowel and consonant when the character is a letter. Return false early if an invalid char is found. That yields O(n) time and O(1) extra space. Could also use regex but plain iteration is simple and clear.

## Refining the problem, round 2 thoughts
Edge cases:
- Short strings (length < 3) should immediately return False.
- Strings with only digits are invalid because they lack vowel and consonant.
- Strings with only vowels (e.g., "ae1") or only consonants are invalid.
- Presence of '@', '#', '$' must make it invalid.
- Uppercase vowels should be treated the same as lowercase (use a vowel set with both or lowercase conversion).

Complexity: iterate once over up to 20 characters -> negligible; O(n) time, O(1) space. Implementation detail: use str.isalpha() and str.isdigit() or str.isalnum() to detect allowed characters.

## Attempted solution(s)
```python
class Solution:
    def isValid(self, word: str) -> bool:
        # length requirement
        if len(word) < 3:
            return False

        vowels = set("aeiouAEIOU")
        has_vowel = False
        has_consonant = False

        for ch in word:
            # must be only letters or digits
            if not (ch.isalpha() or ch.isdigit()):
                return False

            if ch.isalpha():
                if ch in vowels:
                    has_vowel = True
                else:
                    has_consonant = True

            # early exit if both found
            if has_vowel and has_consonant:
                # still must ensure remaining chars are valid,
                # but we've already validated current char; continue validation
                # We cannot return True yet because future chars might be invalid.
                # So do nothing here and continue scanning.
                pass

        return has_vowel and has_consonant
```
- Notes:
  - Approach: single-pass scan. For each character, check that it's a letter or digit. If it's a letter, classify as vowel or consonant using a vowel set.
  - Important detail: even if we have found both vowel and consonant, we must continue scanning to ensure there are no invalid characters later, so we only return after scanning whole string.
  - Time complexity: O(n) where n = len(word) (n ≤ 20 by constraints).
  - Space complexity: O(1) extra space (vowel set is constant).
  - This solution handles uppercase and lowercase letters, digits, and rejects '@', '#', '$' (or any other non-alphanumeric) as required.