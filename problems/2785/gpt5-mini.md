# [Problem 2785: Sort Vowels in a String](https://leetcode.com/problems/sort-vowels-in-a-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to permute the string so consonants stay in-place and vowels are placed into vowel positions in nondecreasing ASCII order. A straightforward idea: collect all vowels from s (in their current order), sort that list by ASCII, then walk the original string and whenever I see a vowel, pop the next sorted vowel and place it; otherwise keep the consonant. Sorting characters in Python uses their ASCII ordering by default, which matches the problem requirement. Complexity will be dominated by sorting the vowels. Edge cases: no vowels (return s), all vowels (sort entire string), mixed uppercase/lowercase (ASCII ordering makes uppercase come before lowercase).

## Refining the problem, round 2 thoughts
- Vowels to consider: 'a', 'e', 'i', 'o', 'u' in both lowercase and uppercase (10 possible characters). 'Y' is treated as consonant here.
- If we want optimal time we could use counting since there are only 10 vowel characters; that yields O(n) time. But sorting the vowel list (k vowels) gives O(k log k) time and is simpler to implement; worst-case k = n so O(n log n).
- Memory: we need extra storage for the vowels list and for building the result string (O(n)).
- Implementation details: use a set for quick vowel membership test; use a list to accumulate result characters; join at the end.

## Attempted solution(s)
```python
class Solution:
    def sortVowels(self, s: str) -> str:
        # Set of vowels (both lowercase and uppercase)
        vowel_set = set("aeiouAEIOU")
        # Extract vowels
        vowels = [c for c in s if c in vowel_set]
        # Sort vowels by ASCII (default for strings)
        vowels.sort()
        # Rebuild string: replace vowel positions with sorted vowels in order
        res = []
        vi = 0
        for c in s:
            if c in vowel_set:
                res.append(vowels[vi])
                vi += 1
            else:
                res.append(c)
        return "".join(res)
```
- Notes:
  - Approach: extract vowels -> sort them by ASCII -> place them back into the vowel positions while leaving consonants untouched.
  - Time complexity: O(n + k log k) where n = len(s) and k is number of vowels. In the worst case k = n, so O(n log n).
  - Space complexity: O(n) extra (for the vowels list and the result list).
  - An alternative O(n) approach: use counting because there are only 10 possible vowel characters; count occurrences and then output vowels in ASCII order while rebuilding. The above sort-based solution is simpler and efficient for n up to 1e5.