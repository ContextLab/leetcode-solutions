# [Problem 1930: Unique Length-3 Palindromic Subsequences](https://leetcode.com/problems/unique-length-3-palindromic-subsequences/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We want palindromes of length 3, so they must be of the form x y x (first and last characters equal). The only degrees of freedom are the outer character x and the middle character y. We need to count distinct strings "x y x" that appear as subsequences (not substrings). For a given outer character x, if we can find at least one occurrence of x before some position and at least one occurrence after that position, then any distinct character y that appears somewhere between the first and last occurrence of x will yield the palindrome x y x. So counting, for each outer letter x, the number of distinct letters present between the first and last occurrence of x gives the number of distinct palindromes with outer letter x. Sum over x (26 letters). That avoids double counting because each palindrome is determined uniquely by (x,y).

## Refining the problem, round 2 thoughts
- Edge cases: if a letter x appears fewer than 2 times (i.e., no index i<k with s[i]=s[k]=x), it contributes 0.
- Implementation: compute first and last index for each letter. For letters with first < last, collect distinct letters in s[first+1:last] (a set or boolean array). Complexity: scanning interior for each letter could be up to 26 * n ~ 2.6e6 operations for n=1e5, which is fine.
- Alternative: could compute prefix/suffix masks to avoid rescanning, but the simple approach is clear and fast enough.
- Time complexity: O(26 * n) = O(n). Space: O(1) extra (constant 26-sized arrays).

## Attempted solution(s)
```python
class Solution:
    def countPalindromicSubsequence(self, s: str) -> int:
        # record first and last occurrence for each lowercase letter
        first = [-1] * 26
        last = [-1] * 26
        for i, ch in enumerate(s):
            idx = ord(ch) - 97
            if first[idx] == -1:
                first[idx] = i
            last[idx] = i

        ans = 0
        # for each possible outer character, count distinct middle characters between first and last
        for c in range(26):
            if first[c] != -1 and first[c] < last[c]:
                seen = [False] * 26
                for j in range(first[c] + 1, last[c]):
                    seen[ord(s[j]) - 97] = True
                ans += sum(seen)
        return ans
```
- Notes:
  - Approach: For each outer character x (26 options), find its first and last index; if they exist with first < last, count the number of distinct characters in between — each distinct middle character y gives a unique palindrome x y x.
  - Time complexity: O(26 * n) = O(n) where n = len(s). For n up to 1e5 this is fast.
  - Space complexity: O(1) extra (arrays of size 26).