# [Problem 2981: Find Longest Special Substring That Occurs Thrice I](https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the longest substring composed of a single repeated character (a "special" substring) that appears at least 3 times in s. Because special substrings consist of a single character repeated, occurrences of such a substring can only come from contiguous runs of that character in s. For a run of length r of character c, how many substrings equal to c^L (L repeats of c) appear inside that run? It's r - L + 1 (if r >= L), since substrings can overlap inside the run.

So for each character, if we know the lengths of all its runs, we can test a candidate length L by summing max(0, r - L + 1) over runs; if the sum >= 3 then c^L occurs at least thrice. The problem reduces to examining possible lengths L for each character. The string length n <= 50, so brute force is very cheap.

## Refining the problem, round 2 thoughts
- Extract runs of each character (maximal contiguous same-character segments).
- For each character, check lengths L from its maximum run length down to 1. For each L compute total occurrences across runs using sum(max(0, r - L + 1)).
- Keep the maximum L among all characters with count >= 3. If none, return -1.
- Complexity: at most 26 characters, each with runs summing to n; checking all L up to n gives O(26 * n * n) worst-case which is trivial for n <= 50.
- Edge cases: single character repeated many times (e.g., "aaaa") — occurrences formula handles overlapping. Characters that appear but never with total occurrences >= 3 should be ignored. If no valid L for any char, return -1.

## Attempted solution(s)
```python
class Solution:
    def longestSpecial(self, s: str) -> int:
        n = len(s)
        # Build runs per character: list of run lengths for each character
        runs = {chr(ord('a') + i): [] for i in range(26)}
        i = 0
        while i < n:
            j = i + 1
            while j < n and s[j] == s[i]:
                j += 1
            runs[s[i]].append(j - i)
            i = j

        ans = -1
        # For each character, try lengths from largest run down to 1
        for c in runs:
            if not runs[c]:
                continue
            max_run = max(runs[c])
            # try larger L first so we can break early per character
            for L in range(max_run, 0, -1):
                # total occurrences of c^L across all runs
                total = 0
                for r in runs[c]:
                    if r >= L:
                        total += (r - L + 1)
                        # small optimization: if total already >= 3, we can stop summing
                        if total >= 3:
                            break
                if total >= 3:
                    ans = max(ans, L)
                    # no need to check smaller L for this character
                    break

        return ans
```
- Approach: group contiguous runs per character and count how many length-L same-character substrings each run contributes (r - L + 1). For each character, check lengths descending so the first valid length is the maximum for that character.
- Time complexity: O(26 * n * n) in worst case (n <= 50) => effectively constant / very fast.
- Space complexity: O(n) for storing run lengths.