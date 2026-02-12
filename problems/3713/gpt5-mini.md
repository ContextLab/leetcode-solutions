# [Problem 3713: Longest Balanced Substring I](https://leetcode.com/problems/longest-balanced-substring-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks for the longest substring in which every distinct character appears the same number of times. If a substring has k distinct characters and each appears t times, its length is k * t. A brute-force idea is to check all substrings and verify whether the counts of the present characters are equal. For a substring we can maintain a frequency array of size 26 (lowercase letters) and check if all nonzero frequencies are equal. n is at most 1000, so an O(n^2 * 26) check should be feasible.

I also think about smarter approaches: iterate over possible numbers of distinct characters k (1..26) and try to find substrings where every present character appears t times using sliding window or prefix sums. But given constraints, simpler double loop with an O(26) validation is straightforward and easy to implement correctly.

## Refining the problem, round 2 thoughts
Edge cases:
- Single-character strings should return 1.
- Substrings with only one distinct character are balanced.
- We should avoid unnecessary repeated work; but computing min and max counts from 26 slots is cheap.
- We can stop early in some inner loops? Not easily without complicating logic; current O(n^2 * 26) is acceptable for n <= 1000.

Time/space:
- Time: O(n^2 * 26) => O(n^2) effectively (26 is constant).
- Space: O(26) extra for frequency array.

I'll implement a double loop: for each start index i, expand end j updating counts; compute min (over nonzero) and max counts; if equal, update answer with current length.

## Attempted solution(s)
```python
class Solution:
    def longestBalancedSubstring(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0
        ans = 1  # at least one character is a balanced substring
        for i in range(n):
            counts = [0] * 26
            for j in range(i, n):
                counts[ord(s[j]) - 97] += 1
                # compute min nonzero and max
                mn = float('inf')
                mx = 0
                for c in counts:
                    if c > 0:
                        if c < mn:
                            mn = c
                        if c > mx:
                            mx = c
                # if no characters (shouldn't happen here) skip
                if mn == float('inf'):
                    continue
                if mn == mx:
                    ans = max(ans, j - i + 1)
        return ans
```

- Notes:
  - Approach: brute-force all substrings with an incremental frequency array for the current start index; validate balanced property by checking that all nonzero frequencies are equal (min_nonzero == max).
  - Time complexity: O(n^2 * 26) = O(n^2) for n = len(s). With n <= 1000 this is efficient enough.
  - Space complexity: O(1) extra beyond input (frequency array of size 26).
  - Implementation detail: ans initialized to 1 because any single character substring is balanced; handle empty string defensively although constraints guarantee length >= 1.