# [Problem 966: Vowel Spellchecker](https://leetcode.com/problems/vowel-spellchecker/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to implement a spellchecker that checks queries against a wordlist with three levels of precedence: exact (case-sensitive), case-insensitive match (first such in wordlist), and vowel-error matches (treat all vowels as interchangeable, case-insensitive, and return first such word from wordlist). The straightforward approach is to preprocess the wordlist into structures that let me answer each query in O(L) time (L = word length). I'll need:
- A set for exact (case-sensitive) membership checks.
- A map from lowercased word -> first original word seen (for case-insensitive matches).
- A map from a "devoweled" lowercased form -> first original word seen (for vowel-error matches). Devoweling can be done by replacing a, e, i, o, u with a placeholder like '*'.

Careful: must preserve the first occurrence in the wordlist for both maps. Queries are resolved in precedence order. Word lengths are small (<= 7), so building these maps is cheap.

## Refining the problem, round 2 thoughts
Edge cases / considerations:
- The vowel-error map and case-insensitive map should only store the first occurrence. So only set them if the key doesn't already exist.
- The exact check is simply membership in the original-word set.
- "Vowel" definition is a/e/i/o/u only, case-insensitive.
- Complexity: building maps is O(N * L), queries processed in O(Q * L). Space O(N * L).
- Alternatives: Could do pattern matching or tries, but maps are simplest and fastest.
- Make sure to lower-case words when producing keys for the case-insensitive map and the devoweled map.

Now implement the standard solution: preprocess wordlist into three structures, then answer each query by trying exact, then lower-case map, then devoweled map, else return "".

## Attempted solution(s)
```python
class Solution:
    def spellchecker(self, wordlist: list[str], queries: list[str]) -> list[str]:
        vowels = set('aeiou')
        
        def devowel(word: str) -> str:
            # return lowercased devoweled form where vowels replaced by '*'
            w = word.lower()
            return ''.join('*' if ch in vowels else ch for ch in w)
        
        exact = set(wordlist)  # case-sensitive exact matches
        case_map = {}          # lowercased -> first original word
        vowel_map = {}         # devoweled lowercased -> first original word
        
        for w in wordlist:
            lw = w.lower()
            if lw not in case_map:
                case_map[lw] = w
            dv = devowel(w)
            if dv not in vowel_map:
                vowel_map[dv] = w
        
        ans = []
        for q in queries:
            if q in exact:
                ans.append(q)
                continue
            lq = q.lower()
            if lq in case_map:
                ans.append(case_map[lq])
                continue
            dq = devowel(q)
            if dq in vowel_map:
                ans.append(vowel_map[dq])
                continue
            ans.append("")
        return ans
```
- Notes about the solution:
  - The devowel function lowercases the word and replaces any vowel (a, e, i, o, u) with '*'. This gives a canonical form for vowel-error matching.
  - We preserve the first occurrence by only setting a mapping if the key is not already present.
  - Complexity:
    - Time: O(N * L + Q * L) where N = len(wordlist), Q = len(queries), L = max length of words (<= 7). Each key construction and lookup is O(L).
    - Space: O(N * L) for the maps and set.
  - This is the common, efficient approach for this problem and works within the constraints provided.